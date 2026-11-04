"""Source-order, evidence gating and CLI contracts for the M3 donor overlay."""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from m3.catalogue import CatalogueError, ROOT, load_candidates, select_candidates


class M3CatalogueTest(unittest.TestCase):
    def test_real_candidates_are_source_ordered_and_not_approved(self):
        candidates = load_candidates()
        self.assertEqual(
            ["csvfix", "csvkit", "csvtk", "dasel", "gron", "jq",
             "Miller", "VisiData", "xsv"],
            [candidate["name"] for candidate in candidates])
        for candidate in candidates:
            self.assertEqual("candidate", candidate["review_status"])
            self.assertEqual("unverified", candidate["license_status"])
            self.assertEqual("not-run", candidate["benchmark_status"])
            self.assertEqual("not-evaluated", candidate["implementation_status"])

    def test_category_operation_and_tag_filters_intersect(self):
        candidates = load_candidates()
        self.assertEqual(
            ["csvkit", "csvtk", "Miller", "xsv"],
            [item["name"] for item in select_candidates(
                candidates, categories=["structured-search"], operations=["join"])])
        self.assertEqual(
            ["dasel", "gron", "jq"],
            [item["name"] for item in select_candidates(
                candidates, tags=["json"], categories=["format-conversion"])])
        self.assertEqual([], select_candidates(candidates, operations=["nonexistent"]))
        self.assertEqual(["Miller"], [item["name"] for item in
                                     select_candidates(candidates, query="name-indexed")])

    def test_cli_output_is_deterministic_and_parseable(self):
        cmd = [sys.executable, "-m", "m3.catalogue", "--category",
               "structured-search", "--format", "jsonl"]
        def output():
            return subprocess.check_output(cmd, cwd=ROOT, text=True)
        first = output()
        self.assertEqual(first, output())
        names = [json.loads(line)["name"] for line in first.splitlines()]
        self.assertEqual(["csvkit", "csvtk", "Miller", "xsv"], names)

    def test_invalid_overlay_and_unbacked_claims_are_rejected(self):
        project = '[known]\nurl = "https://example.test"\ntags = ["csv"]\n'
        base = ('schema_version = 1\n[donors.{name}]\n'
                'problem_categories = ["delimited-records"]\n'
                'operations = ["join"]\n'
                'review_status = "{review}"\n'
                'license_status = "{license}"\n'
                'benchmark_status = "{benchmark}"\n'
                'implementation_status = "{implementation}"\n')
        def overlay(**changes):
            data = dict(name="known", review="candidate", license="unverified",
                        benchmark="not-run", implementation="not-evaluated")
            data.update(changes)
            return base.format(**data)
        with tempfile.TemporaryDirectory() as directory:
            projects = Path(directory) / "projects.toml"
            donors = Path(directory) / "donors.toml"
            projects.write_text(project, encoding="utf-8")
            for bad in (
                overlay(name="missing"),
                overlay(review="reviewed"),
                overlay(license="compatible"),
                overlay(benchmark="benchmarked"),
                overlay(implementation="jni-implemented"),
                overlay().replace('["join"]', '["join", "join"]'),
                overlay().replace('schema_version = 1', 'schema_version = 2'),
            ):
                with self.subTest(bad=bad):
                    donors.write_text(bad, encoding="utf-8")
                    with self.assertRaises(CatalogueError):
                        load_candidates(projects, donors)


if __name__ == "__main__":
    unittest.main()
