# 57. Reverse Word Order

**What you learn:** Splitting and joining strings.

## Problem

Return a sentence with its word order reversed.

## Example

```text
Input: sentence = "learn python today"
Output: "today python learn"
```

## Simple idea

Split the sentence into words, reverse the words, and join them with spaces.

## Python solution

```python
def reverse_words(sentence: str) -> str:
    words = sentence.split()
    words.reverse()
    return " ".join(words)
```

## Complexity

- Time: `O(n)`
- Extra space: `O(n)`

Try to write the solution yourself before reading the code.

