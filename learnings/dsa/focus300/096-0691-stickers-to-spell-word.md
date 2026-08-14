# Focus300 096: LeetCode 691 - Stickers to Spell Word

**Source:** [LeetCode 691](https://leetcode.com/problems/stickers-to-spell-word/)  
**Difficulty:** Hard  
**Pattern:** memoized dynamic programming on a remaining-letter multiset

## Exact contract

Each lowercase sticker word may be used any number of times, and its letters
may be cut apart. Return the minimum number of stickers whose combined letters
can spell the nonempty lowercase target, or `-1` when this is impossible.
Sticker order and unused letters do not matter.

## First principles

Only the multiset of target letters still missing affects future choices. A
canonical 26-count tuple therefore merges all histories with the same
remainder. In each state, requiring the next sticker to contain the first
missing character is safe: some sticker in every successful solution must
supply that character, and stickers can be reordered.

## Cases that decide correctness

- Stickers are reusable; input multiplicity does not limit their use.
- Extra sticker letters are discarded.
- Repeated target letters require repeated total supply.
- A target character absent from all stickers makes the answer `-1`.
- Different orders producing the same remainder must share one DP state.

## Brute force: breadth-first search over covered target positions

```python
from collections import deque


def minimum_stickers_brute(stickers: list[str], target: str) -> int:
    if type(stickers) is not list or not 1 <= len(stickers) <= 50:
        raise ValueError("stickers must contain between 1 and 50 words")
    if any(
        type(sticker) is not str
        or not 1 <= len(sticker) <= 10
        or any(not "a" <= character <= "z" for character in sticker)
        for sticker in stickers
    ):
        raise ValueError("stickers must be nonempty lowercase ASCII words")
    if (
        type(target) is not str
        or not 1 <= len(target) <= 15
        or any(not "a" <= character <= "z" for character in target)
    ):
        raise ValueError("target must be a lowercase ASCII word of length 1..15")

    full_mask = (1 << len(target)) - 1
    queue = deque([(0, 0)])
    visited = {0}
    while queue:
        mask, used = queue.popleft()
        for sticker in stickers:
            next_mask = mask
            for character in sticker:
                for index, target_character in enumerate(target):
                    if target_character == character and not next_mask & (1 << index):
                        next_mask |= 1 << index
                        break
            if next_mask == full_mask:
                return used + 1
            if next_mask != mask and next_mask not in visited:
                visited.add(next_mask)
                queue.append((next_mask, used + 1))
    return -1
```

BFS is exact but may visit all `2^len(target)` position masks.

## Better insight: identical letters make target positions interchangeable

Replace the position mask by the remaining 26 letter counts. Trying only
stickers that reduce one chosen missing character removes fruitless branches.

## Expert solution: memoized remainder-count DP

```python
from functools import cache


def minimum_stickers(stickers: list[str], target: str) -> int:
    if type(stickers) is not list or not 1 <= len(stickers) <= 50:
        raise ValueError("stickers must contain between 1 and 50 words")
    if any(
        type(sticker) is not str
        or not 1 <= len(sticker) <= 10
        or any(not "a" <= character <= "z" for character in sticker)
        for sticker in stickers
    ):
        raise ValueError("stickers must be nonempty lowercase ASCII words")
    if (
        type(target) is not str
        or not 1 <= len(target) <= 15
        or any(not "a" <= character <= "z" for character in target)
    ):
        raise ValueError("target must be a lowercase ASCII word of length 1..15")

    sticker_counts: list[tuple[int, ...]] = []
    for sticker in stickers:
        counts = [0] * 26
        for character in sticker:
            counts[ord(character) - ord("a")] += 1
        sticker_counts.append(tuple(counts))

    needed = [0] * 26
    for character in target:
        needed[ord(character) - ord("a")] += 1

    @cache
    def solve(remaining: tuple[int, ...]) -> int:
        if not any(remaining):
            return 0
        first_missing = next(
            index for index, count in enumerate(remaining) if count > 0
        )
        best = len(target) + 1
        for available in sticker_counts:
            if available[first_missing] == 0:
                continue
            next_remaining = tuple(
                max(0, required - supplied)
                for required, supplied in zip(remaining, available, strict=True)
            )
            suffix = solve(next_remaining)
            if suffix != -1:
                best = min(best, suffix + 1)
        return -1 if best > len(target) else best

    return solve(tuple(needed))
```

Every recursive edge consumes at least the selected missing character, and the
memo key contains all information that can influence the suffix optimum.

**Complexity:** at most `O(S * 26 * product(count_i + 1))` time over reachable
remainders and the same number of memo states, where `S` is the sticker count.
