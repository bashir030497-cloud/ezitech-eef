def calculate_scores(validation_data: dict, test_results: list) -> dict:
    def to_score(passed: bool, weight: float = 100.0) -> float:
        return weight if passed else 0.0

    feature_completion = to_score(validation_data["structure"]["passed"])
    code_quality = to_score(validation_data["security"]["passed"])
    architecture = to_score(validation_data["structure"]["passed"] and validation_data["db"]["passed"])
    security = to_score(validation_data["security"]["passed"])
    api_quality = to_score(validation_data["api"]["passed"])
    deployment_readiness = to_score(all(t["passed"] for t in test_results) if test_results else False)
    engineering_maturity = round(
        (feature_completion + code_quality + architecture + security + api_quality + deployment_readiness) / 6, 2
    )

    overall = round(
        (feature_completion + code_quality + architecture + security + api_quality
         + deployment_readiness + engineering_maturity) / 7, 2
    )

    return {
        "feature_completion_score": feature_completion,
        "code_quality_score": code_quality,
        "architecture_score": architecture,
        "security_score": security,
        "api_quality_score": api_quality,
        "deployment_readiness_score": deployment_readiness,
        "engineering_maturity_score": engineering_maturity,
        "overall_score": overall,
    }
