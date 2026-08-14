# Focus300 110: LeetCode 761 - Special Binary String

**Source:** [LeetCode 761](https://leetcode.com/problems/special-binary-string/)  
**Difficulty:** Hard  
**Pattern:** recursive canonicalization of balanced blocks

## Exact contract

A binary string is special when it contains equally many `1` and `0` characters
and every prefix has at least as many `1` characters as `0` characters. Given a
special string, repeatedly swap adjacent non-empty special substrings in any
order. Return the lexicographically largest reachable string.

## First principles

Interpret `1` as an opening parenthesis and `0` as a closing parenthesis. Every
special string uniquely splits into top-level primitive special blocks. Blocks
may be swapped freely, so sort their recursively maximized forms in descending
order. The same rule applies independently inside each primitive block.

## Cases that decide correctness

- The whole input and every movable block must be special.
- A balance of zero marks the end of one top-level primitive block.
- Nested content must be maximized before sibling blocks are sorted.
- Equal blocks are harmless; duplicates remain present.
- Lexicographic descending order places the best block first.

## Brute force: explore every legal adjacent swap

```python
def make_largest_special_brute(text: str) -> str:
    if not text or any(character not in "01" for character in text):
        raise ValueError("text must be a non-empty binary string")

    def is_special(candidate: str) -> bool:
        balance = 0
        for character in candidate:
            balance += 1 if character == "1" else -1
            if balance < 0:
                return False
        return balance == 0

    if not is_special(text):
        raise ValueError("text must be special")
    seen = {text}
    stack = [text]
    while stack:
        current = stack.pop()
        for left in range(len(current) - 1):
            for middle in range(left + 1, len(current)):
                if not is_special(current[left:middle]):
                    continue
                for right in range(middle + 1, len(current) + 1):
                    if not is_special(current[middle:right]):
                        continue
                    candidate = (
                        current[:left]
                        + current[middle:right]
                        + current[left:middle]
                        + current[right:]
                    )
                    if candidate not in seen:
                        seen.add(candidate)
                        stack.append(candidate)
    return max(seen)
```

The reachable-state graph can be exponential, and testing all adjacent
substring pairs adds a polynomial factor per state.

## Better solution: recursively sort primitive blocks

```python
def make_largest_special_recursive(text: str) -> str:
    if not text or any(character not in "01" for character in text):
        raise ValueError("text must be a non-empty binary string")

    def normalize(segment: str) -> str:
        balance = 0
        start = 0
        blocks: list[str] = []
        for index, character in enumerate(segment):
            balance += 1 if character == "1" else -1
            if balance < 0:
                raise ValueError("text must be special")
            if balance == 0:
                inner = normalize(segment[start + 1 : index])
                blocks.append("1" + inner + "0")
                start = index + 1
        if balance != 0:
            raise ValueError("text must be special")
        return "".join(sorted(blocks, reverse=True))

    return normalize(text)
```

This follows the proof directly, but recursive slicing rebuilds nested strings.

## Expert solution: bottom-up block stack

```python
def make_largest_special(text: str) -> str:
    if not text or any(character not in "01" for character in text):
        raise ValueError("text must be a non-empty binary string")

    frames: list[list[str]] = [[]]
    for character in text:
        if character == "1":
            frames.append([])
        else:
            if len(frames) == 1:
                raise ValueError("text must be special")
            children = frames.pop()
            block = "1" + "".join(sorted(children, reverse=True)) + "0"
            frames[-1].append(block)
    if len(frames) != 1:
        raise ValueError("text must be special")
    return "".join(sorted(frames[0], reverse=True))
```

Each stack frame holds the already maximized primitive children of one open
block. Closing that block sorts its children once and appends its canonical form
to the parent, exactly reproducing the recursive decomposition without slicing.

**Complexity:** `O(n^2 log n)` worst-case time including string comparisons and
concatenation, and `O(n^2)` worst-case stored characters across nested frames.
