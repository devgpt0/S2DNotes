# Focus300 016: LeetCode 76 - Minimum Window Substring

**Source:** [LeetCode 76](https://leetcode.com/problems/minimum-window-substring/)  
**Difficulty:** Hard  
**Pattern:** variable sliding window with multiplicity counts

## Exact contract

Given nonempty strings `source` and `target`, return the shortest substring of
`source` containing every character of `target` with at least the same
multiplicity. Return `""` if no such substring exists. The source guarantees
the answer is unique when it exists.

## First principles

Expanding the right boundary can only add required characters. Once all target
occurrences are covered, advancing the left boundary can only improve the
window until removing one required occurrence makes it invalid. Thus each
boundary moves forward at most once across the string.

## Cases that decide correctness

- Repeated target characters require repeated source occurrences.
- Character matching is case-sensitive.
- A target longer than the source has no window.
- Irrelevant characters may appear inside the minimum window.
- The answer is a substring, not a subsequence.

## Brute force: expand from every left boundary

```python
from collections import Counter


def minimum_window_brute(source: str, target: str) -> str:
    if not source or not target:
        raise ValueError("source and target must be nonempty")

    required = Counter(target)
    best_start = 0
    best_length = len(source) + 1
    for left in range(len(source)):
        present: Counter[str] = Counter()
        for right in range(left, len(source)):
            present[source[right]] += 1
            if all(
                present[character] >= count for character, count in required.items()
            ):
                length = right - left + 1
                if length < best_length:
                    best_start = left
                    best_length = length
                break
    if best_length > len(source):
        return ""
    return source[best_start : best_start + best_length]
```

This takes `O(n^2 * u)` time for `u` distinct target characters.

## Better transition: track one missing-occurrence count

Instead of rechecking every required character, maintain how many target
occurrences are still missing. A character entering the window decreases that
number only if its remaining requirement was positive. Removing a character
increases it only when the window falls below the requirement.

## Expert solution: expand and contract one window

```python
from collections import Counter


def minimum_window(source: str, target: str) -> str:
    if not source or not target:
        raise ValueError("source and target must be nonempty")

    remaining = Counter(target)
    missing = len(target)
    left = 0
    best_start = 0
    best_length = len(source) + 1
    for right, character in enumerate(source):
        if remaining[character] > 0:
            missing -= 1
        remaining[character] -= 1

        while missing == 0:
            length = right - left + 1
            if length < best_length:
                best_start = left
                best_length = length
            outgoing = source[left]
            remaining[outgoing] += 1
            left += 1
            if remaining[outgoing] > 0:
                missing += 1

    if best_length > len(source):
        return ""
    return source[best_start : best_start + best_length]
```

`missing == 0` is equivalent to satisfying every multiplicity. The inner loop
examines every valid window ending at `right` until the leftmost required
occurrence is removed, so the smallest valid window is never skipped.

**Complexity:** `O(n + m)` time and `O(u)` space.
