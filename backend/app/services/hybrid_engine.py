def compute_final_risk(rule_result, ml_result, email_data):
    rule_score = rule_result["risk_score"]
    ml_prob = ml_result["ml_probability"] * 100

    # adaptive weighting
    if email_data.get("domain") is None:
        # less structured data → trust ML more
        rule_weight = 0.4
        ml_weight = 0.6
    else:
        rule_weight = 0.6
        ml_weight = 0.4

    final_score = (rule_weight * rule_score) + (ml_weight * ml_prob)

    if final_score >= 70:
        level = "HIGH"
    elif final_score >= 40:
        level = "MEDIUM"
    else:
        level = "LOW"

    return {
        "final_score": round(final_score, 2),
        "final_level": level,
        "rule_score": rule_score,
        "ml_probability": ml_result["ml_probability"],
        "weights": {
            "rule_weight": rule_weight,
            "ml_weight": ml_weight
        }
    }