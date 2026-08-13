# `itertools` for Collection Workflows
## 1. Core truth

`itertools` gives you small, focused tools for working with iterables lazily.
That means the data is processed as needed instead of being copied into big temporary lists.

```python
from itertools import chain

items = list(chain([1, 2], [3, 4], [5]))
print(items)
```

Output:

```text
[1, 2, 3, 4, 5]
```

`chain()` joins several iterables into one stream.

## 2. Lazy iteration foundations

### `chain()` joins iterables

```python
from itertools import chain

result = list(chain([1, 2], [3, 4], [5]))
print(result)
```

Output:

```text
[1, 2, 3, 4, 5]
```

Practical takeaway: use `chain()` when you want one stream from several smaller streams.

### `islice()` takes a slice from an iterator

```python
from itertools import islice

nums = range(10)
print(list(islice(nums, 3, 7)))
```

Output:

```text
[3, 4, 5, 6]
```

Practical takeaway: use `islice()` when the source is an iterator and normal slicing is not available.

### `groupby()` groups consecutive equal keys

```python
from itertools import groupby

records = sorted(
    [("ENG", "Ana"), ("HR", "Raj"), ("ENG", "Mia")],
    key=lambda item: item[0],
)

for dept, group in groupby(records, key=lambda item: item[0]):
    print(dept, [name for _, name in group])
```

Output:

```text
ENG ['Ana', 'Mia']
HR ['Raj']
```

Practical takeaway: sort first when you want all equal keys grouped together.

## 3. Iterator-building tools

### `chain()`

Use it to glue iterables together.

### `islice()`

Use it to take a bounded window from an iterator.

### `groupby()`

Use it only when consecutive equal keys should be grouped.

### `product()`

Use it for all pairwise combinations across input pools.

```python
from itertools import product

print(list(product([1, 2], ["A", "B"])))
```

Output:

```text
[(1, 'A'), (1, 'B'), (2, 'A'), (2, 'B')]
```

### `combinations()` and `permutations()`

```python
from itertools import combinations, permutations

print(list(combinations([1, 2, 3], 2)))
print(list(permutations([1, 2, 3], 2)))
```

Output:

```text
[(1, 2), (1, 3), (2, 3)]
[(1, 2), (1, 3), (2, 1), (2, 3), (3, 1), (3, 2)]
```

## 4. Practical iterator pipelines

### Example 1: Merge sources lazily

```python
from itertools import chain

logs = chain(["app-1"], ["app-2"], ["app-3"])
print(list(logs))
```

Output:

```text
['app-1', 'app-2', 'app-3']
```

### Example 2: Read a small window from a large stream

```python
from itertools import islice

numbers = range(100)
print(list(islice(numbers, 5, 10)))
```

Output:

```text
[5, 6, 7, 8, 9]
```

### Example 3: Generate all team pairings

```python
from itertools import combinations

players = ["Ana", "Mia", "Raj"]
print(list(combinations(players, 2)))
```

Output:

```text
[('Ana', 'Mia'), ('Ana', 'Raj'), ('Mia', 'Raj')]
```

- Use `chain()` to combine chunks from several files or sources.
- Use `islice()` to sample a large iterable without loading everything.
- Use `groupby()` after sorting to summarize records.
- Use `product()` for configuration matrices, test-case generation, or cartesian search spaces.
- Use `combinations()` and `permutations()` for candidate generation.

## 5. Iterator mistakes

### Mistake 1: Forgetting that `groupby()` groups only consecutive keys

```python
from itertools import groupby

records = [("ENG", "Ana"), ("HR", "Raj"), ("ENG", "Mia")]
for dept, group in groupby(records, key=lambda item: item[0]):
    print(dept, [name for _, name in group])
```

Output:

```text
ENG ['Ana']
HR ['Raj']
ENG ['Mia']
```

Correct approach:

```python
from itertools import groupby

records = sorted(
    [("ENG", "Ana"), ("HR", "Raj"), ("ENG", "Mia")],
    key=lambda item: item[0],
)
for dept, group in groupby(records, key=lambda item: item[0]):
    print(dept, [name for _, name in group])
```

Output:

```text
ENG ['Ana', 'Mia']
HR ['Raj']
```

### Mistake 2: Reusing a consumed iterator

```python
nums = iter([1, 2, 3])
print(list(nums))
print(list(nums))
```

Output:

```text
[1, 2, 3]
[]
```

Rule to remember: most iterators can be consumed only once.

### Mistake 3: Converting huge lazy results to a list too early

That throws away the memory benefit.

## 6. Iterator decision guide

| Need | Best choice | Why | Avoid when |
| --- | --- | --- | --- |
| Join several iterables | `chain()` | Simple lazy concatenation | You need a single copied list immediately |
| Take a window from an iterator | `islice()` | Works on one-pass iterators | You already have a list slice |
| Group consecutive equal keys | `groupby()` | Fast streaming grouping | The data is unsorted and must be grouped globally |
| Generate all pairs across pools | `product()` | Cartesian product | The search space is too large |
| Generate unordered subsets | `combinations()` | No duplicate orderings | Order matters |
| Generate ordered arrangements | `permutations()` | Order-sensitive results | You only need unique subsets |

Selection rule:

- Use iterator tools when you want lazy processing.
- Use `groupby()` only when the input order already matches the grouping plan.

## 7. Performance and safety

- Lazy iterators reduce memory use.
- Iterator pipelines are good when you only need one pass.
- `groupby()` is powerful but easy to misuse if you forget to sort.
- The moment you convert a lazy pipeline to a list, you pay the memory cost.

Best practices:

- Keep the pipeline lazy for as long as possible.
- Sort before `groupby()` if you want global grouping.
- Recreate iterators when you need to traverse again.

## 8. Advanced iterator behavior

### Running totals with `accumulate()`

```python
from itertools import accumulate

print(list(accumulate([1, 2, 3, 4])))
```

Output:

```text
[1, 3, 6, 10]
```

### Iterator pipelines

You can combine multiple `itertools` functions to process data step by step without building temporary lists.

## 9. Mental model

| Need | Use | Remember |
| --- | --- | --- |
| Join streams | `chain()` | Lazy concatenation |
| Slice an iterator | `islice()` | Works without a list |
| Group by key | `groupby()` | Sort first for global grouping |
| Generate cartesian combinations | `product()` | Can grow fast |
| Generate subsets | `combinations()` | Order does not repeat |
| Generate permutations | `permutations()` | Order matters |

## 10. Batching with a completeness contract

`batched()` was added in Python 3.12. On Python 3.13+, `strict=True` rejects a
short final batch.

```python
from itertools import batched

print(list(batched(range(6), 2, strict=True)))
```

Output on Python 3.13+:

```text
[(0, 1), (2, 3), (4, 5)]
```

Use strict batches when downstream code requires fixed-size records.

## 11. `tee()` has hidden buffering

`tee(iterator, n)` creates independently consumable branches, but values needed
by a slower branch are buffered in memory.

```python
from itertools import tee

first, second = tee(iter([1, 2, 3]))
print(next(first))
print(list(second))
print(list(first))
```

Output:

```text
1
[1, 2, 3]
[2, 3]
```

Do not use `tee()` for branches that can drift arbitrarily far apart, and do not
assume the returned iterators are thread-safe.
