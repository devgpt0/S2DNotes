# `itertools` for Collection Workflows

`itertools` helps process collections lazily and efficiently.

## 1) Why It Matters

For large inputs, avoiding intermediate lists reduces memory pressure.

## 2) High-Value Tools

### `chain`

```python
from itertools import chain

out = list(chain([1, 2], [3, 4], [5]))
print(out)  # [1, 2, 3, 4, 5]
```

### `islice`

```python
from itertools import islice

nums = range(100)
print(list(islice(nums, 5, 10)))  # [5, 6, 7, 8, 9]
```

### `groupby` (requires sorted input by grouping key)

```python
from itertools import groupby

records = sorted(
    [("ENG", "Ana"), ("HR", "Raj"), ("ENG", "Mia")],
    key=lambda x: x[0]
)

for dept, grp in groupby(records, key=lambda x: x[0]):
    print(dept, [name for _, name in grp])
```

### `product`

```python
from itertools import product

print(list(product([1, 2], ["A", "B"])))
```

### `combinations` and `permutations`

```python
from itertools import combinations, permutations

print(list(combinations([1, 2, 3], 2)))
print(list(permutations([1, 2, 3], 2)))
```

## 3) Common Pitfalls

- `groupby` groups consecutive equal keys, not all equal keys globally (sort first if needed).
- iterators are one-pass; once consumed, they need recreation.
- converting huge lazy iterators to list defeats memory benefits.

## 4) Collection Design Insight

Prefer iterator pipelines when:
- data is large
- one-pass processing is enough
- memory usage matters more than random access
