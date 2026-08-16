# Focus300 145: LeetCode 899 - Orderly Queue

**Source:** [LeetCode 899](https://leetcode.com/problems/orderly-queue/)  
**Difficulty:** Hard  
**Pattern:** reachability invariant plus minimum rotation

## Exact contract

Given a lowercase string `text` and integer `limit`, one move chooses any one
of the first `limit` characters, removes it, and appends it to the end. Apply
any number of moves and return the lexicographically smallest reachable string.

## First principles

When `limit = 1`, every move is a left rotation, so no other permutation is
reachable. When `limit >= 2`, the first two choices allow adjacent-order changes;
repeated moves generate every permutation. The answer is therefore the minimum
rotation in the first case and the sorted characters in the second.


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

- Zero moves are allowed, so the original string is a candidate.
- `limit = 1` preserves cyclic order exactly.
- Any `limit >= 2` has the same full-permutation reachability.
- Repeated characters do not change the reachability proof.
- The limit must lie between one and the string length.

## Brute force: explore every reachable string

```python
def orderly_queue_brute(text: str, limit: int) -> str:
    if not text or any(
        character not in "abcdefghijklmnopqrstuvwxyz" for character in text
    ):
        raise ValueError("text must be a non-empty lowercase English string")
    if not 1 <= limit <= len(text):
        raise ValueError("limit must be between 1 and len(text)")

    seen = {text}
    stack = [text]
    while stack:
        current = stack.pop()
        for index in range(limit):
            candidate = current[:index] + current[index + 1 :] + current[index]
            if candidate not in seen:
                seen.add(candidate)
                stack.append(candidate)
    return min(seen)
```

The state graph may contain `n!` distinct permutations.

## Better transition: split on the reachability threshold

For `limit >= 2`, sorting is immediately optimal. For `limit = 1`, comparing
all `n` rotations takes `O(n^2)`; Booth's two-candidate elimination finds the
minimum rotation in linear time.

## Expert solution: Booth rotation or sorted permutation

```python
def orderly_queue(text: str, limit: int) -> str:
    if not text or any(
        character not in "abcdefghijklmnopqrstuvwxyz" for character in text
    ):
        raise ValueError("text must be a non-empty lowercase English string")
    if not 1 <= limit <= len(text):
        raise ValueError("limit must be between 1 and len(text)")
    if limit >= 2:
        return "".join(sorted(text))

    doubled = text + text
    first = 0
    second = 1
    offset = 0
    while first < len(text) and second < len(text) and offset < len(text):
        left = doubled[first + offset]
        right = doubled[second + offset]
        if left == right:
            offset += 1
        elif left > right:
            first = first + offset + 1
            if first == second:
                first += 1
            offset = 0
        else:
            second = second + offset + 1
            if first == second:
                second += 1
            offset = 0
    start = min(first, second)
    return doubled[start : start + len(text)]
```

When two rotations first differ after `offset` equal characters, every start
through the losing start plus that offset is also worse and can be skipped.

**Complexity:** `O(n)` time for `limit = 1`; `O(n log n)` for sorting when
`limit >= 2`; `O(n)` space for the doubled string or sorted output.
