# Focus300 054: LeetCode 336 - Palindrome Pairs

**Source:** [LeetCode 336 - Palindrome Pairs](https://leetcode.com/problems/palindrome-pairs/)  
**Difficulty:** Hard  
**Pattern:** palindromic split plus reversed-word lookup  

## Exact contract

Given unique strings, return every ordered pair of distinct indices `(i, j)`
such that `words[i] + words[j]` is a palindrome. The implementation returns
pairs in sorted order.

## First principles

Split a word into `prefix + suffix`. If the prefix is already palindromic, a
word equal to `reverse(suffix)` can be placed on the left. If the suffix is
palindromic, `reverse(prefix)` can be placed on the right. Every palindromic
concatenation has one of these alignments.

## Cases that decide correctness

- Pair order matters.
- The empty string pairs with every nonempty palindrome in both orders.
- A word cannot pair with itself.
- Splitting after the final character needs one duplicate guard.
- Source words are unique, enabling one index per reverse lookup.

## Brute force: test every ordered pair

```python
def palindrome_pairs_brute(words: list[str]) -> list[tuple[int, int]]:
    if any(not isinstance(word, str) for word in words) or len(set(words)) != len(
        words
    ):
        raise ValueError("words must be unique strings")
    result = []
    for first, first_word in enumerate(words):
        for second, second_word in enumerate(words):
            if first == second:
                continue
            combined = first_word + second_word
            if combined == combined[::-1]:
                result.append((first, second))
    return result
```

**Complexity:** `O(w^2 L)` time and `O(L)` temporary space.

## Better approach: trie of reversed words

A reversed-word trie can report compatible suffixes during one traversal per
word. It achieves the same `O(total characters + output)` target with more
state; split lookup is shorter and equally precise for unique words.

## Expert solution: enumerate all palindromic splits

```python
def palindrome_pairs(words: list[str]) -> list[tuple[int, int]]:
    if any(not isinstance(word, str) for word in words) or len(set(words)) != len(
        words
    ):
        raise ValueError("words must be unique strings")
    index_by_word = {word: index for index, word in enumerate(words)}
    pairs: set[tuple[int, int]] = set()
    for index, word in enumerate(words):
        for split in range(len(word) + 1):
            prefix = word[:split]
            suffix = word[split:]
            if prefix == prefix[::-1]:
                left = index_by_word.get(suffix[::-1])
                if left is not None and left != index:
                    pairs.add((left, index))
            if split != len(word) and suffix == suffix[::-1]:
                right = index_by_word.get(prefix[::-1])
                if right is not None and right != index:
                    pairs.add((index, right))
    return sorted(pairs)
```

For any valid pair, the unmatched part of one word must equal the reverse of
the other word, while its overhanging part is palindromic. The two split tests
enumerate exactly those two orientations.

**Complexity:** `O(w L^2 + output)` time with Python slicing and `O(w L)`
lookup space.

