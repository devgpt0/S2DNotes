# Focus300 143: LeetCode 891 - Sum of Subsequence Widths

**Source:** [LeetCode 891](https://leetcode.com/problems/sum-of-subsequence-widths/)  
**Difficulty:** Hard  
**Pattern:** sorted contribution counting

## Exact contract

For every non-empty subsequence of `numbers`, define its width as
`maximum - minimum`. Return the sum of all widths modulo `1_000_000_007`.
Equal values at different indices still represent different subsequence choices.

## First principles

After sorting, value at index `i` is the maximum of `2^i` subsequences formed by
choosing any subset of earlier positions. It is the minimum of `2^(n-1-i)`
subsequences formed from later positions. Its total signed contribution is the
difference of those two counts times the value.


## Classroom board: see the repeated work once

```text
brute force tries every choice.
the optimized solution keeps only the state that must survive to the
next step.
```



## Step-by-step transformation

1. Compress the input into counts, prefixes, bit masks, or another compact state.
2. Update that state once per element instead of recomputing earlier work.
3. Combine the stored pieces to recover the value the problem asks for.
4. Return the final count, sum, or constructed answer.

These notes transform input into output by reducing the data to a compact invariant first, then rebuilding the answer from that invariant.


## Diagram: compress the input first

```text

            raw values
                |
                v
            counts / prefix / bit state
                |
                v
            combine stored facts
                |
                v
            final answer
```

The algorithm first compresses the input into a small invariant, then rebuilds the answer from that compact state.

## Cases that decide correctness

- Single-element subsequences have width zero.
- Duplicate values keep separate index contributions even though their values match.
- Sorting a copy avoids changing the caller's list.
- Signed intermediate contributions may be negative.
- Apply the modulus to the accumulated sum.

## Brute force: enumerate every non-empty index subset

```python
def sum_subsequence_widths_brute(numbers: list[int]) -> int:
    if not numbers:
        raise ValueError("numbers must be non-empty")

    answer = 0
    for mask in range(1, 1 << len(numbers)):
        subsequence = [
            value for index, value in enumerate(numbers) if mask & (1 << index)
        ]
        answer += max(subsequence) - min(subsequence)
    return answer % 1_000_000_007
```

This takes `O(n * 2^n)` time and `O(n)` temporary space.

## Better transition: count endpoint roles instead of subsequences

Every non-empty subsequence has one sorted position serving as its chosen
maximum and one as its chosen minimum. Summing those roles counts each width
exactly once without constructing a subsequence.

## Expert solution: powers-of-two contributions

```python
def sum_subsequence_widths(numbers: list[int]) -> int:
    if not numbers:
        raise ValueError("numbers must be non-empty")

    modulus = 1_000_000_007
    ordered = sorted(numbers)
    power = 1
    answer = 0
    last = len(ordered) - 1
    for index, value in enumerate(ordered):
        answer += power * (value - ordered[last - index])
        answer %= modulus
        power = power * 2 % modulus
    return answer
```

Pairing index `i` with `n - 1 - i` combines its maximum and minimum terms while
one running power supplies `2^i`.

**Complexity:** `O(n log n)` time for sorting and `O(n)` space for the copy.
