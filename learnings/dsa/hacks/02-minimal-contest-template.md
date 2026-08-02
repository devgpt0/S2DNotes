# A Minimal Contest Template

## First principles

A contest template should remove repetitive input plumbing without hiding the
algorithm. Every unused helper increases reading time, collision risk, and the
chance of carrying a bug into a solution.

## Why it matters

A large personal template hides bugs, slows reading, and encourages using the
wrong tool. A strong template contains only stable setup.

## Technique

Keep imports and global state minimal. Put one test case in a focused function
when the problem has multiple cases.

## Python pattern

```python
import sys
from collections.abc import Iterator


def solve_case(tokens: Iterator[bytes]) -> int:
    size = int(next(tokens))
    values = [int(next(tokens)) for _ in range(size)]
    return max(values)


def solve() -> None:
    tokens = iter(sys.stdin.buffer.read().split())
    test_count = int(next(tokens))
    answers = [str(solve_case(tokens)) for _ in range(test_count)]
    sys.stdout.write('\n'.join(answers))


if __name__ == '__main__':
    solve()
```

For a single test case, remove `test_count` and call the logic once.

## When to extend it

Add only what this problem uses:

- `deque` for BFS;
- `heapq` for a heap;
- `bisect` for boundaries;
- `math` for exact helpers;
- a proven local DSU/Fenwick implementation.

## Expert habit

Keep tested snippets in notes, not pasted into every submission. Copy only the
smallest required implementation and rename it for the current problem.

## Visual worked example: one explicit execution path

```text
judge input
    |
    v
solve() parses one documented format
    |
    v
algorithm computes typed values
    |
    v
one buffered output

module import -> no input side effect
main guard   -> calls solve exactly once
```

If the statement has test cases, the loop belongs visibly inside `solve`;
do not guess the format in a magical scanner.

## Traps

- Wildcard imports hide names and increase review cost.
- Global mutable arrays can leak between test cases.
- Increasing the recursion limit in every solution is not harmless.
- A `try/except` around the solver can hide the only useful failure signal.
