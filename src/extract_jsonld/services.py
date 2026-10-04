from httpx import get
import re, json
from bs4 import BeautifulSoup, Tag
from typing import List, Dict, Any


def fetch_html(url: str) -> str:
    response = get(url)
    response.raise_for_status()
    return response.text


# Match ld+json type attribute (case-insensitive, ignores extra params like charset)
LD_JSON_PATTERN = re.compile(r"^application/ld\+json", re.IGNORECASE)

# Strips CDATA and JS comment wrappers that break json.loads
CDATA_PATTERN = re.compile(
    r"^\s*(?://\s*<!\[CDATA\[|<!\[CDATA\[|/\*\s*<!\[CDATA\[\s*\*/|\s*/\*|\s*//)"
    r"|(?:(?://\s*)?\]\]>|/\*\s*\]\]>\s*\*/|\*/)\s*$",
    re.MULTILINE,
)


def _clean(tag: Tag) -> Dict[str, Any]:
    raw_text = tag.get_text(strip=True)
    if not raw_text:
        return
    cleaned = CDATA_PATTERN.sub("", raw_text).strip()
    try:
        return json.loads(cleaned, strict=False)
    except json.JSONDecodeError:
        return None


def extract_tags(raw_html: str, tag: str) -> List[Dict[str, Any]]:

    soup = BeautifulSoup(raw_html, "html.parser")
    return [
        _clean(tag) for tag in soup.find_all("script", attrs={"type": LD_JSON_PATTERN})
    ]
