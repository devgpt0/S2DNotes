# PYTHON - MODULES, PACKAGES, AND IMPORTS

Modules organize Python code. Packages organize related modules. Importing executes and caches module code.

## 1. Module

A module is a Python file or another importable module object with its own namespace.

```python
import math

print(type(math).__name__)
print(math.sqrt(81))
print(math.__name__)
```

Output:

```text
module
9.0
math
```

Access module names with dot notation.

## 2. Package

A package is a module that can contain submodules and subpackages.

```python
import xml
import xml.etree

print(xml.__name__)
print(xml.etree.__name__)
print(hasattr(xml, "__path__"))
```

Output:

```text
xml
xml.etree
True
```

Traditional packages contain `__init__.py`. Namespace packages can span directories without it.

## 3. Module Namespace

Imported names live in the module's dictionary.

```python
import math

print("sqrt" in math.__dict__)
print(math.__dict__["sqrt"](16))
```

Output:

```text
True
4.0
```

Normal code should use `math.sqrt`; `__dict__` mainly helps inspection.

## 4. Import Executes Top-Level Code

The first import executes the module body.

```python
import importlib
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

with TemporaryDirectory() as directory:
    module_name = "lesson_module_example"
    Path(directory, f"{module_name}.py").write_text(
        'print("module loaded")\nvalue = 42\n',
        encoding="utf-8",
    )
    sys.path.insert(0, directory)
    try:
        module = importlib.import_module(module_name)
        print(module.value)
    finally:
        sys.path.remove(directory)
        sys.modules.pop(module_name, None)
```

Output:

```text
module loaded
42
```

Keep expensive work, network calls, and application startup out of module top level.

## 5. Import Cache

Python stores loaded modules in `sys.modules`. Later imports normally reuse the same object.

```python
import math
import sys

first = math
second = __import__("math")

print("math" in sys.modules)
print(first is second)
```

Output:

```text
True
True
```

## 6. Import Styles

`import module` keeps the source namespace visible.

```python
import statistics

print(statistics.mean([10, 20, 30]))
```

Output:

```text
20
```

`from module import name` binds selected names locally.

```python
from statistics import mean

print(mean([10, 20, 30]))
```

Output:

```text
20
```

Prefer `import module` when qualification improves clarity or prevents name collisions.

## 7. Import Aliases

`as` binds an imported object to another local name.

```python
import statistics as stats
from math import factorial as fact

print(stats.median([1, 3, 2]))
print(fact(5))
```

Output:

```text
2
120
```

Use conventional or genuinely clearer aliases.

## 8. Avoid Wildcard Imports

`from module import *` hides where names came from and can overwrite local names.

```python
from math import pi, tau

print(round(pi, 2))
print(round(tau, 2))
```

Output:

```text
3.14
6.28
```

Import explicit names instead.

## 9. `__name__` and the Main Guard

Directly executed code receives `__name__ == "__main__"`.

```python
def main():
    print("application started")


if __name__ == "__main__":
    main()
```

Output:

```text
application started
```

When imported, the guard prevents startup code from running.

## 10. Package Layout

A small `src`-layout package can look like this:

```text
project/
|-- pyproject.toml
|-- src/
|   `-- shop/
|       |-- __init__.py
|       |-- pricing.py
|       `-- reports.py
`-- tests/
```

Import through the package namespace:

```python
import xml.etree.ElementTree as element_tree

root = element_tree.fromstring("<course>Python</course>")
print(root.tag)
print(root.text)
```

Output:

```text
course
Python
```

## 11. Package `__init__.py`

`__init__.py` initializes a regular package and may expose a small public API.

Example package files:

```text
# pricing.py
def total(price, quantity):
    return price * quantity


# __init__.py
from .pricing import total
```

Consumer:

```python
# After installing the package:
# from shop import total

def total(price, quantity):
    return price * quantity


print(total(10, 3))
```

Output:

```text
30
```

Keep `__init__.py` light to avoid slow imports and circular dependencies.

## 12. Absolute and Relative Imports

Absolute imports start from the importable package name. Relative imports use leading dots inside a package.

```python
# Inside shop/reports.py:
# from shop.pricing import total  # absolute
# from .pricing import total      # relative

import importlib

module = importlib.import_module("xml.etree.ElementTree")
print(module.__name__)
```

Output:

```text
xml.etree.ElementTree
```

Prefer absolute imports for clarity across package boundaries. Use relative imports for nearby internal modules when the relationship is clear.

## 13. `__all__`

`__all__` declares names exported by wildcard import and documents intended public names.

```python
__all__ = ["calculate_total"]


def calculate_total(price, quantity):
    return price * quantity


def _internal_helper():
    return "internal"


print(__all__)
print(calculate_total(4, 5))
```

Output:

```text
['calculate_total']
20
```

It does not provide access control; underscore names are conventions.

## 14. Module Search Path

Python searches locations listed in `sys.path` through import finders.

```python
import sys

print(type(sys.path).__name__)
print(all(isinstance(entry, str) for entry in sys.path))
```

Output:

```text
list
True
```

Prefer installing packages over modifying `sys.path` in application code.

## 15. Dynamic Imports

Use `importlib.import_module()` when the module name is selected at runtime.

```python
import importlib

module = importlib.import_module("math")

print(module.factorial(5))
print(module.__name__)
```

Output:

```text
120
math
```

Validate externally supplied module names before importing them.

## 16. Circular Imports

A circular import occurs when modules depend on each other during initialization.

```text
orders.py imports payments.py
payments.py imports orders.py
```

One module may observe the other before all names exist.

Fix the dependency structure:

- move shared types or constants to a third module;
- depend on lower-level abstractions;
- move runtime startup into functions;
- use a local import only when delayed loading is genuinely required.

```python
dependencies = {
    "orders": ["contracts"],
    "payments": ["contracts"],
    "contracts": [],
}

print(dependencies["orders"])
print(dependencies["payments"])
```

Output:

```text
['contracts']
['contracts']
```

The shared module breaks the `orders <-> payments` cycle.

## 17. Module Shadowing

A local file can accidentally shadow an installed or standard-library module.

```python
import math

print(math.__name__)
print(hasattr(math, "sqrt"))
```

Output:

```text
math
True
```

Do not name local files `math.py`, `json.py`, `typing.py`, or after dependencies they should import.

## 18. Final Mental Model

For an import, ask:

1. What exact module name is requested?
2. Is it already in `sys.modules`?
3. Where will Python search?
4. What top-level code runs?
5. Does initialization create side effects or a dependency cycle?
6. Which names become part of the public API?

Remember:

- a module is an importable namespace;
- a package can contain modules;
- first import executes top-level code;
- later imports normally reuse the cache;
- the main guard separates reusable imports from application startup;
- clean dependency direction prevents circular imports.
