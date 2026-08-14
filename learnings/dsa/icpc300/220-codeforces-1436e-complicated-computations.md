# ICPC300 220: Codeforces 1436E - Complicated Computations

**Source:** [Codeforces 1436E](https://codeforces.com/problemset/problem/1436/E)  
**Pattern:** last-occurrence minima over candidate MEX values

## Exact contract

Consider the MEX of every nonempty contiguous subarray. Output the smallest
positive integer that is not the MEX of any such subarray.

## First principles

Candidate `x` is a subarray MEX exactly when some gap between consecutive
occurrences of `x` contains every value `1..x-1`. While scanning at position
`i` containing `x`, let `last[x]` be the previous occurrence. All smaller
values occur inside that gap precisely when

`min(last[1], ..., last[x-1]) > last[x]`.

A segment tree over values maintains those last positions. Test the gap before
updating `last[x]`, then test every tail gap after the scan.

## Cases that decide correctness

- Only nonempty subarrays count.
- Attainable MEX values range through `n+1`; `n+2` is the sentinel answer if
  all of them occur.
- Values greater than `n+1` do not affect any candidate test.
- For candidate `1`, a gap must contain at least one position.
- Test both interior gaps and the final suffix gap.

## Brute force: enumerate all subarrays

```python
def complicated_computations_brute(values: list[int]) -> int:
    possible: set[int] = set()
    for left in range(len(values)):
        present: set[int] = set()
        for right in range(left, len(values)):
            present.add(values[right])
            mex = 1
            while mex in present:
                mex += 1
            possible.add(mex)
    answer = 1
    while answer in possible:
        answer += 1
    return answer
```

This examines quadratically many subarrays and repeatedly searches for MEX.

## Better insight: examine only gaps that exclude the candidate

For fixed `x`, every subarray with MEX `x` lies inside one occurrence-free gap.
The most recent position of each smaller value decides whether that gap can
contain all requirements.

## Expert solution: range minimum of last positions

```python
import sys


def solve() -> None:
    input_stream = sys.stdin.buffer
    size = int(input_stream.readline())
    values = list(map(int, input_stream.readline().split()))
    candidate_count = size + 1
    base = 1
    while base < candidate_count:
        base *= 2
    infinity = size + 2
    minimum = [infinity] * (2 * base)
    for index in range(candidate_count):
        minimum[base + index] = 0
    for node in range(base - 1, 0, -1):
        minimum[node] = min(minimum[node * 2], minimum[node * 2 + 1])

    def update(position: int, value: int) -> None:
        node = base + position
        minimum[node] = value
        node //= 2
        while node:
            minimum[node] = min(minimum[node * 2], minimum[node * 2 + 1])
            node //= 2

    def range_minimum(left: int, right: int) -> int:
        if left == right:
            return infinity
        left += base
        right += base
        answer = infinity
        while left < right:
            if left & 1:
                answer = min(answer, minimum[left])
                left += 1
            if right & 1:
                right -= 1
                answer = min(answer, minimum[right])
            left //= 2
            right //= 2
        return answer

    last = [0] * (candidate_count + 1)
    possible = [False] * (candidate_count + 1)
    for position, value in enumerate(values, start=1):
        if value > candidate_count:
            continue
        gap_is_nonempty = position - last[value] > 1
        if gap_is_nonempty and range_minimum(0, value - 1) > last[value]:
            possible[value] = True
        last[value] = position
        update(value - 1, position)

    for value in range(1, candidate_count + 1):
        gap_is_nonempty = size + 1 - last[value] > 1
        if gap_is_nonempty and range_minimum(0, value - 1) > last[value]:
            possible[value] = True
    for value in range(1, candidate_count + 1):
        if not possible[value]:
            print(value)
            return
    print(candidate_count + 1)


if __name__ == "__main__":
    solve()
```

Every occurrence-free gap is tested once at its right boundary or at the array
end. The last-position minimum exactly certifies the presence of all smaller
values.

**Complexity:** `O(n log n)` time and `O(n)` space.
