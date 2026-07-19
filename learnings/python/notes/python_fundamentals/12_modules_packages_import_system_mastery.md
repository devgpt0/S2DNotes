# Modules, Packages, and Import System Mastery

## 1) Module and Package Basics

- Module: single `.py` file.
- Package: folder containing modules (usually with `__init__.py`).

Clean packaging improves readability, testing, and deployment.

## 2) Import Execution Model

Import is executable:
1. Check `sys.modules` cache.
2. If missing, load and execute module top-level code.
3. Cache module object.
4. Future imports reuse cached module.

## 3) Top-Level Side Effects

Avoid heavy work at import time:
- DB connections
- network calls
- expensive computation

Put runtime logic behind functions or `if __name__ == "__main__":`.

## 4) Absolute vs Relative Imports

Prefer absolute imports for clarity in app code.
Use relative imports mainly inside package internals when appropriate.

## 5) Circular Import Failures

Circular imports often signal poor module boundaries.

Fix strategies:
- move shared types/constants to separate module
- defer import inside function in limited cases
- invert dependencies via abstraction interfaces

## 6) Package Entry Points

Standard script entry:

```python
def main() -> None:
    print("run app")


if __name__ == "__main__":
    main()
```

## 7) API Surface Design with `__init__.py`

Expose stable public API intentionally:
- re-export selected names
- keep internals private

## 8) Import Debugging Checklist

1. Verify module path.
2. Check naming conflicts with stdlib modules.
3. Check circular dependencies.
4. Validate package structure and `__init__.py` expectations.

## 9) Interview Questions

1. Why does import run top-level code?
2. What is `sys.modules` and why is it important?
3. How do you resolve circular imports safely?
4. Absolute vs relative import tradeoffs?

## 10) Production Checklist

1. No expensive import-time side effects.
2. Clear package boundaries.
3. Public API exported intentionally.
4. Module names do not shadow stdlib names.
