# `collections` Module Mastery
## 1. Core truth

`collections` is a standard-library module that adds specialized container types for common patterns.
Think of it like a toolbox with purpose-built tools: one tool for counting, one for queues, one for layered config, and so on.

```python
from collections import Counter

items = ["apple", "banana", "apple"]
print(Counter(items).most_common())
```

Output:

```text
[('apple', 2), ('banana', 1)]
```

`Counter` counts each item, and `most_common()` returns the items sorted by frequency.

## 2. Specialized containers

### Counting values with `Counter`

`Counter` is the easiest way to count repeated values.

```python
from collections import Counter

items = ["apple", "banana", "apple", "pear"]
counts = Counter(items)

print(counts["apple"])
print(counts.most_common(2))
```

Output:

```text
2
[('apple', 2), ('banana', 1)]
```

`Counter` stores each item as a key and its frequency as the value.

Practical takeaway: use `Counter` whenever you find yourself writing a manual counting loop.

### Grouping values with `defaultdict`

`defaultdict(list)` creates an empty list the first time a key appears.

```python
from collections import defaultdict

groups = defaultdict(list)
records = [("ENG", "Ana"), ("HR", "Raj"), ("ENG", "Mia")]

for dept, name in records:
    groups[dept].append(name)

print(groups["ENG"])
print(groups["HR"])
```

Output:

```text
['Ana', 'Mia']
['Raj']
```

The first time a department appears, `defaultdict` creates `[]`, then `append()` adds the names.

Practical takeaway: use `defaultdict` when missing keys should create a usable default automatically.

### Fast queue work with `deque`

`deque` is built for fast work at both ends.

```python
from collections import deque

queue = deque(["task-1", "task-2"])
queue.append("task-3")
first = queue.popleft()

print(first)
print(list(queue))
```

Output:

```text
task-1
['task-2', 'task-3']
```

`append()` adds to the right side, and `popleft()` removes from the left side.

Practical takeaway: use `deque` for queues, BFS, and sliding-window style work.

## 3. Container APIs

### `Counter`

- `update()` adds counts from new data.
- `subtract()` reduces counts.
- `most_common()` returns the highest-frequency items.

```python
from collections import Counter

counts = Counter("banana")
counts.update("band")
print(counts["a"])
print(counts.most_common(2))
```

Output:

```text
4
[('a', 4), ('n', 3)]
```

### `defaultdict`

- The factory runs only when a missing key is accessed with `[]`.
- `get()` does not create the key.

```python
from collections import defaultdict

groups = defaultdict(list)
print(groups.get("ENG"))
print("ENG" in groups)
print(groups["ENG"])
print("ENG" in groups)
```

Output:

```text
None
False
[]
True
```

### `deque`

- `append()` and `appendleft()` add items.
- `pop()` and `popleft()` remove items.
- `rotate()` shifts the queue.

```python
from collections import deque

dq = deque([1, 2, 3])
dq.rotate(1)
print(list(dq))
```

Output:

```text
[3, 1, 2]
```

### `ChainMap`

- Searches the first mapping first, then the next one, and so on.
- Useful for layered configuration.

```python
from collections import ChainMap

defaults = {"timeout": 30, "retries": 2}
env = {"timeout": 60}
cfg = ChainMap(env, defaults)

print(cfg["timeout"])
print(cfg["retries"])
```

Output:

```text
60
2
```

### `OrderedDict`

- `move_to_end()` moves a key to one side.

```python
from collections import OrderedDict

od = OrderedDict([("a", 1), ("b", 2), ("c", 3)])
od.move_to_end("a")
print(list(od.keys()))
```

Output:

```text
['b', 'c', 'a']
```

### `namedtuple`

- Creates a lightweight immutable record.
- Field names are easy to read.

```python
from collections import namedtuple

Point = namedtuple("Point", ["x", "y"])
p = Point(2, 5)

print(p.x + p.y)
print(p._asdict())
```

Output:

```text
7
{'x': 2, 'y': 5}
```

### `UserDict`

- Use it when you want custom dictionary behavior without fighting the built-in `dict` internals.

## 4. Practical container patterns

### Example 1: Count word frequency

```python
from collections import Counter

words = ["red", "blue", "red", "green", "blue", "red"]
counts = Counter(words)

print(counts["red"])
print(counts.most_common(2))
```

Output:

```text
3
[('red', 3), ('blue', 2)]
```

### Example 2: Group people by department

```python
from collections import defaultdict

people = [("ENG", "Ana"), ("HR", "Raj"), ("ENG", "Mia"), ("HR", "Zoe")]
departments = defaultdict(list)

for dept, name in people:
    departments[dept].append(name)

print(departments["ENG"])
print(departments["HR"])
```

Output:

```text
['Ana', 'Mia']
['Raj', 'Zoe']
```

### Example 3: Build a simple task queue

```python
from collections import deque

tasks = deque(["download", "parse"])
tasks.append("save")
print(tasks.popleft())
print(list(tasks))
```

Output:

```text
download
['parse', 'save']
```

- Use `Counter` for logs, tags, token counts, and inventory counts.
- Use `defaultdict(list)` for grouping records by category.
- Use `deque` for BFS, job queues, and sliding windows.
- Use `ChainMap` for config layering such as defaults, environment values, and user overrides.
- Use `OrderedDict` when key order must be manipulated intentionally.
- Use `namedtuple` for small read-only records returned from functions.

## 5. Container mistakes

### Mistake 1: Expecting `defaultdict.get()` to create a default

```python
from collections import defaultdict

groups = defaultdict(list)
print(groups.get("ENG"))
print("ENG" in groups)
print(groups["ENG"])
print("ENG" in groups)
```

Output:

```text
None
False
[]
True
```

Rule to remember: only `groups["ENG"]` creates the default value.

### Mistake 2: Using a list as a queue

`list.pop(0)` works, but it shifts all remaining items and gets slow as the list grows.
Use `deque.popleft()` instead.

### Mistake 3: Assuming `ChainMap` merges everything into a new dict

`ChainMap` is a live view over several mappings. It searches them in order instead of copying them.

### Mistake 4: Using `OrderedDict` just for normal insertion order

In modern Python, plain `dict` already keeps insertion order. Use `OrderedDict` only when you need order-specific methods such as `move_to_end()`.

## 6. Container decision guide

| Need | Best choice | Why | Avoid when |
| --- | --- | --- | --- |
| Count repeated values | `Counter` | Built for frequencies | You need custom aggregation rules |
| Group items by key | `defaultdict(list)` | Removes grouping boilerplate | Missing keys should stay invalid |
| Queue from both ends | `deque` | Fast end operations | You need heavy random indexing |
| Layer configs | `ChainMap` | Reads multiple mappings in order | You need a real merged copy |
| Reorder keys intentionally | `OrderedDict` | Has order-control methods | Plain insertion order is enough |
| Small immutable record | `namedtuple` | Compact and readable | You need mutable fields |

Selection rule:

- If the job is counting, start with `Counter`.
- If the job is grouping, start with `defaultdict`.
- If the job is queue-like, start with `deque`.
- If the job is layered lookup, start with `ChainMap`.
- If the job is an ordered record, start with `namedtuple`.

## 7. Performance and maintainability

| Type | Strength | Limitation |
| --- | --- | --- |
| `Counter` | Fast counting and frequency math | It is still a dictionary, so memory grows with unique keys |
| `defaultdict` | Removes missing-key boilerplate | Missing keys are created automatically, which may hide mistakes |
| `deque` | Fast at both ends | Random indexing is slower than list indexing |
| `ChainMap` | No copying for layered lookup | Lookups search each mapping in order |
| `OrderedDict` | Explicit order operations | Usually unnecessary if you only need insertion order |
| `namedtuple` | Lightweight immutable record | Fields cannot be updated in place |

Best practices:

- Prefer explicit output formatting when the result is shown to users.
- Use the narrowest container that matches the job.
- Do not create missing keys unless that behavior is actually intended.

## 8. Advanced container behavior

### Counter arithmetic

`Counter` supports useful frequency math such as intersection and union.

### `deque(maxlen=...)`

Use `maxlen` when you want a fixed-size rolling buffer.

```python
from collections import deque

window = deque([1, 2, 3], maxlen=3)
window.append(4)
print(list(window))
```

Output:

```text
[2, 3, 4]
```

### `namedtuple._replace()`

Use `_replace()` to create a new record with one changed field.

### `UserDict` for custom behavior

If you need to normalize keys, log writes, or add validation, subclass `UserDict` instead of trying to fight `dict` directly.

## 9. Mental model

| Need | Use | Remember |
| --- | --- | --- |
| Count values | `Counter` | Frequencies first |
| Group records | `defaultdict(list)` | Missing key creates default |
| Queue behavior | `deque` | Fast at both ends |
| Layered config | `ChainMap` | Lookup is ordered |
| Reorder keys | `OrderedDict` | Use when order operations matter |
| Small record | `namedtuple` | Immutable and readable |
