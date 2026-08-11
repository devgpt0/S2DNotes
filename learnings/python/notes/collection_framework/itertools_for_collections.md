# `itertools` for Collection Workflows: Beginner-to-Expert Notes

## 1. Learning goals

By the end of this note, you should be able to:

- use `itertools` to build lazy pipelines over collections;
- choose between `chain`, `islice`, `groupby`, `product`, `combinations`, and `permutations`;
- explain why some iterator results can only be used once;
- avoid the most common `groupby` mistake.

## 2. Prerequisites

- Lists, loops, and slicing
- Basic sorting
- An understanding of iterators at a simple level

## 3. Topic at a glance

`itertools` gives you small, focused tools for working with iterables lazily.
That means the data is processed as needed instead of being copied into big temporary lists.

### Minimal first example

```python
from itertools import chain

items = list(chain([1, 2], [3, 4], [5]))
print(items)
```

Output:

```text
[1, 2, 3, 4, 5]
```

Why this output?

`chain()` joins several iterables into one stream.

Roadmap: first we build the mental model, then we learn the main tools, then we compare them, and finally we practice using them safely.

## 4. Core vocabulary

| Term | Plain-language meaning | Example |
| --- | --- | --- |
| Iterable | Something you can loop over | `range(5)` |
| Iterator | A one-pass object that yields values | `iter([1, 2, 3])` |
| Lazy | Work happens only when values are requested | `chain()` |
| `chain` | Joins several iterables together | `chain(a, b)` |
| `islice` | Takes a slice from an iterator | `islice(nums, 5, 10)` |
| `groupby` | Groups consecutive equal keys | `groupby(records, key=...)` |
| `product` | Cartesian product of inputs | `product([1, 2], ["A"])` |
| `combinations` | Unique unordered selections | `combinations(items, 2)` |
| `permutations` | Ordered arrangements | `permutations(items, 2)` |

## 5. Mental model

```mermaid
flowchart TD
    A[Input iterables] --> B[Lazy itertools tool]
    B --> C[Iterator output]
    C --> D[Consume once with loop, list(), sum(), etc.]
```

Think of `itertools` as building blocks for iterator pipelines.
Each building block does a small job well and keeps memory use low.

## 6. Foundations

### 6.1 `chain()` joins iterables

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

### 6.2 `islice()` takes a slice from an iterator

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

### 6.3 `groupby()` groups consecutive equal keys

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

## 7. How it works

Most `itertools` functions return iterators, not lists.
That means values are produced only when you loop over them or convert them to a concrete container.

This is why `itertools` is memory-friendly for large inputs.

## 8. Core operations or methods

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

## 9. Guided examples

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

## 10. Common patterns and real-world applications

- Use `chain()` to combine chunks from several files or sources.
- Use `islice()` to sample a large iterable without loading everything.
- Use `groupby()` after sorting to summarize records.
- Use `product()` for configuration matrices, test-case generation, or cartesian search spaces.
- Use `combinations()` and `permutations()` for candidate generation.

## 11. Common mistakes, misconceptions, and failure cases

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

## 12. Comparison and decision guide

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

## 13. Efficiency, limitations, safety, and best practices

- Lazy iterators reduce memory use.
- Iterator pipelines are good when you only need one pass.
- `groupby()` is powerful but easy to misuse if you forget to sort.
- The moment you convert a lazy pipeline to a list, you pay the memory cost.

Best practices:

- Keep the pipeline lazy for as long as possible.
- Sort before `groupby()` if you want global grouping.
- Recreate iterators when you need to traverse again.

## 14. Advanced concepts

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

## 15. Interview or assessment knowledge

- Why use `itertools`? It keeps processing lazy and memory-friendly.
- Why is `groupby()` tricky? It groups consecutive keys, not all equal keys globally.
- Why use `chain()` instead of `+`? `chain()` works lazily and avoids creating temporary lists.
- Why use `islice()`? It works on iterators, not just lists.

## 16. Practice exercises

1. Use `chain()` to combine two lists.
2. Use `islice()` to take items 2 through 5 from `range(10)`.
3. Use `groupby()` correctly on a sorted list of department records.
4. Use `product()` to list all combinations of `[1, 2]` and `["A", "B"]`.
5. Use `accumulate()` to print running totals for `[2, 3, 4]`.

### Solutions

#### Solution 1

```python
from itertools import chain

print(list(chain([1, 2], [3, 4])))
```

Output:

```text
[1, 2, 3, 4]
```

#### Solution 2

```python
from itertools import islice

print(list(islice(range(10), 2, 6)))
```

Output:

```text
[2, 3, 4, 5]
```

#### Solution 3

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

#### Solution 4

```python
from itertools import product

print(list(product([1, 2], ["A", "B"])))
```

Output:

```text
[(1, 'A'), (1, 'B'), (2, 'A'), (2, 'B')]
```

#### Solution 5

```python
from itertools import accumulate

print(list(accumulate([2, 3, 4])))
```

Output:

```text
[2, 5, 9]
```

## 17. Summary cheat sheet

| Need | Use | Remember |
| --- | --- | --- |
| Join streams | `chain()` | Lazy concatenation |
| Slice an iterator | `islice()` | Works without a list |
| Group by key | `groupby()` | Sort first for global grouping |
| Generate cartesian combinations | `product()` | Can grow fast |
| Generate subsets | `combinations()` | Order does not repeat |
| Generate permutations | `permutations()` | Order matters |

## 18. Mastery checklist and next steps

- [ ] I can explain why `itertools` is lazy.
- [ ] I know when to use `chain()` and `islice()`.
- [ ] I understand the sorted-input rule for `groupby()`.
- [ ] I can distinguish `product`, `combinations`, and `permutations`.
- [ ] I can write a small iterator pipeline without making temporary lists too early.

Next topics:

- `collections` module types
- `heapq` and `bisect`
- `collections.abc` and typing
- specialized sequence types
