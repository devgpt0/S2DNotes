# 70. Find the Longest Common Prefix

**What you learn:** Comparing string positions.

## Problem

Return the longest starting text shared by every string in a non-empty list.

## Example

```text
Input: words = ["flower", "flow", "flight"]
Output: "fl"
```

## Simple idea

Use the first word as a guide and stop at the first position that does not match every word.

## Python solution

```python
def longest_common_prefix(words: list[str]) -> str:
    if len(words) == 0:
        raise ValueError("words must not be empty")

    first_word = words[0]

    for index in range(len(first_word)):
        character = first_word[index]

        for word in words[1:]:
            if index >= len(word) or word[index] != character:
                return first_word[:index]

    return first_word
```

## Complexity

- Time: `O(number of words × shortest word length)`
- Extra space: `O(1)`

Try to write the solution yourself before reading the code.

