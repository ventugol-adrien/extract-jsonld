import io
import json
import sys
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from extract_jsonld import cli


class CliTests(unittest.TestCase):
    def test_empty_non_tty_stdin_falls_back_to_url_argument(self):
        url = "https://jobs.ashbyhq.com/livekit/example"
        extracted = [{"@type": "JobPosting"}]
        output = io.StringIO()

        with (
            patch.object(sys, "argv", ["extract-jsonld", url]),
            patch.object(sys, "stdin", io.StringIO("")),
            patch.object(cli, "fetch_html", return_value="<html></html>") as fetch,
            patch.object(cli, "extract_tags", return_value=extracted),
            patch.object(cli, "save_page_and_tags") as save,
            redirect_stdout(output),
        ):
            cli.main()

        fetch.assert_called_once_with(url)
        save.assert_called_once_with(url, "<html></html>", extracted)
        self.assertEqual(json.loads(output.getvalue()), extracted)


if __name__ == "__main__":
    unittest.main()
