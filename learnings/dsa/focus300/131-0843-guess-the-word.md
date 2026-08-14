# Focus300 131: LeetCode 843 - Guess the Word

**Source:** [LeetCode 843](https://leetcode.com/problems/guess-the-word/)  
**Difficulty:** Hard  
**Pattern:** minimax partitioning in an interactive search

## Exact contract

A hidden six-letter lowercase word belongs to a unique list of at most 100
words. Calling `guess(word)` returns the number of positions matching the
hidden word. Find the hidden word within at most ten calls. The functions below
return the discovered word; an inconsistent judge response fails immediately.

## First principles

Each guess partitions the remaining candidates into seven buckets by match
count `0..6`. After the response, only its bucket can contain the secret. A
minimax guess chooses the partition whose largest bucket is smallest, directly
limiting the worst possible remaining search space.

## Cases that decide correctness

- Matches compare equal positions, not shared letters.
- Guesses must come from the supplied word list.
- A response of six identifies the exact secret.
- A response that eliminates every candidate is inconsistent.
- Repeating a previous guess wastes the strict ten-call budget.

## Brute force: guess candidates sequentially

```python
from collections.abc import Callable


def guess_word_brute(words: list[str], guess: Callable[[str], int]) -> str:
    if type(words) is not list or any(
        type(word) is not str
        or len(word) != 6
        or any(not "a" <= character <= "z" for character in word)
        for word in words
    ):
        raise TypeError("words must be a list of six-letter lowercase strings")
    if not 1 <= len(words) <= 100 or len(set(words)) != len(words):
        raise ValueError("words must contain 1..100 unique entries")
    if not callable(guess):
        raise TypeError("guess must be callable")

    for word in words:
        response = guess(word)
        if type(response) is not int or not 0 <= response <= 6:
            raise ValueError("guess responses must be integers from 0 through 6")
        if response == 6:
            return word
    raise RuntimeError("the judge did not identify a listed secret")
```

This uses up to `n` calls, so it is executable as a baseline but does not meet
the source's ten-call constraint for large lists.

## Better approach: choose the most balanced expected partition

Entropy maximization favors small average buckets when secrets are assumed
uniform. Minimax is safer for the interactive contract because it optimizes
the largest bucket rather than relying on a probability distribution.

## Expert solution: minimize the worst response bucket

```python
from collections import Counter
from collections.abc import Callable


def guess_word(words: list[str], guess: Callable[[str], int]) -> str:
    if type(words) is not list or any(
        type(word) is not str
        or len(word) != 6
        or any(not "a" <= character <= "z" for character in word)
        for word in words
    ):
        raise TypeError("words must be a list of six-letter lowercase strings")
    if not 1 <= len(words) <= 100 or len(set(words)) != len(words):
        raise ValueError("words must contain 1..100 unique entries")
    if not callable(guess):
        raise TypeError("guess must be callable")

    def match_count(first: str, second: str) -> int:
        return sum(left == right for left, right in zip(first, second, strict=True))

    remaining = words.copy()
    unused = set(words)
    for _ in range(10):
        if not remaining or not unused:
            raise RuntimeError("judge responses are inconsistent with the word list")
        remaining_set = set(remaining)
        candidate = min(
            unused,
            key=lambda word: (
                max(Counter(match_count(word, other) for other in remaining).values()),
                word not in remaining_set,
                word,
            ),
        )
        unused.remove(candidate)
        response = guess(candidate)
        if type(response) is not int or not 0 <= response <= 6:
            raise ValueError("guess responses must be integers from 0 through 6")
        if response == 6:
            return candidate
        remaining = [
            word for word in remaining if match_count(candidate, word) == response
        ]
    raise RuntimeError("secret was not found within the ten-call limit")
```

Every response retains exactly one partition bucket. Choosing the smallest
worst bucket maximizes deterministic progress under adversarial responses.

**Complexity:** `O(g n^3)` character comparisons for at most `g = 10` guesses
and `n <= 100`; `O(n)` auxiliary space.
