# ICPC300 069: CSES - String Removals

**Source:** [CSES - String Removals](https://cses.fi/problemset/task/1149/)  
**Pattern:** distinct-subsequence DP with last occurrences  
**Goal:** Count, modulo `1_000_000_007`, the different nonempty strings that
can be obtained by deleting zero or more characters without reordering the
remaining characters.

## 1. Problem in plain words

Different deletion choices may produce the same string and must be counted
once. For `aaa`, the distinct nonempty results are `a`, `aa`, and `aaa`, so the
answer is `3`, not `7`.

## 2. First principles

Let `dp[i]` count distinct subsequences of the first `i` characters, including
the empty string. Appending character `c` appears to double the set: every old
subsequence either excludes `c` or appends `c`.

If the previous occurrence of `c` was at one-based position `j`, the appended
subsequences formed from prefixes before `j` were already created using that
older `c`. Exactly `dp[j-1]` results are duplicates. Thus:

`dp[i] = 2*dp[i-1] - dp[j-1]` when `c` appeared before.

Subtract one at the end to exclude the empty subsequence.

## 3. Cases that decide correctness

| Case | Required result |
| --- | --- |
| One character | `1`. |
| All characters distinct | `2^n - 1`. |
| All characters equal | `n`. |
| Character repeats after a gap | Subtract subsequences before its prior position. |
| Modular subtraction becomes negative | Normalize with `% MODULO`. |

## 4. Brute force: enumerate deletion masks

```python
MODULO = 1_000_000_007


def count_distinct_subsequences_brute_force(text: str) -> int:
    if not text:
        raise ValueError("text must be nonempty")
    subsequences = {
        "".join(
            character for index, character in enumerate(text) if mask & (1 << index)
        )
        for mask in range(1, 1 << len(text))
    }
    return len(subsequences) % MODULO
```

**Complexity:** `O(n 2^n)` time and up to `O(n 2^n)` stored characters.

## 5. Better for small repeated inputs: update the distinct set directly

This avoids revisiting all masks and merges equal strings after every
character, but the set can still have exponential size.

```python
MODULO = 1_000_000_007


def count_distinct_subsequences_set_dp(text: str) -> int:
    if not text:
        raise ValueError("text must be nonempty")
    subsequences = {""}
    for character in text:
        subsequences |= {subsequence + character for subsequence in subsequences}
    return (len(subsequences) - 1) % MODULO
```

**Complexity:** proportional to the total characters in all distinct
subsequences, exponential in the worst case.

## 6. Expert solution: subtract the previous duplicate block

```python
MODULO = 1_000_000_007


def count_distinct_subsequences(text: str) -> int:
    if not text:
        raise ValueError("text must be nonempty")

    dp = [0] * (len(text) + 1)
    dp[0] = 1
    last_position: dict[str, int] = {}

    for position, character in enumerate(text, start=1):
        dp[position] = 2 * dp[position - 1]
        if character in last_position:
            previous = last_position[character]
            dp[position] -= dp[previous - 1]
        dp[position] %= MODULO
        last_position[character] = position

    return (dp[-1] - 1) % MODULO
```

### Why the expert code is correct

- Excluding or appending the new character initially creates two copies of
  every old distinct subsequence.
- Results duplicated by a previous equal character are exactly those formed by
  appending it to subsequences available before that previous occurrence.
- There are `dp[previous-1]` such strings, so the subtraction removes each
  duplicate once and no unique result.
- The DP includes the empty string throughout; the final subtraction removes
  only that source-excluded result.

**Complexity:** `O(n)` expected time and `O(n + alphabet_size)` memory.

## 7. What to remember

Distinct-subsequence DP doubles on every new character, then subtracts the
subsequence set that the previous equal character already generated.
