import docker
import time
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.logger import get_logger
from app.models.submission import Submission, SubmissionStatus
from app.sandbox.repo_handler import clone_repo, cleanup_repo
from app.sandbox.language_configs.config_loader import get_language_config
from app.validation.structure_check import check_structure
from app.validation.api_check import check_api
from app.validation.db_check import check_database
from app.validation.auth_check import check_auth
from app.validation.security_check import check_security
from app.testing.api_test_runner import run_api_tests
from app.ai_engine.scorer import calculate_scores
from app.ai_engine.feedback_generator import generate_feedback
from app.ai_engine.plagiarism_check import check_plagiarism
from app.reports.report_builder import build_report
from app.models.evaluation import Evaluation
from app.models.score import Score
from app.models.leaderboard import LeaderboardEntry

logger = get_logger("docker_runner")
client = docker.from_env()


def run_sandbox_pipeline(submission_id, db: Session):
    submission = db.query(Submission).filter(Submission.id == submission_id).first()
    local_path = None
    container = None

    try:
        # 1. Clone
        submission.status = SubmissionStatus.CLONING
        db.commit()
        local_path = clone_repo(submission.source_url, str(submission.id))

        # 2. Build + Run
        submission.status = SubmissionStatus.BUILDING
        db.commit()
        config = get_language_config(submission.language_stack)

        container = client.containers.run(
            image=config["base_image"],
            command=config["run_command"],
            volumes={local_path: {"bind": "/app", "mode": "rw"}},
            working_dir="/app",
            detach=True,
            mem_limit="512m",
            network_mode="bridge",
        )
        submission.status = SubmissionStatus.RUNNING
        db.commit()
        time.sleep(5)  # give app time to boot

        # 3. Validation
        structure_result = check_structure(local_path)
        api_result = check_api(config.get("health_endpoint"))
        db_result = check_database(local_path)
        auth_result = check_auth(config.get("auth_endpoint"))
        security_result = check_security(local_path)

        # 4. Testing
        submission.status = SubmissionStatus.TESTING
        db.commit()
        test_results = run_api_tests(local_path, config)

        # 5. AI Scoring + Feedback + Plagiarism
        submission.status = SubmissionStatus.EVALUATING
        db.commit()

        validation_data = {
            "structure": structure_result,
            "api": api_result,
            "db": db_result,
            "auth": auth_result,
            "security": security_result,
        }
        scores = calculate_scores(validation_data, test_results)
        feedback = generate_feedback(validation_data, test_results, scores)
        plagiarism = check_plagiarism(local_path, db)

        # 6. Save results
        score_row = Score(submission_id=submission.id, **scores)
        db.add(score_row)

        eval_row = Evaluation(
            submission_id=submission.id,
            plagiarism_score=plagiarism["score"],
            plagiarism_matches=plagiarism["matches"],
            **feedback,
        )
        db.add(eval_row)

        leaderboard_row = LeaderboardEntry(
            submission_id=submission.id,
            student_name=submission.student_name,
            project_name=submission.project_name,
            overall_score=scores["overall_score"],
            architecture_score=scores["architecture_score"],
            api_quality_score=scores["api_quality_score"],
        )
        db.add(leaderboard_row)

        submission.status = SubmissionStatus.COMPLETED
        db.commit()

        # 7. Report
        build_report(submission, score_row, eval_row)

    except Exception as e:
        logger.error(f"Pipeline failed for {submission_id}: {e}")
        submission.status = SubmissionStatus.FAILED
        db.commit()

    finally:
        if container:
            try:
                container.stop(timeout=5)
                container.remove()
            except Exception:
                pass
        if local_path:
            cleanup_repo(local_path)
