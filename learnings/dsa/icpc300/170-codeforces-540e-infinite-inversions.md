# ICPC300 170: Codeforces 540E - Infinite Inversions

**Source:** [Codeforces 540E](https://codeforces.com/problemset/problem/540/E)  
**Pattern:** sparse permutation inversions with weighted coordinate gaps

## Exact contract

Start with the infinite identity permutation `p[i] = i` for positive integer
positions. Apply `n` swaps of values at two given positions, whose coordinates
can be as large as `10^9`. Output the finite number of inversions in the final
permutation.

## First principles

Only touched coordinates exchange values; every untouched position remains
fixed. Let the sorted touched coordinates have compressed ranks.

Count inversions between two touched positions with a Fenwick tree over the
final touched values. For a touched position `x` holding touched value `y`, an
untouched coordinate strictly between `x` and `y` forms exactly one inversion
with that position. The number of such coordinates is

`abs(x-y) - abs(rank(x)-rank(y))`:

the physical distance minus the number of steps between touched ranks. No two
untouched positions form an inversion.

## Cases that decide correctness

- Repeated swaps of the same coordinates must update the current permutation.
- Values at touched positions always remain within the touched coordinate set.
- Exclude touched coordinates from the physical gap contribution.
- Count each touched-touched pair once in position order.
- Coordinates beyond the greatest touched position remain identity values and
  create no inversion.

## Brute force: materialize the finite affected prefix

```python
def infinite_inversions_brute(swaps: list[tuple[int, int]]) -> int:
    maximum = max(max(first, second) for first, second in swaps)
    permutation = list(range(maximum + 1))
    for first, second in swaps:
        permutation[first], permutation[second] = (
            permutation[second],
            permutation[first],
        )
    return sum(
        permutation[first] > permutation[second]
        for first in range(1, maximum + 1)
        for second in range(first + 1, maximum + 1)
    )
```

Large coordinates make both the materialized prefix and quadratic counting
impossible.

## Better: compress gaps but compare touched pairs quadratically

```python
def infinite_inversions_compressed(swaps: list[tuple[int, int]]) -> int:
    touched = sorted({coordinate for swap in swaps for coordinate in swap})
    permutation = {coordinate: coordinate for coordinate in touched}
    for first, second in swaps:
        permutation[first], permutation[second] = (
            permutation[second],
            permutation[first],
        )

    rank = {coordinate: index for index, coordinate in enumerate(touched)}
    answer = sum(
        permutation[first] > permutation[second]
        for first_index, first in enumerate(touched)
        for second in touched[first_index + 1 :]
    )
    answer += sum(
        abs(position - permutation[position])
        - abs(rank[position] - rank[permutation[position]])
        for position in touched
    )
    return answer
```

Coordinate gaps are handled arithmetically, but touched-pair comparison remains
quadratic.

## Expert solution: Fenwick inversions plus gap contributions

```python
import sys


def solve() -> None:
    input_stream = sys.stdin.buffer
    swap_count = int(input_stream.readline())
    swaps = [
        tuple(map(int, input_stream.readline().split())) for _ in range(swap_count)
    ]
    touched = sorted({coordinate for swap in swaps for coordinate in swap})
    permutation = {coordinate: coordinate for coordinate in touched}
    for first, second in swaps:
        permutation[first], permutation[second] = (
            permutation[second],
            permutation[first],
        )

    rank = {coordinate: index for index, coordinate in enumerate(touched)}
    fenwick = [0] * (len(touched) + 1)

    def prefix_count(position: int) -> int:
        result = 0
        while position:
            result += fenwick[position]
            position -= position & -position
        return result

    def add(position: int) -> None:
        position += 1
        while position < len(fenwick):
            fenwick[position] += 1
            position += position & -position

    answer = 0
    for seen, position in enumerate(touched):
        value_rank = rank[permutation[position]]
        answer += seen - prefix_count(value_rank + 1)
        add(value_rank)

    answer += sum(
        abs(position - permutation[position])
        - abs(rank[position] - rank[permutation[position]])
        for position in touched
    )
    print(answer)


if __name__ == "__main__":
    solve()
```

The Fenwick pass counts every inversion with two touched endpoints. The gap
formula counts every inversion with exactly one touched endpoint, and these
disjoint classes contain all possible inversions.

**Complexity:** `O(n log n)` time and `O(n)` space for at most `2n` touched
coordinates.
