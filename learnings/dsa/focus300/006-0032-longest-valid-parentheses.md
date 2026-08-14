# Focus300 006: LeetCode 32 - Longest Valid Parentheses

**Source:** [LeetCode 32](https://leetcode.com/problems/longest-valid-parentheses/)  
**Difficulty:** Hard  
**Pattern:** balanced-boundary scans and suffix DP

## Exact contract

Given a string containing only `(` and `)`, return the length of its longest
contiguous well-formed parentheses substring.

## First principles

A valid substring never has more closes than opens in any left-to-right prefix
and finishes with equal counts. A left-to-right scan finds valid regions unless
they have unmatched opening parentheses. A symmetric right-to-left scan finds
those missing cases.

Alternatively, `dp[i]` can store the valid suffix ending at `i`; when `s[i]` is
`)`, inspect the character immediately before the previous valid suffix.

## Cases that decide correctness

- The empty string and one-character strings return zero.
- Valid substrings may be nested or adjacent.
- An unmatched close resets a forward scan.
- An unmatched open resets a reverse scan.
- The answer is a contiguous length, not a subsequence length.

## Brute force: validate every even-length substring

```python
def longest_valid_parentheses_brute(parentheses: str) -> int:
    answer = 0
    for left in range(len(parentheses)):
        balance = 0
        for right in range(left, len(parentheses)):
            balance += 1 if parentheses[right] == "(" else -1
            if balance < 0:
                break
            if balance == 0:
                answer = max(answer, right - left + 1)
    return answer
```

This takes `O(n^2)` time and `O(1)` space.

## Better approach: longest valid suffix DP

```python
def longest_valid_parentheses_dp(parentheses: str) -> int:
    dynamic = [0] * len(parentheses)
    answer = 0
    for index in range(1, len(parentheses)):
        if parentheses[index] != ")":
            continue
        if parentheses[index - 1] == "(":
            dynamic[index] = 2 + (dynamic[index - 2] if index >= 2 else 0)
        else:
            previous_length = dynamic[index - 1]
            opening = index - previous_length - 1
            if opening >= 0 and parentheses[opening] == "(":
                dynamic[index] = previous_length + 2
                if opening:
                    dynamic[index] += dynamic[opening - 1]
        answer = max(answer, dynamic[index])
    return answer
```

This is `O(n)` time and `O(n)` space.

## Expert solution: two directional balance scans

```python
def longest_valid_parentheses(parentheses: str) -> int:
    answer = 0
    opens = 0
    closes = 0
    for character in parentheses:
        opens += character == "("
        closes += character == ")"
        if opens == closes:
            answer = max(answer, 2 * closes)
        elif closes > opens:
            opens = 0
            closes = 0

    opens = 0
    closes = 0
    for character in reversed(parentheses):
        opens += character == "("
        closes += character == ")"
        if opens == closes:
            answer = max(answer, 2 * opens)
        elif opens > closes:
            opens = 0
            closes = 0
    return answer
```

The two scans cover both possible unmatched-boundary directions without storing
per-index state.

**Complexity:** `O(n)` time and `O(1)` space.
