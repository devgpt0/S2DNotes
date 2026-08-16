# Focus300 203: LeetCode 89 - Gray Code

**Source:** [LeetCode 89](https://leetcode.com/problems/gray-code/)  
**Difficulty:** Medium  
**Pattern:** reflected sequence generation

## Exact contract

Generate an `n`-bit Gray code sequence in which consecutive numbers differ by exactly one bit.

## First principles

Reflection preserves the one-bit-difference property because the second half is the first half reversed with a new high bit set. Each additional bit doubles the sequence while changing only one bit at each transition.


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

- Zero bits should still produce a valid starting sequence.
- Consecutive outputs must differ by exactly one bit.
- The sequence length must be `2^n`.
- The first and last values are both valid members of the cycle.

## Brute force

```python
def gray_code_brute(n):
    return [i ^ (i >> 1) for i in range(1 << n)]
```

Generate ordinary binary numbers and filter for adjacency, which is wasteful and fragile.

## Better insight

Build the next bit layer by reflecting the current sequence and prefixing the new bit.

## Expert solution

```python
def gray_code(n):
    result = [0]
    for bit in range(n):
        result += [x | (1 << bit) for x in reversed(result)]
    return result
```

Start from `[0]` and repeatedly append the reversed sequence with the new bit set in each reflected value.

**Complexity:** O(2^n) time and O(2^n) space for the output.
