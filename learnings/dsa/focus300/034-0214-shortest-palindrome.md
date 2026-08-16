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


## Classroom board: turn a range into two prefixes

```text
a subarray sum becomes prefix[right] - prefix[left], so one prefix table
replaces many repeated range scans.
```



## Step-by-step transformation

1. Compress the input into counts, prefixes, bit masks, or another compact state.
2. Update that state once per element instead of recomputing earlier work.
3. Combine the stored pieces to recover the value the problem asks for.
4. Return the final count, sum, or constructed answer.

These notes transform input into output by reducing the data to a compact invariant first, then rebuilding the answer from that invariant.


## Diagram: compress the input first

```text

            raw values
                |
                v
            counts / prefix / bit state
                |
                v
            combine stored facts
                |
                v
            final answer
```

The algorithm first compresses the input into a small invariant, then rebuilds the answer from that compact state.

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

