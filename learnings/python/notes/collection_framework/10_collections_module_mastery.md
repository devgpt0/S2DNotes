# `collections` Module Mastery (Python)

This file covers high-impact stdlib collection types frequently required in interviews and production systems.

## 1) Why `collections` Exists

Built-ins (`list`, `dict`, `set`, `tuple`) are foundational.
`collections` adds specialized containers optimized for specific patterns:
- counting
- grouping
- queue/deque operations
- layered mappings
- ordered reordering workflows

## 2) `Counter` - Frequency Toolkit

```python
from collections import Counter

c = Counter("banana")
print(c)                 # Counter({'a': 3, 'n': 2, 'b': 1})
print(c.most_common(2))  # [('a', 3), ('n', 2)]
```

Core operations:
- `update(iterable_or_mapping)`
- `subtract(iterable_or_mapping)`
- arithmetic (`+`, `-`, `&`, `|`)
- `elements()` for expanded iterator

Use cases:
- log/event frequency
- text token counts
- inventory balance

## 3) `defaultdict` - Default Value on Missing Keys

```python
from collections import defaultdict

groups = defaultdict(list)
for dept, name in [("ENG", "Ana"), ("HR", "Raj"), ("ENG", "Mia")]:
    groups[dept].append(name)
print(groups)
```

Common factories:
- `int` for counters
- `list` for grouping
- `set` for unique grouping

Pitfall:
- default factory runs only on missing key access, not on `get()`.

## 4) `deque` - Double-Ended Queue

```python
from collections import deque

dq = deque([1, 2, 3])
dq.append(4)
dq.appendleft(0)
print(dq.popleft())  # 0
print(dq.pop())      # 4
```

Strength:
- O(1) append/pop from both ends.

Great for:
- queue processing
- sliding window
- BFS traversal

## 5) `ChainMap` - Layered Mapping View

```python
from collections import ChainMap

defaults = {"timeout": 30, "retries": 2}
env = {"timeout": 60}
cfg = ChainMap(env, defaults)
print(cfg["timeout"])  # 60
print(cfg["retries"])  # 2
```

Use case:
- config overlays (CLI > env > defaults).

## 6) `OrderedDict` - When Explicit Reordering Matters

Dict preserves insertion order in modern Python, but `OrderedDict` still offers:
- `move_to_end(key, last=True/False)`
- order-sensitive queue/cache style workflows

```python
from collections import OrderedDict

od = OrderedDict([("a", 1), ("b", 2), ("c", 3)])
od.move_to_end("a")
print(list(od.keys()))  # ['b', 'c', 'a']
```

## 7) `namedtuple` - Lightweight Named Records

```python
from collections import namedtuple

User = namedtuple("User", ["id", "name"])
u = User(1, "Ana")
print(u.id, u.name)
```

When to choose:
- immutable record
- low ceremony
- positional compatibility needed

## 8) `UserDict`, `UserList`, `UserString` for Safe Extension

If you need custom behavior, subclass wrapper types instead of raw built-ins.

```python
from collections import UserDict

class LowerKeyDict(UserDict):
    def __setitem__(self, key, value):
        super().__setitem__(str(key).lower(), value)
```

Why:
- avoids subtle pitfalls when overriding C-implemented built-in behaviors directly.

## 9) Missing Pitfalls and Best Practices

- Use `Counter` when counting logic appears; avoid manual verbose loops.
- Use `defaultdict` only when implicit key creation is acceptable.
- Do not use `deque` when heavy random indexing is required.
- For deterministic external output, convert/format explicitly.

## 10) Quick Selection Table

- counting: `Counter`
- grouping: `defaultdict(list/set)`
- FIFO/LIFO at both ends: `deque`
- layered config lookup: `ChainMap`
- explicit order-manipulation: `OrderedDict`
- immutable named record: `namedtuple`
- custom mapping/list/string containers: `UserDict/UserList/UserString`
