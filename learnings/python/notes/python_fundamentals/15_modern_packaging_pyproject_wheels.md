# Modern Python Packaging - `pyproject.toml`, Wheels, and Publishing

Packaging turns source code into an installable, versioned artifact. A package directory used by imports is different from a distribution published to a package index.

## 1. Vocabulary

- import package: a directory/module imported in Python, such as `course_tools`;
- distribution: installable project identified by metadata, such as `course-tools`;
- source distribution (`sdist`): source archive rebuilt by the installer;
- wheel: built installation archive;
- build backend: tool that creates distributions;
- build frontend: command such as `python -m build` that calls the backend;
- package index: repository serving distributions.

Distribution names can contain hyphens while import names normally use underscores.

## 2. Recommended Project Layout

```text
course-tools/
|-- pyproject.toml
|-- README.md
|-- LICENSE
|-- src/
|   `-- course_tools/
|       |-- __init__.py
|       |-- cli.py
|       `-- parser.py
`-- tests/
    `-- test_parser.py
```

The `src` layout prevents tests from accidentally importing the repository directory instead of the installed package.

## 3. Complete `pyproject.toml`

This example uses setuptools as one well-supported backend. Other standards-compliant backends are valid choices.

```toml
[build-system]
requires = ["setuptools>=75", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "course-tools"
version = "0.1.0"
description = "Strict course-file utilities"
readme = "README.md"
requires-python = ">=3.12"
license = "MIT"
authors = [
  { name = "Course Tools Team", email = "engineering@example.com" },
]
classifiers = [
  "Programming Language :: Python :: 3",
  "Programming Language :: Python :: 3.12",
  "Typing :: Typed",
]
dependencies = []

[project.optional-dependencies]
dev = [
  "bandit>=1.7",
  "build>=1.2",
  "mypy>=1.11",
  "pytest>=8.3",
  "ruff>=0.8",
  "twine>=5.1",
]

[project.scripts]
course-tools = "course_tools.cli:main"

[project.urls]
Documentation = "https://example.com/course-tools/docs"
Repository = "https://example.com/course-tools/repository"

[tool.setuptools.packages.find]
where = ["src"]

[tool.setuptools.package-data]
course_tools = ["py.typed"]
```

Use real project URLs and contact data. Keep runtime dependencies separate from development tools.

## 4. Public Package API

`src/course_tools/__init__.py`:

```python
from course_tools.parser import Course, parse_course

__all__ = ["Course", "parse_course"]
```

Re-export only deliberate public API. Internal file layout can then evolve without forcing consumers to import private modules.

## 5. Strict Domain Parser

`src/course_tools/parser.py`:

```python
from dataclasses import dataclass
from typing import TypedDict


class CoursePayload(TypedDict):
    course_id: str
    title: str


@dataclass(frozen=True, slots=True)
class Course:
    course_id: str
    title: str


def parse_course(payload: CoursePayload) -> Course:
    course_id = payload["course_id"]
    title = payload["title"]

    if not course_id:
        raise ValueError("course_id must not be empty")
    if not title:
        raise ValueError("title must not be empty")
    if course_id.strip() != course_id:
        raise ValueError("course_id must not contain surrounding whitespace")

    return Course(course_id=course_id, title=title)
```

The function validates rather than trimming or coercing values. A JSON boundary must first verify that the external mapping has exactly the expected keys and types; `TypedDict` alone is static documentation.

## 6. Console Entry Point

`src/course_tools/cli.py`:

```python
import argparse
from collections.abc import Sequence


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="course-tools")
    parser.add_argument("course_id")
    return parser


def main(arguments: Sequence[str] | None = None) -> int:
    options = build_parser().parse_args(arguments)
    print(options.course_id)
    return 0
```

After installation:

```powershell
course-tools python
```

Output:

```text
python
```

Returning an integer makes CLI behavior testable. The generated launcher converts it into a process exit status.

## 7. Typed-Package Marker

Create an empty file:

```text
src/course_tools/py.typed
```

Including `py.typed` tells type checkers that an installed distribution provides inline type information. It does not prove the annotations are complete; run strict type checks.

## 8. Tests Import the Installed Package

`tests/test_parser.py`:

```python
import pytest

from course_tools import Course, parse_course


def test_parse_course_returns_domain_value() -> None:
    result = parse_course({"course_id": "python", "title": "Python"})

    assert result == Course(course_id="python", title="Python")


def test_parse_course_rejects_padded_id() -> None:
    with pytest.raises(ValueError, match="surrounding whitespace"):
        parse_course({"course_id": " python ", "title": "Python"})
```

Install the project before testing so imports reflect the built package layout.

## 9. Create an Isolated Development Environment

```powershell
py -3.12 -m venv .venv
.venv\Scripts\python -m pip install --upgrade pip
.venv\Scripts\python -m pip install --editable ".[dev]"
```

Editable installation is for development. Release testing must install the built wheel into a clean environment.

## 10. Build Artifacts

```powershell
.venv\Scripts\python -m build
```

Expected artifacts:

```text
dist/
|-- course_tools-0.1.0-py3-none-any.whl
`-- course_tools-0.1.0.tar.gz
```

`py3-none-any` means this pure-Python wheel is not tied to one CPython ABI or platform. Native extensions produce platform-specific tags.

## 11. Inspect and Check the Build

```powershell
.venv\Scripts\python -m twine check dist\*
.venv\Scripts\python -m zipfile --list dist\course_tools-0.1.0-py3-none-any.whl
```

Check that the wheel contains:

- expected modules;
- metadata;
- license files;
- `py.typed` when promised;
- required package data;
- no secrets, local caches, tests, or unrelated files unless intentionally shipped.

## 12. Test the Wheel, Not Only the Source Tree

```powershell
py -3.12 -m venv .wheel-venv
.wheel-venv\Scripts\python -m pip install dist\course_tools-0.1.0-py3-none-any.whl
.wheel-venv\Scripts\course-tools python
.wheel-venv\Scripts\python -c "from course_tools import Course; print(Course.__name__)"
```

Output:

```text
python
Course
```

This catches missing package files and undeclared dependencies hidden by the developer environment.

## 13. Dependencies and Constraints

For a reusable library:

- declare the minimum compatible range your tests support;
- avoid unnecessary upper bounds that block security upgrades;
- keep optional features in extras;
- do not place test/build tools in runtime dependencies.

For an application:

- resolve and lock the complete environment with the chosen workflow;
- review dependency updates;
- deploy the tested lock/artifact;
- keep platform markers explicit.

A library dependency declaration and an application lock file solve different problems.

## 14. Environment Markers

```toml
dependencies = [
  "importlib-resources>=6.4; python_version < '3.12'",
  "colorama>=0.4.6; platform_system == 'Windows'",
]
```

Use markers only for a real platform/version distinction. Test every branch in CI.

## 15. Package Data

Use `importlib.resources` to read installed package data:

```python
from importlib.resources import files


def default_schema() -> str:
    resource = files("course_tools").joinpath("schemas/course.json")
    return resource.read_text(encoding="utf-8")
```

Do not build paths relative to `__file__` when the resource API expresses the installation contract better.

Never package secrets. Distribution artifacts may be publicly downloadable and cached indefinitely.

## 16. Namespace Packages

Namespace packages let multiple distributions contribute subpackages under one top-level namespace. Use them only when separate ownership and release boundaries truly require it. They add discovery and packaging complexity.

An ordinary package with `__init__.py` is simpler for most projects.

## 17. Versioning

Choose one authoritative version source:

- static version in `pyproject.toml` updated by release automation;
- dynamic version read from reviewed version-control metadata;
- dedicated version module used by the backend.

Avoid importing the package during build merely to discover its version; imports can require dependencies or trigger side effects.

Follow semantic versioning when the project promises it, and document what the public API includes.

## 18. Reproducible Builds

- build from a clean version-control checkout;
- isolate build dependencies;
- record the source revision and toolchain;
- avoid timestamps or machine paths in generated content where possible;
- generate deterministic files;
- compare artifact contents across rebuilds;
- sign or attest artifacts according to organizational policy.

## 19. Publishing Safely

Recommended release flow:

```text
tag reviewed commit -> CI tests -> isolated build -> artifact inspection
                    -> clean-wheel tests -> trusted publishing -> verify index
```

Prefer package-index trusted publishing through short-lived CI identity instead of storing a long-lived API token.

Never print credentials or embed them in repository configuration. Use a staging index before the production index when the release process is new.

## 20. Supply-Chain Checks

- audit known dependency vulnerabilities;
- review licenses and provenance;
- inspect new build backends and plugins;
- minimize code executed during builds;
- protect release workflows and environments;
- generate an SBOM or provenance attestation when policy requires it;
- verify the uploaded filename, hash, metadata, and install behavior.

Build backends execute code. Treat build dependencies as a security boundary.

## 21. Common Packaging Failures

- tests pass only because the repository root is importable;
- a package or data file is absent from the wheel;
- runtime dependency is installed globally but undeclared;
- build imports the application and triggers side effects;
- distribution and import names are confused;
- version exists in several files and drifts;
- local compiler artifact is uploaded without a clean test;
- credentials are stored in `pyproject.toml` or shell history;
- editable install behavior is assumed to match a wheel.

## 22. Release Checklist

```powershell
python -m ruff format --check .
python -m ruff check .
python -m mypy
python -m pytest
python -m bandit -r src
python -m build
python -m twine check dist\*
```

Then install each wheel into a clean supported environment and run smoke/integration tests.

## Final Rules

- use `pyproject.toml` as the packaging and tool-configuration center;
- use a `src` layout for reliable import testing;
- separate runtime and development dependencies;
- expose console commands through entry points;
- include `py.typed` when publishing inline types;
- build both sdist and wheel when source distribution is supported;
- inspect and clean-install artifacts before publishing;
- define one version source;
- build in isolated CI;
- publish with short-lived trusted identity and verify the uploaded artifact.
