# extract-jsonld

`extract-jsonld` fetches or reads an HTML page, extracts JSON-LD from its
`<script type="application/ld+json">` elements, prints the parsed values as a
JSON array, and stores the page and extracted data in SQLite.

## Requirements

- Python 3.14 or newer
- [uv](https://docs.astral.sh/uv/) for installing and running the project

From the project directory, install the project and its dependencies:

```sh
uv sync
```

## Usage

The command accepts one positional argument, either a URL or a local file path.
If non-empty standard input is piped, it reads raw HTML from stdin first, even
if a positional argument or `SCRAPE_URL` is also present. Otherwise, it uses
the positional argument if provided, then falls back to the `SCRAPE_URL`
environment variable, which must be an HTTP(S) URL.

Fetch a page from a URL:

```sh
uv run extract-jsonld https://example.com/jobs/123
```

Read a local HTML file:

```sh
uv run extract-jsonld ./page.html
```

Read HTML from standard input:

```sh
cat page.html | uv run extract-jsonld
```

Fetch the URL from the environment:

```sh
SCRAPE_URL=https://example.com/jobs/123 uv run extract-jsonld
```

The command prints a JSON array to standard output. Each array element
corresponds to a matching JSON-LD script. A script with invalid or empty JSON
produces `null` in the output and is not saved as an extracted payload.

## Stored data

The SQLite database defaults to `data/extractions.db` in the project directory.
The tables and indexes are initialized from [`sql/schema.sql`](./sql/schema.sql).
Each run stores the source HTML in `web_pages` and its valid extracted JSON-LD
values in `ldjson_payloads`.

Running the utility again for the same URL or local file updates its saved HTML
and replaces its previous payloads. Local files are identified by their
resolved `file://` URI. Stdin input uses the source key `stdin:`, so each
stdin run replaces the previously stored stdin input.
