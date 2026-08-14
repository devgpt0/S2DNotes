# Focus300 015: LeetCode 68 - Text Justification

**Source:** [LeetCode 68](https://leetcode.com/problems/text-justification/)  
**Difficulty:** Hard  
**Pattern:** greedy line packing and quotient-remainder spacing

## Exact contract

Given nonempty words and `max_width`, greedily place as many words as possible
on each line without exceeding the width. Fully justify every non-final
multiword line: distribute spaces as evenly as possible, with larger gaps on
the left. Left-justify the final line and every one-word line. Every returned
line must have exactly `max_width` characters.

## First principles

The next word fits when the total word characters plus one mandatory space per
gap remains within the width. Once a line's words are fixed, `divmod` of the
required spaces by the gap count gives the common gap size and the number of
leftmost gaps receiving one extra space.

## Cases that decide correctness

- A word whose length equals the width forms a complete line.
- A one-word non-final line is padded on the right.
- The last line uses single internal spaces and right padding.
- Extra spaces go to leftmost gaps.
- Words remain in their original order.

## Brute force: repack and distribute spaces one at a time

```python
def full_justify_brute(words: list[str], max_width: int) -> list[str]:
    if (
        not words
        or max_width <= 0
        or any(not word or len(word) > max_width for word in words)
    ):
        raise ValueError("words must be nonempty and fit the width")

    lines: list[str] = []
    start = 0
    while start < len(words):
        end = start + 1
        while end < len(words) and len(" ".join(words[start : end + 1])) <= max_width:
            end += 1
        current = words[start:end]
        if end == len(words) or len(current) == 1:
            lines.append(" ".join(current).ljust(max_width))
        else:
            gaps = [1] * (len(current) - 1)
            extra = max_width - sum(map(len, current)) - len(gaps)
            for index in range(extra):
                gaps[index % len(gaps)] += 1
            line = current[0]
            for gap, word in zip(gaps, current[1:]):
                line += " " * gap + word
            lines.append(line)
        start = end
    return lines
```

This is correct but repeatedly joins candidate lines and assigns surplus spaces
one character at a time.

## Better transition: compute each gap arithmetically

Track the current line's total word characters while extending it. For a
non-final line with `gaps` gaps and `spaces` required spaces,
`divmod(spaces, gaps)` determines the complete distribution immediately.

## Expert solution: one greedy packing pass

```python
def full_justify(words: list[str], max_width: int) -> list[str]:
    if (
        not words
        or max_width <= 0
        or any(not word or len(word) > max_width for word in words)
    ):
        raise ValueError("words must be nonempty and fit the width")

    lines: list[str] = []
    start = 0
    while start < len(words):
        end = start + 1
        letter_count = len(words[start])
        while (
            end < len(words)
            and letter_count + len(words[end]) + (end - start) <= max_width
        ):
            letter_count += len(words[end])
            end += 1

        word_count = end - start
        if end == len(words) or word_count == 1:
            lines.append(" ".join(words[start:end]).ljust(max_width))
        else:
            gap_count = word_count - 1
            gap_width, wider_gaps = divmod(max_width - letter_count, gap_count)
            parts: list[str] = []
            for offset in range(gap_count):
                parts.append(words[start + offset])
                parts.append(" " * (gap_width + (offset < wider_gaps)))
            parts.append(words[end - 1])
            lines.append("".join(parts))
        start = end
    return lines
```

Greedy packing is required by the contract, so each line boundary is forced.
The quotient-remainder distribution produces equal gaps differing by at most
one and puts every surplus space on the left.

**Complexity:** `O(total output characters)` time and output space.
