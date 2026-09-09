def calculate_scores(validation_data: dict, test_results: list) -> dict:
    def to_score(passed: bool, weight: float = 100.0) -> float:
        return weight if passed else 0.0

    def pct_passed(results: list) -> float:
        if not results:
            return 0.0
        passed = sum(1 for r in results if r.get("passed"))
        return round((passed / len(results)) * 100, 2)

    feature_completion = to_score(validation_data["structure"]["passed"])
    code_quality = to_score(validation_data["security"]["passed"])
    architecture = to_score(validation_data["structure"]["passed"] and validation_data["db"]["passed"])
    security = to_score(validation_data["security"]["passed"])
    api_quality = to_score(validation_data["api"]["passed"])
    deployment_readiness = pct_passed(test_results)

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
