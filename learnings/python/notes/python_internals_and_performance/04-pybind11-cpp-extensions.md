# pybind11 C++ Extensions

pybind11 exposes C++ functions and types as Python extension modules with a small header-only binding API. Use it when a measured kernel or an existing C++ library justifies a native boundary.

## 1. Boundary Mental Model

```text
Python object -> pybind11 validation/conversion -> C++ value or borrowed buffer
              -> native work -> explicit result conversion -> Python object
```

The boundary has cost and ownership rules. A fast C++ loop can still lose if each call copies or converts large inputs.

## 2. Complete Project

This module accepts only a one-dimensional, C-contiguous NumPy `float64` array. It does not silently convert a list or another dtype.

```text
pybind11-stats/
|-- pyproject.toml
|-- CMakeLists.txt
|-- src/
|   `-- native_stats.cpp
`-- tests/
    `-- test_native_stats.py
```

## 3. `pyproject.toml`

```toml
[build-system]
requires = [
  "scikit-build-core>=0.10",
  "pybind11>=2.13",
]
build-backend = "scikit_build_core.build"

[project]
name = "pybind11-stats-example"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = ["numpy>=2.0"]
```

The build backend drives CMake in an isolated environment. Review and constrain tool versions according to application or library release policy.

## 4. `CMakeLists.txt`

```cmake
cmake_minimum_required(VERSION 3.20)
project(native_stats LANGUAGES CXX)

find_package(pybind11 CONFIG REQUIRED)

pybind11_add_module(native_stats src/native_stats.cpp)
target_compile_features(native_stats PRIVATE cxx_std_20)

install(TARGETS native_stats
    LIBRARY DESTINATION .
    RUNTIME DESTINATION .
)
```

The `RUNTIME` destination matters for extension-module placement on Windows; `LIBRARY` covers platforms that classify the module as a shared library.

## 5. `src/native_stats.cpp`

```cpp
#include <cstddef>
#include <stdexcept>

#include <pybind11/numpy.h>
#include <pybind11/pybind11.h>

namespace py = pybind11;

double mean(py::array_t<double, py::array::c_style> values) {
    if (values.ndim() != 1) {
        throw std::invalid_argument("values must be one-dimensional");
    }
    if (values.size() == 0) {
        throw std::invalid_argument("values must not be empty");
    }

    const auto view = values.unchecked<1>();
    double total = 0.0;

    {
        py::gil_scoped_release release;
        for (py::ssize_t index = 0; index < view.shape(0); ++index) {
            total += view(index);
        }
     }

    return total / static_cast<double>(values.size());
}

PYBIND11_MODULE(native_stats, module) {
    module.doc() = "Strict native statistics example";
    module.def(
        "mean",
        &mean,
        py::arg("values").noconvert(),
        "Return the arithmetic mean of a C-contiguous float64 array."
    );
}
```

Important details:

- `py::array_t<double, py::array::c_style>` requires float64 C-contiguous storage;
- `.noconvert()` rejects implicit argument conversion;
- dimension and empty checks happen before accessing the buffer;
- `unchecked<1>()` removes per-access dimension checking only after validation;
- the GIL is released around the C++ loop;
- the array argument remains alive for the complete call;
- C++ `std::invalid_argument` becomes Python `ValueError` through pybind11.

## 6. `tests/test_native_stats.py`

```python
import numpy as np
import pytest

import native_stats


def test_mean_returns_expected_value() -> None:
    values = np.array([2.0, 4.0, 6.0], dtype=np.float64)

    assert native_stats.mean(values) == 4.0


def test_mean_rejects_empty_array() -> None:
    values = np.array([], dtype=np.float64)

    with pytest.raises(ValueError, match="must not be empty"):
        native_stats.mean(values)


def test_mean_rejects_wrong_dtype_without_converting() -> None:
    values = np.array([2, 4, 6], dtype=np.int64)

    with pytest.raises(TypeError):
        native_stats.mean(values)
```

The third test proves the boundary does not hide a dtype conversion.

## 7. Build and Test

```powershell
py -3.12 -m venv .venv
.venv\Scripts\python -m pip install --upgrade pip
.venv\Scripts\python -m pip install build pytest
.venv\Scripts\python -m build
.venv\Scripts\python -m pip install --force-reinstall (Get-ChildItem dist\*.whl | Select-Object -First 1)
.venv\Scripts\python -m pytest
```

You need CMake and a supported C++ compiler. Compiler and Python architecture must match.

## 8. Use It

```python
import numpy as np

import native_stats

values = np.array([10.0, 20.0, 30.0], dtype=np.float64)
print(native_stats.mean(values))
```

Output:

```text
20.0
```

## 9. Copy Versus View

Binding `std::vector<double>` is convenient but normally creates a C++ vector from a Python sequence. For a large numeric kernel, the copy can dominate.

A NumPy array binding can borrow an existing compatible buffer. The stricter API makes layout requirements visible to the caller.

Choose deliberately:

- value conversion for small configuration-like data;
- borrowed buffer for large numeric arrays;
- owned native object when C++ must retain state;
- copied result when ownership must transfer safely.

## 10. GIL Rules

Release the GIL only after all Python validation and object access needed by the native region is complete.

While released, do not:

- create or destroy Python-owning wrappers whose destructor touches Python;
- call Python functions;
- raise a Python exception directly;
- access Python containers or attributes;
- mutate shared native state without synchronization.

Reacquire with `py::gil_scoped_acquire` only at a documented callback boundary. Avoid frequent GIL transitions inside a tight loop.

## 11. C++ Object Ownership

When binding classes, define who owns the C++ object.

```cpp
class CourseIndex {
public:
    explicit CourseIndex(std::size_t capacity) : capacity_(capacity) {
        if (capacity == 0) {
            throw std::invalid_argument("capacity must be positive");
        }
    }

    [[nodiscard]] std::size_t capacity() const noexcept {
        return capacity_;
    }

private:
    std::size_t capacity_;
};
```

```cpp
py::class_<CourseIndex>(module, "CourseIndex")
    .def(py::init<std::size_t>())
    .def_property_readonly("capacity", &CourseIndex::capacity);
```

The default holder owns the C++ instance with `std::unique_ptr`. Use shared ownership only when the actual C++ design requires it.

## 12. Return-Value Policies

Returning pointers or references requires a lifetime policy. A reference to a child member must not outlive its parent.

Prefer returning values for small data. When borrowing is required, choose and test an explicit pybind11 return-value policy such as `reference_internal`. Incorrect policies can cause leaks, dangling references, or double deletion.

## 13. Exceptions

pybind11 translates common standard exceptions. Register a custom exception for a stable domain-specific C++ error:

```cpp
class DuplicateCourseError : public std::runtime_error {
public:
    using std::runtime_error::runtime_error;
};

py::register_exception<DuplicateCourseError>(module, "DuplicateCourseError");
```

Do not allow an arbitrary C++ exception to cross a C ABI boundary. At Python/pybind11 boundaries, verify how each exception maps and ensure messages do not expose secrets.

## 14. Callbacks into Python

If C++ stores a Python callback:

- a `py::object` reference must keep it alive;
- every invocation needs the GIL;
- shutdown must prevent callbacks after interpreter finalization;
- background-thread exceptions need an explicit reporting path;
- reference cycles between Python and C++ must be considered.

Callbacks are a lifetime and concurrency feature, not merely a function pointer.

## 15. Native Safety

C++ extension bugs can crash or corrupt the complete Python process. Use:

- compiler warnings treated as errors in CI;
- address/undefined/thread sanitizers on supported builds;
- bounds and dimension validation;
- fuzzing for parsers and binary boundaries;
- small reviewed native surfaces;
- deterministic ownership;
- tests under repeated import, use, and interpreter shutdown.

## 16. Stable ABI and Wheel Matrix

Compiled modules are typically specific to a Python ABI, OS, CPU architecture, and runtime library environment. Decide supported targets explicitly and build each wheel in clean CI.

The limited Python API can reduce wheel count for suitable extensions, but not every pybind11 feature or dependency is compatible with that choice. Adopt it only after verifying the complete module.

## 17. Benchmark the Boundary

Measure:

- Python-to-C++ argument conversion;
- native execution;
- result conversion;
- allocation and peak memory;
- GIL contention under intended concurrency;
- small and large input break-even points.

Keep a pure-Python reference for correctness comparisons.

## Final Rules

- use pybind11 for measured native work or existing C++ integration;
- make accepted dtype, shape, layout, and ownership explicit;
- reject invalid input instead of silently converting it;
- release the GIL only around Python-free work;
- choose return-value and holder policies from real ownership;
- test exception, callback, shutdown, and lifetime behavior;
- run native sanitizers and build a verified wheel matrix;
- include boundary cost in every performance claim.

