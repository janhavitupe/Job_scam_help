FREE_EMAIL_PROVIDERS = {
    "gmail.com", "yahoo.com", "outlook.com", "hotmail.com"
}

def is_free_email(domain):
    return domain in FREE_EMAIL_PROVIDERS