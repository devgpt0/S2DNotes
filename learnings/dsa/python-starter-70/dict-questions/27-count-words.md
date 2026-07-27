# 27. Count Words in a Sentence

**What you learn:** Dictionary frequency counting.

## Problem

Count how many times each whitespace-separated word appears in a sentence.

## Example

```text
Input: sentence = "go fast go"
Output: {"go": 2, "fast": 1}
```

## Simple idea

Split the sentence into words and store each word's count in a dictionary.

## Python solution

```python
def count_words(sentence: str) -> dict[str, int]:
    counts: dict[str, int] = {}

    for word in sentence.split():
        if word in counts:
            counts[word] = counts[word] + 1
        else:
            counts[word] = 1

    return counts
```

## Complexity

- Time: `O(n)`
- Extra space: `O(n)`

Try to write the solution yourself before reading the code.

