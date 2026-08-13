# pybind11 C++ Extensions

## 1. Use pybind11 for a justified C++ boundary

pybind11 exposes C++ functions and types to Python. It is a strong fit for an
existing C++ library or a measured computation that genuinely needs C++.

Keep the binding layer narrow: validate the public contract, translate errors,
and delegate to ordinary C++ code.

## 2. Minimal modern project

```text
fastmath/
|-- CMakeLists.txt
|-- pyproject.toml
|-- src/
|   `-- bindings.cpp
`-- fastmath/
    `-- __init__.py
```

`pyproject.toml`:

```toml
[build-system]
requires = ["scikit-build-core", "pybind11"]
build-backend = "scikit_build_core.build"

[project]
name = "fastmath"
version = "0.1.0"
requires-python = ">=3.12"
```

`CMakeLists.txt`:

```cmake
cmake_minimum_required(VERSION 3.15)
project(fastmath LANGUAGES CXX)

find_package(pybind11 CONFIG REQUIRED)
pybind11_add_module(_fastmath src/bindings.cpp)
target_compile_features(_fastmath PRIVATE cxx_std_17)
install(TARGETS _fastmath DESTINATION fastmath)
```

`src/bindings.cpp`:

```cpp
#include <stdexcept>

#include <pybind11/pybind11.h>

namespace py = pybind11;

int square_non_negative(int value) {
    if (value < 0) {
        throw std::invalid_argument("value must be non-negative");
    }
    return value * value;
}

PYBIND11_MODULE(_fastmath, module) {
    module.def("square_non_negative", &square_non_negative, py::arg("value"));
}
```

`fastmath/__init__.py`:

```python
from ._fastmath import square_non_negative

__all__ = ["square_non_negative"]
```

Build and install:

```bash
python -m pip install .
```

Compiler output and wheel names vary by platform. A successful build installs
the package and its native module.

After installation:

```python
from fastmath import square_non_negative

print(square_non_negative(5))

try:
    square_non_negative(-1)
except ValueError as error:
    print(type(error).__name__, str(error))
```

Output:

```text
25
ValueError value must be non-negative
```

This example is contextual; pybind11 maps `std::invalid_argument` to
`ValueError` after the extension has been built.

## 3. Make ownership explicit

Python and C++ use different lifetime models. Prefer copied values or clear
smart-pointer ownership. Use a return-value policy only after establishing who
owns the returned object and how long it remains valid.

Never return a Python view or reference to C++ memory that may already have been
destroyed.

## 4. Validate conversions and sizes

Automatic conversions are convenient but can copy containers or reject values
outside the C++ type's range. Treat Python input as external input:

- choose exact accepted Python and C++ types;
- reject invalid ranges explicitly;
- bound allocation sizes before constructing native buffers;
- avoid accepting arbitrary paths, URLs, or commands in native code;
- translate expected domain failures to specific Python exceptions.

## 5. Release the GIL only around independent C++ work

`py::gil_scoped_release` allows other Python threads to run while C++ executes.
The released region must not touch Python objects or unsafe shared C++ state.

```cpp
module.def("compute", &compute, py::call_guard<py::gil_scoped_release>());
```

Releasing the GIL does not make `compute` thread-safe.

## 6. Build and test rules

- Pin and test supported compilers, Python versions, ABIs, and platforms.
- Build wheels in clean environments and test the installed artifacts.
- Enable normal compiler warnings; use sanitizers in native test jobs.
- Test exception translation, ownership, boundary values, and concurrent calls.
- Benchmark conversion cost as well as the C++ computation.
- Keep business orchestration out of `bindings.cpp`.

## 7. Decision guide

| Situation | Choice |
| --- | --- |
| expose an existing C++ API | pybind11 |
| optimize Python-like numeric code | consider Cython first |
| ordinary application logic | Python |
| small operation with large conversion cost | keep data on one side of the boundary |
| no native build ownership | use a maintained dependency or keep Python |

## 8. Mental model

```text
Python contract -> thin binding -> tested C++ API -> explicit ownership
```
