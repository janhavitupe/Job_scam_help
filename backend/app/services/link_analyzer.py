import tldextract

def extract_link_domains(links):
    domains = []

    for link in links:
        ext = tldextract.extract(link)
        domain = f"{ext.domain}.{ext.suffix}"
        domains.append(domain)

    return domains


def check_link_mismatch(email_domain, link_domains):
    mismatches = []

    for d in link_domains:
        if email_domain and d != email_domain:
            mismatches.append(d)

    return mismatches