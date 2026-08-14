# Focus300 034: LeetCode 214 - Shortest Palindrome

**Source:** [LeetCode 214 - Shortest Palindrome](https://leetcode.com/problems/shortest-palindrome/)  
**Difficulty:** Hard  
**Pattern:** longest palindromic prefix through prefix-function matching  

## Exact contract

Given a string, add characters only in front so the result is a palindrome.
Return the shortest possible result.

## First principles

Any untouched prefix of the final palindrome must already be a palindromic
prefix of the input. Once the longest such prefix is known, the remaining
suffix must be mirrored in front, and that construction is uniquely shortest.

## Cases that decide correctness

- Empty and one-character strings need no addition.
- The whole string may already be a palindrome.
- Repeated characters create overlapping candidate borders.
- The separator used by matching must not equal any string character.
- Only a prefix palindrome matters; an internal palindrome does not help.

## Brute force: test prefixes from longest to shortest

```python
def shortest_palindrome_brute(text: str) -> str:
    if not isinstance(text, str):
        raise ValueError("text must be a string")
    for prefix_length in range(len(text), -1, -1):
        prefix = text[:prefix_length]
        if prefix == prefix[::-1]:
            return text[prefix_length:][::-1] + text
    raise RuntimeError("the empty prefix is always palindromic")
```

**Complexity:** `O(n^2)` time and `O(n)` temporary space.

## Better approach: rolling hashes

Forward and reverse prefix hashes can locate the longest palindromic prefix in
`O(n)` expected time. Exact collision handling still needs verification, while
the prefix function gives a deterministic result.

## Expert solution: KMP prefix function against the reversed string

```python
def shortest_palindrome(text: str) -> str:
    if not isinstance(text, str):
        raise ValueError("text must be a string")
    separator = object()
    sequence: list[object] = [*text, separator, *reversed(text)]
    prefix = [0] * len(sequence)
    for index in range(1, len(sequence)):
        matched = prefix[index - 1]
        while matched and sequence[index] != sequence[matched]:
            matched = prefix[matched - 1]
        if sequence[index] == sequence[matched]:
            matched += 1
        prefix[index] = matched
    palindromic_prefix = prefix[-1] if prefix else 0
    return text[palindromic_prefix:][::-1] + text
```

The final prefix-function value is the longest prefix of `text` matching a
suffix of `reversed(text)`, exactly the longest palindromic prefix. Mirroring
everything after it is necessary and sufficient.

**Complexity:** `O(n)` time and `O(n)` space.

