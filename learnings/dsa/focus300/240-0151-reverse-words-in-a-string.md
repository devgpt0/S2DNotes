# Focus300 240: LeetCode 151 - Reverse Words in a String

**Source:** [LeetCode 151](https://leetcode.com/problems/reverse-words-in-a-string/)  
**Difficulty:** Medium  
**Pattern:** token normalization and reversal

## Exact contract

Reverse the order of the words in the string while collapsing extra whitespace.

## First principles

The words are the semantic units; repeated spaces are just separators. Once the words are extracted, reversing their order is trivial.

## Cases that decide correctness

- Leading and trailing spaces disappear.
- Multiple spaces between words collapse to one separator.
- A one-word string remains that word.
- The output words are reversed, not the letters inside each word.

## Brute force

```python
def reverse_words_brute(s):
    return " ".join(reversed(s.split()))
```

Build every possible substring and test which ones are words.

## Better insight

Split on whitespace, reverse the token list, and rejoin with single spaces.

## Expert solution

```python
def reverse_words(s):
    return " ".join(reversed(s.split()))
```

Normalize the whitespace, extract the words, reverse their order, and emit the cleaned string.

**Complexity:** O(n) time and O(n) space.
