# Focus300 152: LeetCode 3 - Longest Substring Without Repeating Characters

**Source:** [LeetCode 3](https://leetcode.com/problems/longest-substring-without-repeating-characters/)  
**Difficulty:** Medium  
**Pattern:** sliding window with last-seen indices

## Exact contract

Given a string of at most `50_000` characters, return the maximum length of a
contiguous substring containing no repeated character. A substring is
contiguous; a subsequence is not.

## First principles

For a window ending at index `right`, only the newest occurrence of the current
character can invalidate the window. Move `left` just past that occurrence when
it lies inside the current window. Because `left` never moves backward, each
character is processed once.


## Classroom board: see the repeated work once

```text
brute force tries every choice.
the optimized solution keeps only the state that must survive to the
next step.
```



## Step-by-step transformation

1. Load the current candidates into a stack, queue, heap, or window.
2. Push or pop the structure while the current element keeps the invariant true.
3. Drop stale candidates and keep only the ones that can still affect the answer.
4. Read the final top, window score, or popped order as the output.

These problems transform the input by keeping just the active frontier of candidates instead of rescanning the whole array every time.


## Diagram: active frontier only

```text

            scan left to right
                |
                v
            keep active candidates
                |
                v
            pop stale work
                |
                v
            current best answer
```

These notes keep only the active frontier of useful candidates instead of rescanning the whole input.

## Cases that decide correctness

- The empty string returns zero.
- Repeating a character before the current window does not shrink it.
- Spaces and symbols are ordinary characters.
- A string of one repeated character has answer one.
- The metric is Python character count, not byte count.

## Brute force: extend each start until its first duplicate

```python
def longest_unique_substring_brute(text: str) -> int:
    if type(text) is not str or len(text) > 50_000:
        raise ValueError("text must be a string of length at most 50,000")

    best = 0
    for left in range(len(text)):
        used: set[str] = set()
        for right in range(left, len(text)):
            if text[right] in used:
                break
            used.add(text[right])
            best = max(best, right - left + 1)
    return best
```

This takes `O(n^2)` time in a string with few repeats.

## Better insight: retain the previous occurrence instead of rescanning

The last index of each character tells exactly where the valid window must
start. Taking `max(left, previous + 1)` prevents a stale occurrence from moving
the boundary backward.

## Expert solution: last-seen sliding window

```python
def longest_unique_substring(text: str) -> int:
    if type(text) is not str or len(text) > 50_000:
        raise ValueError("text must be a string of length at most 50,000")

    last_seen: dict[str, int] = {}
    left = 0
    best = 0
    for right, character in enumerate(text):
        if character in last_seen:
            left = max(left, last_seen[character] + 1)
        last_seen[character] = right
        best = max(best, right - left + 1)
    return best
```

After updating `left`, `text[left:right+1]` is duplicate-free and is the
longest valid substring ending at `right`.

**Complexity:** `O(n)` time and `O(min(n, alphabet))` space.
