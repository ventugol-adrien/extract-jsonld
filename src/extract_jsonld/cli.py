from argparse import ArgumentParser
import json
import os
from pathlib import Path
import sys
from urllib.parse import urlparse

from extract_jsonld.db import save_page_and_tags
from extract_jsonld.services import fetch_html, extract_tags


def _is_url(source: str) -> bool:
    parsed = urlparse(source)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def main():
    parser = ArgumentParser(description="Extract JSON-LD from web pages")
    parser.add_argument(
        "source",
        nargs="?",
        help="file path or http(s) URL; overrides SCRAPE_URL unless stdin is piped",
    )
    args = parser.parse_args()

    raw_html = sys.stdin.read() if not sys.stdin.isatty() else ""
    if raw_html.strip():
        source_url = "stdin:"
    else:
        source = (
            args.source
            if args.source is not None
            else os.environ.get("SCRAPE_URL")
        )
        if not source:
            parser.error(
                "provide a path or URL, set SCRAPE_URL, or pipe HTML through stdin"
            )
        if args.source is None and not _is_url(source):
            parser.error("SCRAPE_URL must be an http(s) URL")

        if _is_url(source):
            raw_html = fetch_html(source)
            source_url = source
        else:
            source_path = Path(source)
            raw_html = source_path.read_text()
            source_url = source_path.resolve().as_uri()

    extracted_data = extract_tags(raw_html, "script")
    save_page_and_tags(source_url, raw_html, extracted_data)
    print(json.dumps(extracted_data, indent=2))


if __name__ == "__main__":
    main()
