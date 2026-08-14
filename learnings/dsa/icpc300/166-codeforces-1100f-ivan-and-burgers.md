# ICPC300 166: Codeforces 1100F - Ivan and Burgers

**Source:** [Codeforces 1100F](https://codeforces.com/problemset/problem/1100/F)  
**Pattern:** offline range queries with position-aware xor bases

## Exact contract

Given an array and independent queries `[l,r]`, output the maximum xor obtainable
by choosing any subset of `a[l..r]`. The empty subset is allowed and has xor
zero.

## First principles

A binary linear basis represents every subset xor. Process array positions from
left to right and answer queries when their right endpoint is reached. Along
with each pivot vector, store the latest array position responsible for it.

During insertion, if the incoming representation has a later position than an
existing pivot, swap them before eliminating the pivot bit. This leaves the
basis spanning the entire prefix while maximizing each pivot's associated
position. For a query starting at `l`, vectors with stored position at least
`l` form a basis for exactly the usable suffix of that prefix.

## Cases that decide correctness

- Queries do not modify the array and may be reordered by right endpoint.
- The empty subset makes every answer at least zero.
- Compare positions when inserting, before xor elimination.
- During maximization, ignore pivots whose stored position is before `l`.
- Keep answers in original query order.

## Brute force: enumerate every subset

```python
def burgers_brute(values: list[int], queries: list[tuple[int, int]]) -> list[int]:
    answers = []
    for left, right in queries:
        segment = values[left - 1 : right]
        best = 0
        for subset in range(1 << len(segment)):
            value = 0
            for index, item in enumerate(segment):
                if subset >> index & 1:
                    value ^= item
            best = max(best, value)
        answers.append(best)
    return answers
```

This takes exponential time in the queried range length.

## Better: build a fresh basis per query

```python
def burgers_per_query_basis(
    values: list[int], queries: list[tuple[int, int]]
) -> list[int]:
    bit_count = max(1, max(values, default=0).bit_length())
    answers = []
    for left, right in queries:
        basis = [0] * bit_count
        for value in values[left - 1 : right]:
            for bit in range(bit_count - 1, -1, -1):
                if not (value >> bit & 1):
                    continue
                if basis[bit]:
                    value ^= basis[bit]
                else:
                    basis[bit] = value
                    break
        answer = 0
        for bit in range(bit_count - 1, -1, -1):
            answer = max(answer, answer ^ basis[bit])
        answers.append(answer)
    return answers
```

Linear bases remove subset enumeration, but repeated queries still rescan their
entire ranges.

## Expert solution: retain the latest pivot positions

```python
import sys


def solve() -> None:
    input_stream = sys.stdin.buffer
    size = int(input_stream.readline())
    values = list(map(int, input_stream.readline().split()))
    query_count = int(input_stream.readline())
    queries_by_right: list[list[tuple[int, int]]] = [[] for _ in range(size)]
    for query_index in range(query_count):
        left, right = map(int, input_stream.readline().split())
        queries_by_right[right - 1].append((left - 1, query_index))

    bit_count = max(1, max(values, default=0).bit_length())
    basis = [0] * bit_count
    latest_position = [-1] * bit_count
    answers = [0] * query_count

    for position, item in enumerate(values):
        value = item
        value_position = position
        for bit in range(bit_count - 1, -1, -1):
            if not (value >> bit & 1):
                continue
            if basis[bit] == 0:
                basis[bit] = value
                latest_position[bit] = value_position
                break
            if latest_position[bit] < value_position:
                basis[bit], value = value, basis[bit]
                latest_position[bit], value_position = (
                    value_position,
                    latest_position[bit],
                )
            value ^= basis[bit]

        for left, query_index in queries_by_right[position]:
            answer = 0
            for bit in range(bit_count - 1, -1, -1):
                if latest_position[bit] >= left:
                    answer = max(answer, answer ^ basis[bit])
            answers[query_index] = answer

    print("\n".join(map(str, answers)))


if __name__ == "__main__":
    solve()
```

Position-swapping Gaussian elimination preserves prefix span and gives every
pivot the latest possible witness. Filtering those witnesses at `l` therefore
leaves exactly the subarray span.

**Complexity:** `O((n+q) B)` time and `O(n+q+B)` space, where `B` is the value
bit width.
