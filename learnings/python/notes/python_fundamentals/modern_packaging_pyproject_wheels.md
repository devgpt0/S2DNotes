# PYTHON - MODERN PACKAGING

Packaging turns a Python project into versioned, installable artifacts.

## 1. Import Package Versus Distribution

An import package is used by Python code. A distribution is installed by a package installer.

```text
Distribution name: example-shop
Import package:    shop

python -m pip install example-shop
```

```python
import shop

print(shop.__name__)
```

Output:

```text
shop
```

The distribution and import names may differ.

## 2. Recommended Project Layout

The `src` layout keeps importable code away from the repository root.

```text
example-shop/
|-- pyproject.toml
|-- README.md
|-- src/
|   `-- shop/
|       |-- __init__.py
|       |-- pricing.py
|       `-- cli.py
`-- tests/
    `-- test_pricing.py
```

Tests must install the project instead of accidentally importing local source files.

## 3. `pyproject.toml`

`pyproject.toml` stores build configuration and standardized project metadata.

```toml
[build-system]
requires = ["setuptools"]
build-backend = "setuptools.build_meta"

[project]
name = "example-shop"
version = "1.0.0"
description = "Small pricing utilities"
readme = "README.md"
requires-python = ">=3.12"
```

The build frontend creates an isolated environment and invokes the declared backend.

## 4. Project Metadata

Metadata identifies the release and helps installers choose compatible artifacts.

```toml
[project]
name = "example-shop"
version = "1.0.0"
description = "Small pricing utilities"
readme = "README.md"
requires-python = ">=3.12"
license = "MIT"
authors = [
  { name = "Example Team" },
]
classifiers = [
  "Programming Language :: Python :: 3",
]
```

Use the exact license expression and classifiers that apply to the project.

## 5. Runtime Dependencies

Declare packages required when the installed code runs.

```toml
[project]
dependencies = [
  "httpx>=0.27",
]
```

Do not declare standard-library modules. Keep runtime dependencies minimal and intentional.

## 6. Optional Dependencies

Extras group dependencies needed only for specific features or development tasks.

```toml
[project.optional-dependencies]
database = [
  "sqlalchemy>=2",
]
dev = [
  "build",
  "pyright",
  "ruff",
  "pytest",
]
```

Install an extra explicitly:

```text
python -m pip install ".[dev]"
```

## 7. Package Discovery with `src`

Tell the selected backend where import packages live.

```toml
[tool.setuptools.packages.find]
where = ["src"]
```

Backend-specific configuration belongs under that backend's documented table.

## 8. Public Package API

Expose stable public names deliberately from `__init__.py`.

```text
# src/shop/pricing.py
def total(price: int, quantity: int) -> int:
    return price * quantity
```

```text
# src/shop/__init__.py
from .pricing import total

__all__ = ["total"]
```

Consumer:

```python
from shop import total

print(total(10, 3))
```

Output:

```text
30
```

Keep package initialization lightweight and free of application startup work.

## 9. Console Scripts

An entry point creates an installed command without requiring executable module-level code.

```toml
[project.scripts]
shop = "shop.cli:main"
```

```text
# src/shop/cli.py
def main() -> int:
    print("shop started")
    return 0
```

After installation:

```text
shop
```

Output:

```text
shop started
```

The command wrapper calls `shop.cli.main` and uses its integer return value as the exit status.

## 10. Wheel

A wheel is a built installation artifact. Installation normally copies files without running a source build.

```text
example_shop-1.0.0-py3-none-any.whl
```

Name parts describe the distribution, version, Python compatibility, ABI, and platform.

## 11. Source Distribution

A source distribution contains source and metadata for a build frontend to build later.

```text
example_shop-1.0.0.tar.gz
```

Publish a source distribution only if it contains everything required to build the project.

## 12. Build Artifacts

Install the build frontend in the development environment, then build from a clean source tree.

```text
python -m pip install build
python -m build
```

Expected artifact types:

```text
dist/
|-- example_shop-1.0.0-py3-none-any.whl
`-- example_shop-1.0.0.tar.gz
```

Generated filenames depend on project metadata and compatibility tags.

## 13. Test the Built Wheel

Test the artifact users will install, not only an editable source tree.

```text
python -m venv .venv-wheel-test
python -m pip --python .venv-wheel-test install dist/example_shop-1.0.0-py3-none-any.whl
python -m pip --python .venv-wheel-test check
```

Then run a smoke test with that environment's Python:

```python
from shop import total

print(total(4, 5))
```

Output:

```text
20
```

This catches missing files and undeclared dependencies.

## 14. Editable Installation

Editable installation links development imports to the working source tree.

```text
python -m pip install -e ".[dev]"
```

Use it for local development. Do not treat it as proof that the built wheel is correct.

## 15. Package Data

Non-Python runtime files must be included explicitly.

```toml
[tool.setuptools.package-data]
shop = ["templates/*.txt"]
```

Read installed resources through `importlib.resources`, not repository-relative paths.

```python
from importlib.resources import files

template = files("shop").joinpath("templates/invoice.txt")
print(template.name)
```

Output:

```text
invoice.txt
```

## 16. Versioning

Every published artifact needs a valid, unique version.

```toml
[project]
version = "1.4.0"
```

A common release policy is:

| Change | Example version |
| --- | --- |
| backward-compatible fix | `1.4.1` |
| backward-compatible feature | `1.5.0` |
| incompatible public change | `2.0.0` |

Choose and document the project's actual compatibility policy.

## 17. Applications Versus Libraries

Libraries and deployed applications have different dependency goals.

| Project | Dependency approach |
| --- | --- |
| reusable library | declare compatible ranges |
| deployed application | use a tested lock or fully resolved environment |

Libraries should avoid unnecessarily exact transitive pins. Applications need reproducible deployments.

## 18. Release Safety

Before publishing:

1. run linting, type checks, tests, and security checks;
2. build wheel and source distribution;
3. inspect artifact contents;
4. install the wheel in a clean environment;
5. run tests or smoke checks against the installation;
6. verify name and version;
7. publish with short-lived or trusted credentials.

Never place tokens or repository credentials in `pyproject.toml`.

## 19. Common Mistakes

| Mistake | Result |
| --- | --- |
| confusing distribution and import names | incorrect install or import command |
| testing only from repository root | missing package files stay hidden |
| undeclared runtime dependency | clean installation fails |
| heavy work in `__init__.py` | slow or fragile imports |
| shipping secrets | credential exposure |
| publishing without clean-install testing | broken release |

## 20. Final Mental Model

```text
source + metadata
        |
        v
build backend
   |         |
   v         v
 wheel      sdist
   |
   v
clean install -> checks -> publish
```

Remember:

- `pyproject.toml` defines build and project metadata;
- an import package is not the same as a distribution;
- the `src` layout prevents accidental local imports;
- wheels are the primary install artifacts;
- release confidence comes from testing the built artifact.
