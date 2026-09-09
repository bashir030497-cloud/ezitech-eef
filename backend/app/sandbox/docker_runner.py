import docker
import time
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.logger import get_logger
from app.models.submission import Submission, SubmissionStatus
from app.sandbox.repo_handler import get_project_source, cleanup_repo
from app.sandbox.language_configs.config_loader import (
    get_language_config, detect_custom_dockerfile, detect_custom_compose,
)
from app.sandbox.compose_runner import compose_up, compose_down, compose_service_port
from app.validation.structure_check import check_structure
from app.validation.api_check import check_api
from app.validation.db_check import check_database
from app.validation.auth_check import check_auth
from app.validation.security_check import check_security
from app.testing.api_test_runner import run_api_tests
from app.testing.db_test_runner import run_db_tests
from app.testing.perf_check import run_perf_check
from app.ai_engine.scorer import calculate_scores
from app.ai_engine.feedback_generator import generate_feedback
from app.ai_engine.plagiarism_check import check_plagiarism
from app.reports.report_builder import build_report
from app.models.evaluation import Evaluation
from app.models.score import Score
from app.models.leaderboard import LeaderboardEntry
from app.models.test_result import TestResult

logger = get_logger("docker_runner")
client = docker.from_env()


def run_sandbox_pipeline(submission_id, db: Session):
    submission = db.query(Submission).filter(Submission.id == submission_id).first()
    local_path = None
    container = None
    is_compose_run = False
    compose_project_name = f"eef-{str(submission.id)[:8]}"
    build_start_time = None
    build_time_seconds = None
    health_endpoint = None
    auth_endpoint = None

    try:
        submission.status = SubmissionStatus.CLONING
        db.commit()
        local_path = get_project_source(submission, str(submission.id))

        submission.status = SubmissionStatus.BUILDING
        db.commit()
        config = get_language_config(submission.language_stack)
        health_endpoint = config.get("health_endpoint")
        auth_endpoint = config.get("auth_endpoint")

        custom_compose = detect_custom_compose(local_path)
        custom_dockerfile = detect_custom_dockerfile(local_path)
        build_start_time = time.time()

        if custom_compose:
            logger.info(f"Custom docker-compose stack detected for {submission.id}")
            is_compose_run = True
            compose_up(local_path, compose_project_name, timeout=600)
            mapped_port = None
            for service_guess in ("app", "backend", "api", "web"):
                mapped_port = compose_service_port(local_path, compose_project_name, service_guess, 8000)
                if mapped_port:
                    break
            if mapped_port:
                health_endpoint = f"http://localhost:{mapped_port}/health"
                auth_endpoint = f"http://localhost:{mapped_port}/auth/login"

        elif custom_dockerfile:
            logger.info(f"Custom Dockerfile detected for {submission.id}, building from it")
            image, _ = client.images.build(path=local_path, rm=True, forcerm=True)
            container = client.containers.run(
                image=image.id,
                detach=True,
                mem_limit="1g",
                network_mode="bridge",
                ports={"8000/tcp": None},
            )
        else:
            container = client.containers.run(
                image=config["base_image"],
                command=config["run_command"],
                volumes={local_path: {"bind": "/app", "mode": "rw"}},
                working_dir="/app",
                detach=True,
                mem_limit="1g",
                network_mode="bridge",
            )

        submission.status = SubmissionStatus.RUNNING
        db.commit()
        time.sleep(config.get("boot_wait_seconds", 5) if not is_compose_run else 15)
        build_time_seconds = round(time.time() - build_start_time, 2)

        structure_result = check_structure(local_path)
        api_result = check_api(health_endpoint)
        db_result = check_database(local_path)
        auth_result = check_auth(auth_endpoint)
        security_result = check_security(local_path)

        submission.status = SubmissionStatus.TESTING
        db.commit()
        api_test_results = run_api_tests(local_path, {"health_endpoint": health_endpoint})
        db_test_result = run_db_tests(local_path)
        perf_result = run_perf_check(health_endpoint)

        all_test_results = list(api_test_results)
        all_test_results.append({
            "test_name": "db_migration_check",
            "passed": db_test_result["passed"],
            "details": db_test_result["details"],
        })
        all_test_results.append({
            "test_name": "performance_check",
            "passed": perf_result["passed"],
            "details": f"{perf_result.get('response_time_ms')} ms",
        })

        for t in all_test_results:
            db.add(TestResult(
                submission_id=submission.id,
                test_type="api" if "health" in t["test_name"] else t["test_name"].split("_")[0],
                test_name=t["test_name"],
                passed=t["passed"],
                details=str(t.get("details", "")),
            ))

        submission.status = SubmissionStatus.EVALUATING
        db.commit()

        validation_data = {
            "structure": structure_result,
            "api": api_result,
            "db": db_result,
            "auth": auth_result,
            "security": security_result,
        }
        scores = calculate_scores(validation_data, all_test_results)
        feedback = generate_feedback(validation_data, all_test_results, scores)
        plagiarism = check_plagiarism(local_path, db)

        documentation_score = 100.0 if structure_result.get("has_readme") else 0.0

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
            build_time_seconds=build_time_seconds,
            documentation_score=documentation_score,
            performance_score=100.0 if perf_result["passed"] else 0.0,
        )
        db.add(leaderboard_row)

        submission.status = SubmissionStatus.COMPLETED
        db.commit()

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
        if is_compose_run and local_path:
            compose_down(local_path, compose_project_name)
        if local_path:
            cleanup_repo(local_path)
