# Dunder Methods and Object Lifecycle Mastery

## 1) Why Dunder Methods Matter

Dunder methods define object behavior in Python syntax:
- printing
- equality
- hashing
- ordering
- iteration
- context manager behavior

## 2) `__repr__` vs `__str__`

- `__repr__`: unambiguous developer representation.
- `__str__`: user-friendly display.

## 3) Equality and Hashing Contracts

If objects are dictionary/set keys:
- `__eq__` and `__hash__` must align.
- mutable fields in hash logic are dangerous.

## 4) Ordering Methods

Define ordering only when there is a meaningful domain ordering.
Otherwise rely on explicit `key=` functions in sorting.

## 5) Callable Objects

`__call__` can turn objects into stateful callables.
Useful for configurable policies and command-style objects.

## 6) Container-Like Objects

For custom collection classes:
- `__len__`
- `__iter__`
- `__contains__`
- `__getitem__`

Implement only what semantics can guarantee correctly.

## 7) Context Manager Methods

- `__enter__`
- `__exit__`

Use for deterministic resource management in class-based APIs.

## 8) Initialization Flow

Lifecycle basics:
1. `__new__` creates instance (rarely overridden).
2. `__init__` initializes instance state.
3. validation/invariants must hold after init.

## 9) `__slots__` Tradeoff

Benefits:
- reduced memory usage
- prevents accidental dynamic attributes

Costs:
- less flexibility
- may complicate some frameworks/introspection scenarios

## 10) Interview Questions

1. Why `__repr__` should be developer-friendly?
2. Why mutable hashed objects are risky?
3. When to use `__slots__`?
4. Difference between `__new__` and `__init__`?
