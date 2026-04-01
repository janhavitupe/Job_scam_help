import whois
import datetime
import dns.resolver

def get_domain_age(domain):
    try:
        w = whois.whois(domain)
        creation_date = w.creation_date

        if isinstance(creation_date, list):
            creation_date = creation_date[0]

        if creation_date:
            age_days = (datetime.datetime.now() - creation_date).days
            return age_days
    except:
        return None

def has_mx_record(domain):
    try:
        answers = dns.resolver.resolve(domain, 'MX')
        return len(answers) > 0
    except:
        return False

def analyze_domain(domain):
    if not domain:
        return {}

    age = get_domain_age(domain)
    mx = has_mx_record(domain)

    return {
        "domain_age_days": age,
        "has_mx_record": mx
    }