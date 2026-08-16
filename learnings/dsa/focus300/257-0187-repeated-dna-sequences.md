# Focus300 257: LeetCode 187 - Repeated DNA Sequences

**Source:** [LeetCode 187](https://leetcode.com/problems/repeated-dna-sequences/)  
**Difficulty:** Medium  
**Pattern:** problem-specific recursion or scanning

## Exact contract

Solve the LeetCode problem 'Repeated DNA Sequences' according to the statement and constraints.

## First principles

Most interview-style problems reduce to the right state definition. Once that state is explicit, the rest is choosing the simplest way to preserve it.


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

- Check the empty and single-item boundary first.
- Look for duplicate handling and off-by-one errors.
- Confirm whether the answer is a boolean, count, value, or structure.
- Make sure the invariant survives every update step.

## Brute force

```python
def find_repeated_dna_sequences_brute(s):
    repeated = set()
    for i in range(len(s) - 9):
        window = s[i : i + 10]
        if s.count(window) > 1:
            repeated.add(window)
    return list(repeated)
```

Try the most direct exhaustive solution.

## Better insight

Identify the state that can be reused and avoid recomputing it.

## Expert solution

```python
def find_repeated_dna_sequences(s):
    seen = set()
    repeated = set()

    for i in range(len(s) - 9):
        window = s[i : i + 10]
        if window in seen:
            repeated.add(window)
        else:
            seen.add(window)
    return list(repeated)
```

Use the smallest invariant that proves correctness and update it once per step.

**Complexity:** Usually linear or near-linear in the input size, with the exact bound determined by the pattern.
