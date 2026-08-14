# ICPC300 216: Codeforces 1254B2 - Send Boxes to Alice (Hard Version)

**Source:** [Codeforces 1254B2](https://codeforces.com/problemset/problem/1254/B2)  
**Pattern:** prime group size with prefix-flow cost

## Exact contract

Position `i` contains `a[i]` boxes. One move transfers one box to an adjacent
position at cost one. Rearrange the boxes so some integer greater than one
divides every final position count. Output the minimum cost, or `-1` if
impossible.

## First principles

It suffices to test prime divisors of the total: any composite common divisor
has a prime divisor that is no more restrictive. Consider one such prime `p`.
Across the boundary after position `i`, let
`remainder = prefix_boxes mod p`. Completing groups can send those remainder
boxes right, or equivalently send `p-remainder` boxes left. The minimum number
crossing that boundary is `min(remainder, p-remainder)`.

Every adjacent move crosses exactly one boundary, so summing these independent
minimum flows gives the optimal cost for `p`.

## Cases that decide correctness

- A total of one has no prime divisor and is impossible.
- A total of zero already needs no moves.
- Only distinct prime divisors of the total need testing.
- Large counts must not be expanded into individual boxes.
- Positions with zero boxes still contribute movement distance.

## Brute force: expand small groups and use medians

```python
def send_boxes_brute(boxes: list[int]) -> int:
    total = sum(boxes)
    if total == 0:
        return 0
    factors = [
        value
        for value in range(2, total + 1)
        if total % value == 0
        and all(value % divisor for divisor in range(2, int(value**0.5) + 1))
    ]
    if not factors:
        return -1
    positions = [position for position, count in enumerate(boxes) for _ in range(count)]
    answer = 10**30
    for group_size in factors:
        cost = 0
        for start in range(0, total, group_size):
            group = positions[start : start + group_size]
            median = group[group_size // 2]
            cost += sum(abs(position - median) for position in group)
        answer = min(answer, cost)
    return answer
```

Expanding positions is impossible when counts are large.

## Better insight: count boxes crossing each boundary

Median grouping and boundary flow are equivalent on a line. Prefix remainders
compute that flow without materializing any box.

## Expert solution: test prime divisors with prefix remainders

```python
import sys


def solve() -> None:
    input_stream = sys.stdin.buffer
    _ = int(input_stream.readline())
    boxes = list(map(int, input_stream.readline().split()))
    total = sum(boxes)
    if total == 0:
        print(0)
        return

    prime_factors = []
    remaining = total
    divisor = 2
    while divisor * divisor <= remaining:
        if remaining % divisor == 0:
            prime_factors.append(divisor)
            while remaining % divisor == 0:
                remaining //= divisor
        divisor += 1
    if remaining > 1:
        prime_factors.append(remaining)
    if not prime_factors:
        print(-1)
        return

    answer = 10**30
    for group_size in prime_factors:
        remainder = 0
        cost = 0
        for count in boxes[:-1]:
            remainder = (remainder + count) % group_size
            cost += min(remainder, group_size - remainder)
        answer = min(answer, cost)
    print(answer)


if __name__ == "__main__":
    solve()
```

For each prime, the boundary sum is both achievable by consecutive grouping
and a lower bound on every adjacent-transfer plan.

**Complexity:** `O(sqrt(S) + n * omega(S))` time and `O(omega(S))` space, where
`S` is the total and `omega(S)` its number of distinct prime factors.
