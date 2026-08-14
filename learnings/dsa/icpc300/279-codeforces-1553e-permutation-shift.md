# ICPC300 279: Codeforces 1553E - Permutation Shift

**Source:** [Codeforces 1553E](https://codeforces.com/problemset/problem/1553/E)  
**Difficulty:** 2200  
**Pattern:** fixed-point candidate filter plus permutation cycle counts

## Exact contract

For each shift `k` from `0` through `n-1`, replace every zero-based permutation
value `p[i]` by `(p[i]+k) mod n`. Report the shifts whose resulting permutation
can become the identity in at most `m` arbitrary swaps. Answer multiple tests.

## First principles

A permutation needs `n - number_of_cycles` swaps. Before paying for a full
cycle decomposition, filter shifts by fixed points. A solution using at most
`m` swaps moves at most `2m` positions, so it has at least `n-2m` fixed points.

Position `i` is fixed after exactly shift `(i-p[i]) mod n`. Count these shifts,
then run cycle counting only for candidates meeting the lower bound.

## Cases that decide correctness

- Shift zero is a valid candidate.
- The fixed-point bound is necessary, not sufficient.
- A cycle of length `c` costs `c-1` swaps.
- When `n-2m <= 0`, every shift survives the cheap filter.
- Output shifts are zero-based, as in the source.

## Brute force: test every shift by its cycles

```python
def permutation_shift_brute(permutation: list[int], swap_limit: int) -> list[int]:
    size = len(permutation)
    answers: list[int] = []
    for shift in range(size):
        shifted = [(value + shift) % size for value in permutation]
        seen = [False] * size
        cycles = 0
        for start in range(size):
            if seen[start]:
                continue
            cycles += 1
            vertex = start
            while not seen[vertex]:
                seen[vertex] = True
                vertex = shifted[vertex]
        if size - cycles <= swap_limit:
            answers.append(shift)
    return answers
```

This takes `O(n^2)` time.

## Better insight: only shifts with many fixed points can use few swaps

The fixed-point histogram is linear to build and usually leaves at most a
small multiple of `m` candidates. Exact cycle counts certify those candidates.

## Expert solution: filter, then count cycles

```python
import sys


def solve() -> None:
    input_stream = sys.stdin.buffer
    test_count = int(input_stream.readline())
    output: list[str] = []
    for _ in range(test_count):
        size, swap_limit = map(int, input_stream.readline().split())
        permutation = [value - 1 for value in map(int, input_stream.readline().split())]
        fixed_count = [0] * size
        for position, value in enumerate(permutation):
            fixed_count[(position - value) % size] += 1

        answers: list[int] = []
        minimum_fixed = size - 2 * swap_limit
        for shift, count in enumerate(fixed_count):
            if count < minimum_fixed:
                continue
            seen = [False] * size
            cycles = 0
            for start in range(size):
                if seen[start]:
                    continue
                cycles += 1
                vertex = start
                while not seen[vertex]:
                    seen[vertex] = True
                    vertex = (permutation[vertex] + shift) % size
            if size - cycles <= swap_limit:
                answers.append(shift)
        output.append(" ".join([str(len(answers)), *map(str, answers)]))
    print("\n".join(output))


if __name__ == "__main__":
    solve()
```

Every discarded shift violates a necessary move bound, and every retained
answer passes the exact minimum-swap formula.

**Complexity:** `O(n+nC)` time per case for `C` filtered candidates and `O(n)`
space.
