from fastapi import APIRouter
from pydantic import BaseModel

from app.services.data_collector import log_email
from app.services.email_parser import extract_email_components
from app.services.domain_checker import analyze_domain
from app.services.risk_engine import compute_risk
from app.services.link_analyzer import extract_link_domains, check_link_mismatch
from app.utils.domain_utils import is_typosquatted
from app.services.ml_model import predict_scam
from app.services.hybrid_engine import compute_final_risk

router = APIRouter()


class EmailInput(BaseModel):
    text: str


@router.post("/")
def analyze_email(input: EmailInput):
    # -------- Parse Email --------
    parsed = extract_email_components(input.text)
    parsed["raw_text"] = input.text

    # -------- Domain Analysis --------
    domain_info = analyze_domain(parsed.get("domain"))

    # -------- Link Analysis --------
    link_domains = extract_link_domains(parsed.get("links", []))
    mismatches = check_link_mismatch(parsed.get("domain"), link_domains)

    # -------- Typosquatting --------
    typo_flag, legit_domain = is_typosquatted(parsed.get("domain"))

    parsed["link_domains"] = link_domains
    parsed["link_mismatches"] = mismatches
    parsed["typosquatting"] = {
        "is_suspicious": typo_flag,
        "possible_legit": legit_domain
    }

    # -------- Rule-based Risk --------
    risk = compute_risk(parsed, domain_info)

    # -------- ML Prediction --------
    ml_result = predict_scam(input.text)

    # -------- Hybrid Decision --------
    final_result = compute_final_risk(risk, ml_result, parsed)

    # -------- Data Logging (FIXED) --------
    # Auto-label: HIGH → 1 (scam), else → 0 (likely legit)
    label = 1 if final_result["final_level"] == "HIGH" else 0
    log_email(input.text, label)

    # -------- Response --------
    return {
        "email_data": parsed,
        "domain_data": domain_info,
        "risk_analysis": risk,
        "ml_analysis": ml_result,
        "final_analysis": final_result
    }