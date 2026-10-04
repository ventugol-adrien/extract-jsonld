from argparse import ArgumentParser
import json
from pathlib import Path
import sys

from extract_jsonld.db import save_page_and_tags
from extract_jsonld.models import JobPosting
from extract_jsonld.services import fetch_html, extract_tags


def select_platform(data: dict, url: str) -> str:
    match url:
        case _ if "ashby" in url:
            return "ashby"
        case _:
            return "unknown"


def main():
    parser = ArgumentParser(description="Extract JSON-LD from web pages")
    parser.add_argument(
        "-p", "--path", help="File path of the web page to extract JSON-LD from"
    )
    parser.add_argument(
        "-u", "--url", help="URL of the web page to extract JSON-LD from"
    )
    args = parser.parse_args()
    raw_html = ""
    if args.path == "-":
        raw_html = sys.stdin.read()
        source_url = "stdin:"
    elif args.path:
        # print(f"Extracting JSON-LD from file path: {args.path}")
        source_path = Path(args.path)
        raw_html = source_path.read_text()
        source_url = source_path.resolve().as_uri()

    elif args.url:
        # print(f"Extracting JSON-LD from URL: {args.url}")
        raw_html = fetch_html(args.url)
        source_url = args.url
    elif not sys.stdin.isatty():
        raw_html = sys.stdin.read()
        source_url = "stdin:"
    else:
        parser.error("provide a path or URL, or pipe HTML through stdin")

    extracted_data = extract_tags(raw_html, "script")
    save_page_and_tags(source_url, raw_html, extracted_data)
    print(json.dumps(extracted_data, indent=2))


if __name__ == "__main__":
    main()
