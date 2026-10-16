# SPDX-License-Identifier: CC-BY-4.0
"""Differential verification of the structured-text-tools catalogue tag precompute."""
import importlib.util
from pathlib import Path
import random
import sys
import unittest

import jinja2 as j2

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("structured_text_renderer", ROOT / "render-template.py")
assert SPEC is not None and SPEC.loader is not None
RENDERER = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = RENDERER
SPEC.loader.exec_module(RENDERER)


class TagIndexContractTest(unittest.TestCase):
    @staticmethod
    def originals(projects, tag):
        # Independent original algorithm: order-preserving scan and membership.
        return [project for project in projects if tag in project.tags]

    def test_exact_order_duplicates_and_mutable_result_contract(self):
        Project = RENDERER.Project
        projects = [
            Project("alpha", "https://example.test/1", ["csv", "csv", "json"]),
            Project("beta", "https://example.test/2", ["json", "yaml"]),
            Project("gamma", "https://example.test/3", []),
            Project("delta", "https://example.test/4", ["csv"]),
        ]
        index = RENDERER.group_projects_by_tag(projects)
        for tag in ("csv", "json", "yaml", "unknown", ""):
            self.assertEqual(self.originals(projects, tag), list(index.get(tag, ())))
        self.assertEqual(("alpha", "delta"),
                         tuple(project.name for project in index["csv"]))
        result = list(index["csv"])
        result.clear()
        self.assertEqual(2, len(index["csv"]))
        self.assertIs(index["csv"][0], projects[0])

    def test_seeded_comparisons_against_old_scanning_algorithm(self):
        rng = random.Random(20261015)
        Project = RENDERER.Project
        vocabulary = ["csv", "json", "xml", "toml", "yaml", "awk", "", "tést", "lexer"]
        for trial in range(32):
            projects = []
            for i in range(60):
                count = rng.randrange(0, 6)
                tags = [rng.choice(vocabulary) for _ in range(count)]
                projects.append(Project(f"p{i}", f"https://example.test/{i}", tags))
            index = RENDERER.group_projects_by_tag(projects)
            for tag in vocabulary + ["absent", "tést?"]:
                self.assertEqual(
                    self.originals(projects, tag), list(index.get(tag, ())),
                    f"category parity trial {trial} tag {tag}")

    def test_both_real_jinja_catalogues_render_byte_identically(self):
        for data_name, template_name in (
            ("data/projects.toml", "README.md.jinja"),
            ("data/sql-based.toml", "sql-based.md.jinja"),
        ):
            data = RENDERER.tomli.loads((ROOT / data_name).read_text())
            projects = [RENDERER.Project.from_dict(name, value)
                        for name, value in data.items()]
            precomputed = RENDERER.group_projects_by_tag(projects)
            settings = {
                "loader": j2.FileSystemLoader(str(ROOT)),
                "autoescape": j2.select_autoescape(),
                "lstrip_blocks": True,
                "trim_blocks": True,
            }
            def render(selector):
                env = j2.Environment(**settings)
                env.globals["projs_with_tag"] = selector
                return env.get_template(template_name).render(data)
            old_output = render(lambda tag: self.originals(projects, tag))
            new_output = render(lambda tag: list(precomputed.get(tag, ())))
            self.assertEqual(old_output.encode("utf-8"), new_output.encode("utf-8"))
            self.assertIn("# ", new_output)


if __name__ == "__main__":
    unittest.main()
