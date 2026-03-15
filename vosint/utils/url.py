from urllib.parse import urlparse, urlunparse


def canonicalize_url(url: str) -> str:
    parsed = urlparse(url.strip())
    path = parsed.path.rstrip("/")
    return urlunparse((parsed.scheme.lower(), parsed.netloc.lower(), path, "", parsed.query, ""))


def root_domain(url: str) -> str:
    return urlparse(url).netloc.lower().split(":")[0]
