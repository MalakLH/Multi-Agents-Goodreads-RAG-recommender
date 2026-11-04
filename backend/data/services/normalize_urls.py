from urllib.parse import urlparse, urlunparse
import re


def normalize_goodreads_url(url: str) -> str:
    """
    Normalize a Goodreads book URL to avoid duplicate entries.

    - Removes query parameters
    - Removes fragments
    - Removes trailing slashes
    - Standardizes the hostname
    """

    if not url:
        return ""

    url = url.strip()

    parsed = urlparse(url)

    # Standardize hostname
    hostname = (parsed.hostname or "").lower()

    # Keep only the path, without query parameters or fragments
    path = parsed.path.rstrip("/")

    # Remove trailing numeric Goodreads edition IDs when appropriate?
    # No: preserve the complete path to avoid merging different editions.

    normalized = urlunparse((
        "https",
        hostname,
        path,
        "",
        "",
        ""
    ))

    return normalized