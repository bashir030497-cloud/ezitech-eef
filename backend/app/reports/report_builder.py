import os
from app.core.logger import get_logger

logger = get_logger("report_builder")
REPORTS_DIR = "reports_output"


def build_report(submission, score_row, eval_row) -> str:
    os.makedirs(REPORTS_DIR, exist_ok=True)
    file_path = os.path.join(REPORTS_DIR, f"{submission.id}.html")

    html = f"""
    <html>
    <head><title>Evaluation Report - {submission.project_name}</title></head>
    <body>
        <h1>{submission.project_name}</h1>
        <p><b>Student:</b> {submission.student_name}</p>
        <p><b>Language Stack:</b> {submission.language_stack}</p>
        <h2>Scores</h2>
        <ul>
            <li>Feature Completion: {score_row.feature_completion_score}</li>
            <li>Code Quality: {score_row.code_quality_score}</li>
            <li>Architecture: {score_row.architecture_score}</li>
            <li>Security: {score_row.security_score}</li>
            <li>API Quality: {score_row.api_quality_score}</li>
            <li>Deployment Readiness: {score_row.deployment_readiness_score}</li>
            <li>Engineering Maturity: {score_row.engineering_maturity_score}</li>
            <li><b>Overall: {score_row.overall_score}</b></li>
        </ul>
        <h2>Feedback</h2>
        <p><b>Strengths:</b> {eval_row.strengths}</p>
        <p><b>Weaknesses:</b> {eval_row.weaknesses}</p>
        <p><b>Missing Requirements:</b> {eval_row.missing_requirements}</p>
        <p><b>Security Risks:</b> {eval_row.security_risks}</p>
        <p><b>Performance Suggestions:</b> {eval_row.performance_suggestions}</p>
        <p><b>Refactoring Suggestions:</b> {eval_row.refactoring_suggestions}</p>
        <p><b>Improvement Roadmap:</b> {eval_row.improvement_roadmap}</p>
        <h2>Plagiarism</h2>
        <p>Score: {eval_row.plagiarism_score} | Matches: {eval_row.plagiarism_matches}</p>
    </body>
    </html>
    """

    with open(file_path, "w") as f:
        f.write(html)

    logger.info(f"Report generated: {file_path}")
    return file_path
