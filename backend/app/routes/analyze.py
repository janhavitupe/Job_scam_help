from fastapi import APIRouter
from pydantic import BaseModel

from app.services.email_parser import extract_email_components
from app.services.domain_checker import analyze_domain
from app.services.risk_engine import compute_risk

router = APIRouter()

class EmailInput(BaseModel):
    text: str

@router.post("/")
def analyze_email(input: EmailInput):
    parsed = extract_email_components(input.text)
    parsed["raw_text"] = input.text

    domain_info = analyze_domain(parsed.get("domain"))
    risk = compute_risk(parsed, domain_info)

    return {
        "email_data": parsed,
        "domain_data": domain_info,
        "risk_analysis": risk
    }