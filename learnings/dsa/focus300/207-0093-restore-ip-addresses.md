# Focus300 207: LeetCode 93 - Restore IP Addresses

**Source:** [LeetCode 93](https://leetcode.com/problems/restore-ip-addresses/)  
**Difficulty:** Medium  
**Pattern:** segment-validated backtracking

## Exact contract

Split the string into exactly four valid IPv4 segments and return every possible address.

## First principles

Every segment must be between `0` and `255`, and leading zeroes are only valid for the single digit `0`. That makes the recursion shallow but heavily constrained.


## Classroom board: see the repeated work once

```text
brute force tries every choice.
the optimized solution keeps only the state that must survive to the
next step.
```



## Step-by-step transformation

1. Choose a start state such as a cell, node, or partial path.
2. Mark the state as visited or temporarily commit the choice.
3. Expand to valid neighbors or next choices while the invariant still holds.
4. Undo the temporary choice when the branch finishes, then return the collected answer.

These problems transform the input into output by exploring one branch at a time and backtracking whenever a branch can no longer produce a valid solution.


## Diagram: search and undo

```text

            start state
                |
                v
            choose one path
                |
                v
            explore neighbors
                |
                v
            undo and try next path
                |
                v
            answer
```

These notes use search, visit markers, and backtracking to turn one starting state into the final valid path or count.

## Cases that decide correctness

- The string length must be feasible for four segments.
- Segments with leading zeroes are invalid unless the segment is exactly `0`.
- Only four segments are allowed in the final answer.
- Backtracking must stop as soon as the remaining length cannot fit the remaining segments.

## Brute force

```python
def restore_ip_addresses_brute(s):
    result = []
    n = len(s)
    for i in range(1, 4):
        for j in range(i + 1, i + 4):
            for k in range(j + 1, j + 4):
                parts = [s[:i], s[i:j], s[j:k], s[k:]]
                if all(part and (part == "0" or not part.startswith("0")) and int(part) <= 255 for part in parts):
                    result.append(".".join(parts))
    return result
```

Enumerate every cut pattern and validate the four parts afterward.

## Better insight

Build segments incrementally and prune impossible lengths before recursing deeper.

## Expert solution

```python
def restore_ip_addresses(s):
    result = []

    def backtrack(start, parts):
        if len(parts) == 4:
            if start == len(s):
                result.append(".".join(parts))
            return
        for end in range(start + 1, min(len(s), start + 3) + 1):
            part = s[start:end]
            if part.startswith("0") and part != "0":
                continue
            if int(part) <= 255:
                backtrack(end, parts + [part])

    backtrack(0, [])
    return result
```

Backtrack over the next cut position, validate each segment immediately, and emit the address only when exactly four valid parts are chosen.

**Complexity:** O(3^4) practical branching with pruning, bounded by the short input length.
