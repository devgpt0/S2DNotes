# ICPC300 277: Codeforces 1336C - Kaavi and Magic Spell

**Source:** [Codeforces 1336C](https://codeforces.com/problemset/problem/1336/C)  
**Difficulty:** 2200  
**Pattern:** interval DP for adding ordered characters at either end

## Exact contract

Take a prefix of string `s`. Process its characters in order, placing each at
the left or right end of the current string. Count operation histories whose
result begins with string `t`, modulo `998244353`. Left and right are distinct
choices even for the first character.

## First principles

After using `length` characters, imagine the built string occupying an
interval `[l,r]` of a length-`|s|` target padded with unconstrained positions
after `t`. The next character `s[length]` can extend left if it matches `t[l]`
or `l` is padded; it can extend right under the analogous condition.

`dp[l][r]` counts both construction directions. Any state beginning at zero
and having length at least `|t|` is a valid stopping point.

## Cases that decide correctness

- The first insertion contributes two operation histories.
- Positions at or beyond `|t|` accept any character.
- Characters of `s` are consumed strictly from left to right.
- Valid prefix lengths range from `|t|` through `|s|`.
- If `|t|>|s|`, the answer is zero.

## Brute force: enumerate every prefix and left/right history

```python
from collections import deque


MODULUS = 998_244_353


def kaavi_magic_brute(source: str, target: str) -> int:
    answer = 0
    for length in range(len(target), len(source) + 1):
        for choices in range(1 << length):
            built: deque[str] = deque()
            for index, character in enumerate(source[:length]):
                if choices >> index & 1:
                    built.appendleft(character)
                else:
                    built.append(character)
            answer += "".join(built).startswith(target)
    return answer % MODULUS
```

This takes `O(n 2^n)` time.

## Better insight: reverse the construction into interval expansion

The characters already placed are always contiguous in the padded target.
Their exact string need not be stored; the interval endpoints determine both
possible next matches.

## Expert solution: quadratic interval DP

```python
import sys


MODULUS = 998_244_353


def solve() -> None:
    input_stream = sys.stdin.buffer
    source = input_stream.readline().strip().decode()
    target = input_stream.readline().strip().decode()
    source_length = len(source)
    target_length = len(target)
    if target_length > source_length:
        print(0)
        return

    dynamic = [[0] * source_length for _ in range(source_length)]
    for position in range(source_length):
        if position >= target_length or source[0] == target[position]:
            dynamic[position][position] = 2

    for length in range(2, source_length + 1):
        character = source[length - 1]
        for left in range(source_length - length + 1):
            right = left + length - 1
            value = 0
            if left >= target_length or character == target[left]:
                value += dynamic[left + 1][right]
            if right >= target_length or character == target[right]:
                value += dynamic[left][right - 1]
            dynamic[left][right] = value % MODULUS

    answer = sum(dynamic[0][right] for right in range(target_length - 1, source_length))
    print(answer % MODULUS)


if __name__ == "__main__":
    solve()
```

Every operation history has one unique occupied interval after each prefix,
and both legal endpoint extensions are counted exactly once.

**Complexity:** `O(n^2)` time and space.
