# Focus300 287: LeetCode 264 - Ugly Number II

**Source:** [LeetCode 264](https://leetcode.com/problems/ugly-number-ii/)  
**Difficulty:** Medium  
**Pattern:** multiplicative sequence generation

## Exact contract

Return the `n`th ugly number, where ugly numbers have no prime factors other than `2`, `3`, and `5`.

## First principles

Every ugly number can be produced by multiplying a smaller ugly number by `2`, `3`, or `5`. A merged generation process avoids duplicates and preserves ascending order.


## Classroom board: see the repeated work once

```text
brute force tries every choice.
the optimized solution keeps only the state that must survive to the
next step.
```



## Step-by-step transformation

1. Read the input and identify the smallest state that still determines the answer.
2. Process one element, node, or row at a time while preserving that state.
3. Discard work that can no longer change the result.
4. Convert the surviving state into the output the problem requests.

The examples and code below show this transformation on the specific problem instance.


## Diagram: input to output

```text

        input
            |
            v
        core invariant
            |
            v
        process one step at a time
            |
            v
        output
```

The note shows the main idea, the repeated work, and the small state that turns the input into the output.

## Cases that decide correctness

- The first ugly number is `1`.
- Duplicate multiples such as `6 = 2*3 = 3*2` must not repeat.
- The sequence is strictly increasing after duplicates are removed.
- The answer is rank-based, not property-based only.

## Brute force

```python
def nth_ugly_number_brute(n):
    ugly = [1]
    i2 = i3 = i5 = 0
    while len(ugly) < n:
        nxt = min(ugly[i2] * 2, ugly[i3] * 3, ugly[i5] * 5)
        ugly.append(nxt)
        if nxt == ugly[i2] * 2:
            i2 += 1
        if nxt == ugly[i3] * 3:
            i3 += 1
        if nxt == ugly[i5] * 5:
            i5 += 1
    return ugly[-1]
```

Check each integer in order and test whether its prime factors are only `2`, `3`, and `5`.

## Better insight

Generate candidates from previously known ugly numbers using a heap or three-pointer merge.

## Expert solution

```python
def nth_ugly_number(n):
    ugly = [1]
    i2 = i3 = i5 = 0
    while len(ugly) < n:
        nxt = min(ugly[i2] * 2, ugly[i3] * 3, ugly[i5] * 5)
        ugly.append(nxt)
        if nxt == ugly[i2] * 2:
            i2 += 1
        if nxt == ugly[i3] * 3:
            i3 += 1
        if nxt == ugly[i5] * 5:
            i5 += 1
    return ugly[-1]
```

Maintain three moving indices for the next multiples of `2`, `3`, and `5`, and always append the smallest unseen candidate.

**Complexity:** O(n) time and O(n) space with the pointer DP formulation.
