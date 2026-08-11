# Iterators: Beginner-to-Expert Notes

## 1. Learning goals

By the end of this note, you should be able to:

- explain the difference between iterable and iterator;
- use `iter()` and `next()` correctly;
- recognize iterator exhaustion;
- write a simple custom iterator when needed.

## 2. Prerequisites

- Lists, loops, and function calls
- Basic understanding of `for` loops

## 3. Topic at a glance

An iterator is an object that returns values one at a time.
It is useful when you want to process data step by step instead of all at once.

### Minimal first example

```python
items = iter(["a", "b"])
print(next(items))
print(next(items))
```

Output:

```text
a
b
```

Why this output?

`next()` asks the iterator for the next value until it runs out.

Roadmap: first we build the mental model, then we learn the core operations, then we compare iterators with lists, and finally we practice using them safely.

## 4. Core vocabulary

| Term | Plain-language meaning | Example |
| --- | --- | --- |
| Iterable | Something you can loop over | `list`, `range`, `str` |
| Iterator | One-pass object that yields values | `iter([1, 2, 3])` |
| Exhausted | No more values left | calling `next()` after the end |
| `iter()` | Creates an iterator from an iterable | `iter(items)` |
| `next()` | Gets the next value from an iterator | `next(items)` |

## 5. Mental model

```mermaid
flowchart TD
    A[Iterable] --> B[iter()]
    B --> C[Iterator]
    C --> D[next()]
    D --> E[Value]
    D --> F[StopIteration when empty]
```

## 6. Foundations

### 6.1 An iterable can become an iterator

```python
items = ["a", "b"]
iterator = iter(items)
print(next(iterator))
print(next(iterator))
```

Output:

```text
a
b
```

### 6.2 Iterators are one-pass

```python
items = iter([1, 2])
print(list(items))
print(list(items))
```

Output:

```text
[1, 2]
[]
```

### 6.3 `for` loops use iterators internally

```python
for item in [1, 2, 3]:
    print(item)
```

Output:

```text
1
2
3
```

## 7. How it works

The `for` loop repeatedly asks for the next item.
When the iterator is empty, Python stops the loop automatically.

## 8. Core operations or methods

- `iter(obj)` creates an iterator.
- `next(it)` returns the next item.
- `StopIteration` marks the end.

```python
items = iter(["x"])
print(next(items))
```

Output:

```text
x
```

## 9. Guided examples

### Example 1: Manual iteration

```python
items = iter([10, 20])
print(next(items))
print(next(items))
```

Output:

```text
10
20
```

### Example 2: Use an iterator in a loop

```python
for value in iter([1, 2, 3]):
    print(value)
```

Output:

```text
1
2
3
```

### Example 3: Exhaustion

```python
items = iter([1])
print(next(items))
print(list(items))
```

Output:

```text
1
[]
```

## 10. Common patterns and real-world applications

- stream values from large inputs;
- consume file-like or data-source iterables;
- build generator pipelines later;
- stop early when you only need part of the data.

## 11. Common mistakes, misconceptions, and failure cases

### Mistake 1: Treating an iterator like a reusable list

Iterators are consumed as you read them.

### Mistake 2: Calling `next()` without handling the end

If there are no values left, Python raises `StopIteration`.

### Mistake 3: Confusing iterable with iterator

An iterable can produce an iterator, but it is not necessarily one itself.

## 12. Comparison and decision guide

| Need | Best choice | Why |
| --- | --- | --- |
| Reusable collection | `list` | can be reused and indexed |
| One-pass traversal | iterator | memory-friendly |
| Lazy pipeline | generator/iterator | no intermediate list |

## 13. Efficiency, limitations, safety, and best practices

- iterators are efficient for streaming;
- they are not reusable without recreating them;
- do not assume you can index them like a list.

## 14. Advanced concepts

- custom iterator classes;
- iterator chaining;
- interaction with generator functions.

## 15. Interview or assessment knowledge

- What is the difference between iterable and iterator?
- Why are iterators one-pass?
- What does `next()` do?
- How does a `for` loop consume an iterator?

## 16. Practice exercises

1. Create an iterator from a list.
2. Print the first two values with `next()`.
3. Show that an iterator is exhausted after use.
4. Explain `StopIteration`.
5. Explain when an iterator is better than a list.

### Solutions

#### Solution 1

```python
items = iter([1, 2, 3])
print(type(items).__name__)
```

Output:

```text
list_iterator
```

#### Solution 2

```python
items = iter(["x", "y"])
print(next(items))
print(next(items))
```

Output:

```text
x
y
```

#### Solution 3

```python
items = iter([1])
print(list(items))
print(list(items))
```

Output:

```text
[1]
[]
```

#### Solution 4

`StopIteration` is the signal that an iterator has no more items.

#### Solution 5

Use an iterator when you want one-pass, memory-friendly processing.

## 17. Summary cheat sheet

| Concept | Remember |
| --- | --- |
| Iterable | can be looped over |
| Iterator | yields one value at a time |
| `iter()` | creates iterator |
| `next()` | gets next value |
| Exhaustion | iterator is empty |

## 18. Mastery checklist and next steps

- [ ] I can explain iterable versus iterator.
- [ ] I can use `iter()` and `next()`.
- [ ] I understand exhaustion.
- [ ] I know that iterators are one-pass.

Next topics:

- `11_generators.md`
- `12_json.md`
- `17_basic_scripting_and_automation.md`
