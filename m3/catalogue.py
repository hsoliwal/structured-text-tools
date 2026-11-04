"""Validate and search M3 donor candidates without changing the upstream catalogue.

Only explicit catalogue descriptions support candidate classification. A candidate
is not a license approval, benchmark result, or Java/JNI implementation.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any, Iterable

try:
    import tomllib
except ModuleNotFoundError:  # Python 3.8-3.10; installed for the renderer too.
    import tomli as tomllib  # type: ignore[no-redef]


ROOT = Path(__file__).resolve().parents[1]
PROJECTS = ROOT / "data" / "projects.toml"
DONORS = ROOT / "m3" / "donors.toml"

_SLUG = re.compile(r"^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$")
_REVIEW = {"candidate", "reviewed", "rejected"}
_LICENSE = {"unverified", "compatible", "incompatible"}
_BENCHMARK = {"not-run", "benchmarked"}
_IMPLEMENTATION = {
    "not-evaluated", "java-candidate", "jni-candidate",
    "java-implemented", "jni-implemented",
}
_REQUIRED = {
    "problem_categories", "operations", "review_status", "license_status",
    "benchmark_status", "implementation_status",
}
_OPTIONAL = {
    "review_evidence_url", "license_spdx", "license_evidence_url",
    "benchmark_evidence_url", "recipe_id", "test_evidence_url",
}


class CatalogueError(ValueError):
    """Raised when M3 metadata cannot be safely interpreted."""


def _read_toml(path: Path) -> dict[str, Any]:
    with path.open("rb") as source:
        return tomllib.load(source)


def _slugs(value: Any, field: str, name: str) -> list[str]:
    if (not isinstance(value, list) or not value
            or any(not isinstance(item, str) or not _SLUG.fullmatch(item)
                   for item in value)
            or len(set(value)) != len(value)):
        raise CatalogueError(f"{name}: {field} must contain unique nonempty slugs")
    return value


def _evidence(record: dict[str, Any], field: str, name: str) -> None:
    value = record.get(field)
    if not isinstance(value, str) or not value.strip():
        raise CatalogueError(f"{name}: {field} is required for this status")
    if field.endswith("_url") and not value.startswith("https://"):
        raise CatalogueError(f"{name}: {field} must be an https URL")


def _validate_donor(name: str, record: Any) -> None:
    if not isinstance(record, dict):
        raise CatalogueError(f"{name}: donor metadata must be a table")
    missing = _REQUIRED - record.keys()
    unknown = record.keys() - _REQUIRED - _OPTIONAL
    if missing or unknown:
        raise CatalogueError(
            f"{name}: missing {sorted(missing)}; unsupported {sorted(unknown)}")

    _slugs(record["problem_categories"], "problem_categories", name)
    _slugs(record["operations"], "operations", name)
    for field, choices in (
        ("review_status", _REVIEW),
        ("license_status", _LICENSE),
        ("benchmark_status", _BENCHMARK),
        ("implementation_status", _IMPLEMENTATION),
    ):
        if not isinstance(record[field], str) or record[field] not in choices:
            raise CatalogueError(f"{name}: invalid {field}: {record[field]!r}")

    # An affirmative claim is invalid unless its evidence is recorded.
    if record["review_status"] == "reviewed":
        _evidence(record, "review_evidence_url", name)
    if record["license_status"] != "unverified":
        _evidence(record, "license_spdx", name)
        _evidence(record, "license_evidence_url", name)
    if record["benchmark_status"] == "benchmarked":
        _evidence(record, "benchmark_evidence_url", name)
    if record["implementation_status"].endswith("-implemented"):
        _evidence(record, "recipe_id", name)
        _evidence(record, "test_evidence_url", name)

    for key in _OPTIONAL & record.keys():
        _evidence(record, key, name)


def load_candidates(
    projects_path: Path = PROJECTS, donors_path: Path = DONORS
) -> list[dict[str, Any]]:
    """Return validated candidates in original project order, without mutation."""
    projects = _read_toml(projects_path)
    overlay = _read_toml(donors_path)
    if set(overlay) != {"schema_version", "donors"} or overlay["schema_version"] != 1:
        raise CatalogueError("M3 donor metadata requires schema_version = 1")
    donors = overlay["donors"]
    if not isinstance(donors, dict):
        raise CatalogueError("donors must be a TOML table")
    missing_projects = donors.keys() - projects.keys()
    if missing_projects:
        raise CatalogueError(f"Unknown projects: {sorted(missing_projects)}")

    result: list[dict[str, Any]] = []
    for name, project in projects.items():
        if name not in donors:
            continue
        _validate_donor(name, donors[name])
        if (not isinstance(project, dict) or not isinstance(project.get("url"), str)
                or not isinstance(project.get("tags"), list)
                or any(not isinstance(tag, str) for tag in project["tags"])):
            raise CatalogueError(f"{name}: invalid upstream catalogue record")
        donor = donors[name]
        result.append({
            "name": name,
            "url": project["url"],
            "description": project.get("descr", ""),
            "tags": list(project["tags"]),
            **{key: list(donor[key]) for key in ("problem_categories", "operations")},
            **{key: donor[key] for key in (
                "review_status", "license_status", "benchmark_status",
                "implementation_status")},
            **{key: donor[key] for key in sorted(_OPTIONAL & donor.keys())},
        })
    return result


def select_candidates(
    candidates: Iterable[dict[str, Any]], *, tags: Iterable[str] = (),
    categories: Iterable[str] = (), operations: Iterable[str] = (),
    query: str = "",
) -> list[dict[str, Any]]:
    """Apply intersection filters while retaining catalogue source order."""
    required_tags = set(tags)
    required_categories = set(categories)
    required_operations = set(operations)
    needle = query.casefold()
    return [candidate for candidate in candidates
            if required_tags.issubset(candidate["tags"])
            and required_categories.issubset(candidate["problem_categories"])
            and required_operations.issubset(candidate["operations"])
            and (not needle or needle in (
                candidate["name"] + " " + candidate["description"]
            ).casefold())]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tag", action="append", default=[], help="Require a source tag")
    parser.add_argument("--category", action="append", default=[], help="Require an M3 problem category")
    parser.add_argument("--operation", action="append", default=[], help="Require a donor operation")
    parser.add_argument("--query", default="", help="Search project name and description")
    parser.add_argument("--format", choices=("json", "jsonl"), default="json")
    parser.add_argument("--check", action="store_true", help="Validate without outputting records")
    args = parser.parse_args(argv)

    try:
        candidates = load_candidates()
    except (CatalogueError, OSError, tomllib.TOMLDecodeError) as exc:
        parser.exit(2, f"M3 donor catalogue error: {exc}\n")
    if args.check:
        print(f"Validated {len(candidates)} M3 donor candidates")
        return 0

    selected = select_candidates(
        candidates, tags=args.tag, categories=args.category,
        operations=args.operation, query=args.query)
    if args.format == "jsonl":
        for candidate in selected:
            print(json.dumps(candidate, ensure_ascii=False, sort_keys=True))
    else:
        print(json.dumps(selected, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
