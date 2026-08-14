# ICPC300 274: Codeforces 1322B - Present

**Source:** [Codeforces 1322B](https://codeforces.com/problemset/problem/1322/B)  
**Difficulty:** 2200  
**Pattern:** pair-sum parity independently for every bit

## Exact contract

Given an integer array, compute the bitwise XOR of `a[i]+a[j]` over every
unordered pair `i < j`.

## First principles

A bit is set in the XOR exactly when an odd number of pair sums have that bit
set. For bit value `h=2^b`, reduce every number modulo `2h`. A residue pair has
bit `b` set precisely when its sum lies in either interval

- `[h,2h-1]`, or
- `[3h,4h-2]`.

Sort the residues and count partners in both ranges with binary search.

## Cases that decide correctness

- Pairs are unordered and never pair an index with itself.
- Carries from lower bits are preserved by residue pair sums.
- Residue sums can exceed one modulus, creating the second interval.
- Only the parity of each pair count matters.
- Equal values remain distinct indices.

## Brute force: XOR every pair sum

```python
def present_brute(values: list[int]) -> int:
    answer = 0
    for left in range(len(values)):
        for right in range(left + 1, len(values)):
            answer ^= values[left] + values[right]
    return answer
```

This takes `O(n^2)` time.

## Better insight: XOR lets every result bit be counted independently

Modulo `2^(b+1)` retains exactly the information needed for bit `b`. Sorting
turns each valid sum interval into two binary searches per left endpoint.

## Expert solution: sorted residues and range counts

```python
from bisect import bisect_left, bisect_right
import sys


def solve() -> None:
    input_stream = sys.stdin.buffer
    size = int(input_stream.readline())
    values = list(map(int, input_stream.readline().split()))
    if len(values) != size:
        raise ValueError("array length does not match n")
    answer = 0
    maximum_sum = 2 * max(values)
    bit = 0
    while 1 << bit <= maximum_sum:
        half = 1 << bit
        modulus = half * 2
        residues = sorted(value % modulus for value in values)
        pair_count = 0
        for index, value in enumerate(residues):
            start = index + 1
            pair_count += bisect_right(
                residues, modulus - 1 - value, start
            ) - bisect_left(residues, half - value, start)
            pair_count += bisect_right(
                residues, 2 * modulus - 2 - value, start
            ) - bisect_left(residues, half + modulus - value, start)
        if pair_count & 1:
            answer |= half
        bit += 1
    print(answer)


if __name__ == "__main__":
    solve()
```

Each unordered pair is counted exactly once in exactly the residue intervals
where its sum has the current bit set.

**Complexity:** `O(n log n log A)` time and `O(n)` space.
