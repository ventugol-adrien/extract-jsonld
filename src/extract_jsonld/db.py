import json
import sqlite3
from contextlib import closing
from pathlib import Path
from typing import Iterable

DEFAULT_DB_PATH = (
    Path(__file__).resolve().parent.parent.parent / "data" / "extractions.db"
)
SCHEMA_PATH = Path(__file__).resolve().parents[2] / "sql" / "schema.sql"


def get_connection(db_path: Path = DEFAULT_DB_PATH) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(db_path)
    try:
        connection.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
    except Exception:
        connection.close()
        raise
    return connection


def save_page_and_tags(
    url: str,
    html: str,
    tags: Iterable[object],
    db_path: Path = DEFAULT_DB_PATH,
) -> None:
    with closing(get_connection(db_path)) as connection, connection:
        connection.execute(
            """
            INSERT INTO web_pages (url, html)
            VALUES (?, ?)
            ON CONFLICT(url) DO UPDATE SET
                html = excluded.html,
                fetched_at = CURRENT_TIMESTAMP
            """,
            (url, html),
        )
        page_id = connection.execute(
            "SELECT id FROM web_pages WHERE url = ?", (url,)
        ).fetchone()[0]
        connection.execute("DELETE FROM ldjson_payloads WHERE page_id = ?", (page_id,))
        connection.executemany(
            """
            INSERT INTO ldjson_payloads (page_id, tag_index, raw_content)
            VALUES (?, ?, ?)
            """,
            [
                (page_id, index, json.dumps(tag, ensure_ascii=False, allow_nan=False))
                for index, tag in enumerate(tags)
                if tag is not None
            ],
        )
