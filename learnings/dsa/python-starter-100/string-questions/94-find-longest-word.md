# 94. Find the Longest Word

**What you learn:** Tracking the best value.

## Problem

Return the first longest word in a non-empty sentence.

## Example

```text
Input: text = "learn data structures daily"
Output: "structures"
```

## Simple idea

Split into words and replace the answer only when a strictly longer word appears.

## Python solution

```python
def find_longest_word(text: str) -> str:
    words = text.split()
    if len(words) == 0:
        raise ValueError("text must contain at least one word")

    longest = words[0]
    for word in words[1:]:
        if len(word) > len(longest):
            longest = word
    return longest
```

## Complexity

- Time: `O(n)`
- Extra space: `O(n)`

Try to write the solution yourself before reading the code.
