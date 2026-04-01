from app.utils.email_utils import is_free_email
import re

KNOWN_COMPANIES = ["amazon", "google", "microsoft", "infosys", "tcs"]

def compute_risk(email_data, domain_data):
    score = 0
    reasons = []
    text = email_data.get("raw_text", "").lower()
    domain = email_data.get("domain")

    # 🚩 Free email provider
    if domain and is_free_email(domain):
        score += 30
        reasons.append("Free email provider used (not corporate domain)")

    # 🚩 Payment detection (strong)
    if "fee" in text or "payment" in text:
        score += 30
        reasons.append("Payment request detected")

        # amount detection
        if re.search(r"\d{3,}", text):
            score += 20
            reasons.append("Monetary amount mentioned")

    # 🚩 Company mismatch
    for company in KNOWN_COMPANIES:
        if company in text and domain:
            if company not in domain:
                score += 30
                reasons.append(f"Company name '{company}' does not match email domain")

    # 🚩 Suspicious urgency
    if any(word in text for word in ["urgent", "limited", "immediately"]):
        score += 10
        reasons.append("Urgency language detected")

    # domain checks (keep old ones)
    age = domain_data.get("domain_age_days")
    if age is not None and age < 180:
        score += 20
        reasons.append("New domain")

    if not domain_data.get("has_mx_record"):
        score += 20
        reasons.append("No MX record")

    score = min(score, 100)

    return {
        "risk_score": score,
        "risk_level": (
            "HIGH" if score > 70 else
            "MEDIUM" if score > 40 else
            "LOW"
        ),
        "reasons": reasons
    }