# ICPC300 176: Codeforces 896A - Nephren gives a riddle

**Source:** [Codeforces 896A - Nephren gives a riddle](https://codeforces.com/problemset/problem/896/A)  
**Pattern:** capped recursive lengths and indexed descent

## Exact contract

Let:

```text
F(0) = What are you doing at the end of the world? Are you busy? Will you save us?
F(n) = What are you doing while sending " + F(n-1)
       + "? Are you busy? Will you send " + F(n-1) + "?
```

For every query `(n, k)`, return the one-based character `k` of `F(n)`, or
`.` when `k` exceeds its length. Levels can reach `100_000`, so constructing
the strings is impossible.

## First principles

The length recurrence is `L[n] = 2L[n-1] + constant`. Cap lengths above the
largest queried index: larger exact values cannot change any branch decision.
To locate one character, compare its zero-based index with the five consecutive
pieces `prefix`, `F(n-1)`, `middle`, `F(n-1)`, and `suffix`.

## Cases that decide correctness

- Query positions are one-based; internal indices are zero-based.
- Quotes, question marks, and spaces are characters.
- A capped child length means every relevant query lies inside that child.
- Large levels begin with many copies of `prefix`; skip them arithmetically.
- `k` beyond the exact level-zero string returns `.`.

## Brute force: construct the recursive text

```python
BASE = "What are you doing at the end of the world? Are you busy? Will you save us?"
PREFIX = 'What are you doing while sending "'
MIDDLE = '"? Are you busy? Will you send "'
SUFFIX = '"?'


def nephren_characters_brute(queries: list[tuple[int, int]]) -> str:
    if not queries or any(
        type(level) is not int or type(position) is not int or level < 0 or position < 1
        for level, position in queries
    ):
        raise ValueError(
            "queries must contain nonnegative levels and positive positions"
        )

    texts = [BASE]
    for _ in range(max(level for level, _ in queries)):
        previous = texts[-1]
        texts.append(PREFIX + previous + MIDDLE + previous + SUFFIX)

    return "".join(
        texts[level][position - 1] if position <= len(texts[level]) else "."
        for level, position in queries
    )
```

The text length doubles at every level, restricting construction to tiny
levels.

## Better approach: no separate intermediate

Memoizing complete recursive strings still has exponential output size.
Memoizing only their capped lengths and descending by index is already the
expert method below, so there is no distinct intermediate algorithm.

## Expert solution: capped lengths and iterative descent

```python
BASE = "What are you doing at the end of the world? Are you busy? Will you save us?"
PREFIX = 'What are you doing while sending "'
MIDDLE = '"? Are you busy? Will you send "'
SUFFIX = '"?'


def nephren_characters(queries: list[tuple[int, int]]) -> str:
    if not queries or any(
        type(level) is not int or type(position) is not int or level < 0 or position < 1
        for level, position in queries
    ):
        raise ValueError(
            "queries must contain nonnegative levels and positive positions"
        )

    maximum_level = max(level for level, _ in queries)
    cap = max(position for _, position in queries) + 1
    lengths = [len(BASE)]
    saturated_level: int | None = None
    for level in range(1, maximum_level + 1):
        length = min(
            cap,
            len(PREFIX) + lengths[-1] + len(MIDDLE) + lengths[-1] + len(SUFFIX),
        )
        lengths.append(length)
        if length == cap and saturated_level is None:
            saturated_level = level

    answer: list[str] = []
    for level, one_based_position in queries:
        index = one_based_position - 1

        if saturated_level is not None and level > saturated_level:
            repeated_prefixes = level - saturated_level
            prefix_span = repeated_prefixes * len(PREFIX)
            if index < prefix_span:
                answer.append(PREFIX[index % len(PREFIX)])
                continue
            index -= prefix_span
            level = saturated_level

        while level:
            if index < len(PREFIX):
                answer.append(PREFIX[index])
                break
            index -= len(PREFIX)

            child_length = lengths[level - 1]
            if index < child_length:
                level -= 1
                continue
            index -= child_length

            if index < len(MIDDLE):
                answer.append(MIDDLE[index])
                break
            index -= len(MIDDLE)

            if index < child_length:
                level -= 1
                continue
            index -= child_length

            if index < len(SUFFIX):
                answer.append(SUFFIX[index])
            else:
                answer.append(".")
            break
        else:
            answer.append(BASE[index] if index < len(BASE) else ".")

    return "".join(answer)
```

Every comparison removes one complete piece preceding the requested character.
The remaining index is therefore always relative to the selected piece. The
large-level shortcut performs the same first-child descents in one operation.

**Complexity:** `O(max_level + q log(max_k))` time and `O(max_level)` space;
the per-query descent reaches only the unsaturated length levels.
