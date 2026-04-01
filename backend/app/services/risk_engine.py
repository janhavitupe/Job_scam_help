from app.utils.email_utils import is_free_email
import re

KNOWN_COMPANIES = ["amazon", "google", "microsoft", "infosys", "tcs"]

def compute_risk(email_data, domain_data):
    score = 0
    reasons = []
    text = email_data.get("raw_text", "").lower()
    domain = email_data.get("domain")

    # HIGH PRIORITY SIGNALS ----------------------

    # Typosquatting (VERY STRONG)
    typo = email_data.get("typosquatting", {})
    if typo.get("is_suspicious"):
        score += 70
        reasons.append(f"Typosquatting detected (looks like {typo.get('possible_legit')})")

    # Link mismatch (VERY STRONG)
    if email_data.get("link_mismatches"):
        score += 50
        reasons.append("Links point to different domain than sender")

    # Payment detection (VERY STRONG)
    if "fee" in text or "payment" in text:
        score += 40
        reasons.append("Payment request detected")

        if re.search(r"\d{3,}", text):
            score += 20
            reasons.append("Monetary amount mentioned")

    # MEDIUM SIGNALS ----------------------

    # Free email
    if domain and is_free_email(domain):
        score += 30
        reasons.append("Free email provider used")

    # Company mismatch
    for company in KNOWN_COMPANIES:
        if company in text and domain:
            if company not in domain:
                score += 30
                reasons.append(f"Company '{company}' mismatch with domain")

    # LOW SIGNALS ----------------------

    if any(word in text for word in ["urgent", "limited", "immediately"]):
        score += 10
        reasons.append("Urgency language detected")

    age = domain_data.get("domain_age_days")
    if age is not None and age < 180:
        score += 15
        reasons.append("New domain")

    if not domain_data.get("has_mx_record"):
        score += 20
        reasons.append("No MX record")

    # Final cap
    score = min(score, 100)

    return {
        "risk_score": score,
        "risk_level": (
            "HIGH" if score >= 70 else
            "MEDIUM" if score >= 40 else
            "LOW"
        ),
        "reasons": reasons
    }