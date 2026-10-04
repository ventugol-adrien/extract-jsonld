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

Fetch a page from a URL:

```sh
uv run extract-jsonld --url https://example.com/jobs/123
```

Read a local HTML file:

```sh
uv run extract-jsonld --path ./page.html
```

Read HTML from standard input, either by piping it or using `-` as the path:

```sh
cat page.html | uv run extract-jsonld
uv run extract-jsonld --path - < page.html
```

The command prints a JSON array to standard output. Each array element
corresponds to a matching JSON-LD script. A script with invalid or empty JSON
produces `null` in the output and is not saved as an extracted payload.

Use `--help` to see the available options:

```sh
uv run extract-jsonld --help
```

## Stored data

The SQLite database defaults to `data/extractions.db` in the project directory.
The tables and indexes are initialized from [`sql/schema.sql`](./sql/schema.sql).
Each run stores the source HTML in `web_pages` and its valid extracted JSON-LD
values in `ldjson_payloads`.

Running the utility again for the same URL or local file updates its saved HTML
and replaces its previous payloads. Local files are identified by their
resolved `file://` URI. Stdin input uses the source key `stdin:`, so each
stdin run replaces the previously stored stdin input.
