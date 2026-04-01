import re
from email_validator import validate_email, EmailNotValidError
import tldextract

def extract_email_components(text: str):
    email_pattern = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
    emails = re.findall(email_pattern, text)

    sender_email = emails[0] if emails else None

    domain = None
    if sender_email:
        try:
            valid = validate_email(sender_email)
            domain = valid.domain
        except EmailNotValidError:
            domain = None

    links = re.findall(r'https?://\S+', text)

    return {
        "sender_email": sender_email,
        "domain": domain,
        "links": links
    }