# Generators: Beginner-to-Expert Notes

## 1. Learning goals

By the end of this note, you should be able to:

- write a generator function with `yield`;
- explain why generators are lazy;
- use generators for one-pass pipelines;
- recognize generator exhaustion and common mistakes.

## 2. Prerequisites

- Iterators
- Functions and loops

## 3. Topic at a glance

A generator is a lazy way to produce values one at a time.
It is often simpler than a custom iterator class.

### Minimal first example

```python
def numbers():
    yield 1
    yield 2


print(list(numbers()))
```

Output:

```text
[1, 2]
```

Why this output?

Each `yield` sends one value to the caller, and the generator resumes later from the same place.

Roadmap: first we build the mental model, then we learn `yield`, then we compare generators with iterators, and finally we practice simple pipelines.

## 4. Core vocabulary

| Term | Plain-language meaning | Example |
| --- | --- | --- |
| Generator function | Function that uses `yield` | `def numbers(): yield 1` |
| Generator object | The lazy object returned by the function | `numbers()` |
| `yield` | Produces one value and pauses | `yield value` |
| Lazy | Work happens only when needed | generator pipeline |

## 5. Mental model

```mermaid
flowchart TD
    A[Call generator function] --> B[Get generator object]
    B --> C[next()]
    C --> D[yield value]
    D --> E[pause]
    E --> C
```

## 6. Foundations

### 6.1 `yield` pauses and resumes

```python
def count():
    yield 1
    yield 2


g = count()
print(next(g))
print(next(g))
```

Output:

```text
1
2
```

### 6.2 Generators are one-pass

```python
def count():
    yield 1


g = count()
print(list(g))
print(list(g))
```

Output:

```text
[1]
[]
```

### 6.3 Generators can simplify pipelines

```python
def doubled(values):
    for value in values:
        yield value * 2


print(list(doubled([1, 2, 3])))
```

Output:

```text
[2, 4, 6]
```

## 7. How it works

When Python reaches `yield`, it returns one value and saves the function state.
The next `next()` call resumes from the saved point.

## 8. Core operations or methods

- `yield` creates lazy output.
- `yield from` delegates to another iterator or generator.
- `next()` drives generator progress.

```python
def values():
    yield from [1, 2, 3]


print(list(values()))
```

Output:

```text
[1, 2, 3]
```

## 9. Guided examples

### Example 1: Simple generator

```python
def letters():
    yield "a"
    yield "b"


print(list(letters()))
```

Output:

```text
['a', 'b']
```

### Example 2: Filter data lazily

```python
def evens(values):
    for value in values:
        if value % 2 == 0:
            yield value


print(list(evens([1, 2, 3, 4])))
```

Output:

```text
[2, 4]
```

### Example 3: Chain generators

```python
def one():
    yield 1


def two():
    yield from one()
    yield 2


print(list(two()))
```

Output:

```text
[1, 2]
```

## 10. Common patterns and real-world applications

- stream lines from files;
- produce filtered or transformed values;
- build memory-friendly processing pipelines;
- stop early when only part of the data is needed.

## 11. Common mistakes, misconceptions, and failure cases

### Mistake 1: Forgetting that generators are exhausted

### Mistake 2: Returning a list when a generator would be cleaner

### Mistake 3: Mixing side effects and yielding without a clear order

## 12. Comparison and decision guide

| Need | Best choice | Why |
| --- | --- | --- |
| Reusable data | list | can be reused |
| Lazy one-pass values | generator | memory-friendly |
| Custom iteration state | generator often simpler | less boilerplate |

## 13. Efficiency, limitations, safety, and best practices

- generators are efficient for large inputs;
- they are one-pass and must be recreated for reuse;
- keep generator bodies small and readable.

## 14. Advanced concepts

- generator expressions;
- generator delegation with `yield from`;
- interaction with `send`, `throw`, and `close` in advanced code.

## 15. Interview or assessment knowledge

- What is the difference between a generator and a list?
- Why do generators save memory?
- What does `yield` do?
- What does `yield from` do?

## 16. Practice exercises

1. Write a generator that yields `1`, `2`, and `3`.
2. Write a generator that filters even numbers.
3. Show that a generator is exhausted after one pass.
4. Explain `yield from`.
5. Explain when a generator is better than a list.

### Solutions

#### Solution 1

```python
def values():
    yield 1
    yield 2
    yield 3


print(list(values()))
```

Output:

```text
[1, 2, 3]
```

#### Solution 2

```python
def evens(values):
    for value in values:
        if value % 2 == 0:
            yield value


print(list(evens([1, 2, 3, 4])))
```

Output:

```text
[2, 4]
```

#### Solution 3

```python
def values():
    yield 1


g = values()
print(list(g))
print(list(g))
```

Output:

```text
[1]
[]
```

#### Solution 4

`yield from` delegates yielding to another iterable or generator.

#### Solution 5

Use a generator when one-pass lazy processing is enough.

## 17. Summary cheat sheet

| Concept | Remember |
| --- | --- |
| `yield` | pause and return one value |
| Generator | lazy value producer |
| `yield from` | delegate to another iterator |
| Exhaustion | one-pass behavior |

## 18. Mastery checklist and next steps

- [ ] I can write a generator function.
- [ ] I understand lazy behavior.
- [ ] I can explain exhaustion.
- [ ] I know when to use a generator instead of a list.

Next topics:

- `12_json.md`
- `13_csv.md`
- `17_basic_scripting_and_automation.md`
