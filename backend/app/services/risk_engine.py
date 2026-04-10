from app.utils.email_utils import is_free_email
import re

# Constants
KNOWN_COMPANIES = ["amazon", "google", "microsoft", "infosys", "tcs"]
PAYMENT_KEYWORDS = ["pay", "payment", "fee", "deposit", "charges"]
URGENCY_KEYWORDS = ["urgent", "limited", "immediately"]
JOB_SCAM_KEYWORDS = ["pay", "fee", "confirm"]

CURRENCY_REGEX = r"(₹|\$|€|rs\.?|inr)\s?\d+"


def compute_risk(email_data, domain_data):
    score = 0
    reasons = []

    text = email_data.get("raw_text", "").lower()
    domain = email_data.get("domain")

    # ---------- HIGH PRIORITY SIGNALS ----------

    # Typosquatting
    typo = email_data.get("typosquatting", {})
    if typo.get("is_suspicious"):
        score += 70
        reasons.append(
            f"Typosquatting detected (looks like {typo.get('possible_legit')})"
        )

    # Link mismatch
    if email_data.get("link_mismatches"):
        score += 50
        reasons.append("Links point to different domain than sender")

    # Payment detection
    if any(word in text for word in PAYMENT_KEYWORDS):
        score += 40
        reasons.append("Payment-related language detected")

    # Monetary detection (independent)
    if re.search(CURRENCY_REGEX, text):
        score += 30
        reasons.append("Monetary amount detected")

    # Job scam pattern
    if "job" in text and any(word in text for word in JOB_SCAM_KEYWORDS):
        score += 20
        reasons.append("Suspicious job-related payment pattern")

    # ---------- MEDIUM PRIORITY SIGNALS ----------

    # Free email
    if domain and is_free_email(domain):
        score += 30
        reasons.append("Free email provider used")

    # Company checks
    for company in KNOWN_COMPANIES:
        if company in text:
            if domain is None:
                score += 30
                reasons.append(
                    f"Company '{company}' mentioned without official domain"
                )
            elif company not in domain:
                score += 30
                reasons.append(
                    f"Company '{company}' mismatch with domain"
                )

    # ---------- LOW PRIORITY SIGNALS ----------

    if any(word in text for word in URGENCY_KEYWORDS):
        score += 10
        reasons.append("Urgency language detected")

    age = domain_data.get("domain_age_days")
    if age is not None and age < 180:
        score += 15
        reasons.append("New domain")

    if domain is not None and domain_data.get("has_mx_record") is False:
        score += 20
        reasons.append("No MX record")

    # ---------- FINAL ----------

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