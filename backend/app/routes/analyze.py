from fastapi import APIRouter
from pydantic import BaseModel

from app.services.email_parser import extract_email_components
from app.services.domain_checker import analyze_domain
from app.services.risk_engine import compute_risk

from app.services.link_analyzer import extract_link_domains, check_link_mismatch
from app.utils.domain_utils import is_typosquatted

router = APIRouter()

class EmailInput(BaseModel):
    text: str

@router.post("/")
def analyze_email(input: EmailInput):
    parsed = extract_email_components(input.text)
    parsed["raw_text"] = input.text

    domain_info = analyze_domain(parsed.get("domain"))

    # 🔗 Link analysis
    link_domains = extract_link_domains(parsed.get("links", []))
    mismatches = check_link_mismatch(parsed.get("domain"), link_domains)

    # 🌐 Typosquatting
    typo_flag, legit_domain = is_typosquatted(parsed.get("domain"))

    # Add to parsed
    parsed["link_domains"] = link_domains
    parsed["link_mismatches"] = mismatches
    parsed["typosquatting"] = {
        "is_suspicious": typo_flag,
        "possible_legit": legit_domain
    }

    risk = compute_risk(parsed, domain_info)

    return {
        "email_data": parsed,
        "domain_data": domain_info,
        "risk_analysis": risk
    }