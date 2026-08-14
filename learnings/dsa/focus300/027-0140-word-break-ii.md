# Focus300 027: LeetCode 140 - Word Break II

**Source:** [LeetCode 140](https://leetcode.com/problems/word-break-ii/)  
**Difficulty:** Hard  
**Pattern:** memoized sentence DAG with suffix-feasibility pruning

## Exact contract

Insert spaces into `s` so every piece is a dictionary word. Return all possible
sentences, using dictionary words any number of times. Dictionary words are
unique and the output order is irrelevant.

## First principles

Every sentence is a path through string indices: an edge `i -> j` exists when
`s[i:j]` is a word. Plain DFS repeats the same suffix subproblem. Memoizing by
start index turns the search into a DAG evaluation, while the unavoidable
output may still be exponential.

A backward boolean DP can first mark suffixes that can reach the end, pruning
edges that cannot participate in any complete sentence.

## Cases that decide correctness

- Words may be reused.
- Different splits can produce identical word counts but different sentences.
- A prefix word is useful only if its remaining suffix is segmentable.
- No solution returns an empty list.
- Output size can be exponential even with optimal memoization.

## Brute force: enumerate every dictionary prefix recursively

```python
def word_break_brute(source: str, word_dict: list[str]) -> list[str]:
    words = set(word_dict)
    answers: list[str] = []
    path: list[str] = []

    def search(start: int) -> None:
        if start == len(source):
            answers.append(" ".join(path))
            return
        for end in range(start + 1, len(source) + 1):
            word = source[start:end]
            if word in words:
                path.append(word)
                search(end)
                path.pop()

    search(0)
    return answers
```

The same impossible and possible suffixes are recomputed exponentially often.

## Better approach: memoize sentences for each suffix

```python
from functools import cache


def word_break_memo(source: str, word_dict: list[str]) -> list[str]:
    words = set(word_dict)

    @cache
    def build(start: int) -> tuple[str, ...]:
        if start == len(source):
            return ("",)
        sentences: list[str] = []
        for end in range(start + 1, len(source) + 1):
            word = source[start:end]
            if word not in words:
                continue
            for suffix in build(end):
                sentences.append(word if not suffix else f"{word} {suffix}")
        return tuple(sentences)

    return list(build(0))
```

Memoization removes repeated suffix searches but still tests every substring
length at each index.

## Expert solution: feasible suffixes and distinct word lengths

```python
from functools import cache


def word_break(source: str, word_dict: list[str]) -> list[str]:
    words = set(word_dict)
    lengths = sorted({len(word) for word in words})
    can_finish = [False] * (len(source) + 1)
    can_finish[-1] = True
    for start in range(len(source) - 1, -1, -1):
        can_finish[start] = any(
            start + length <= len(source)
            and can_finish[start + length]
            and source[start : start + length] in words
            for length in lengths
        )

    @cache
    def build(start: int) -> tuple[str, ...]:
        if start == len(source):
            return ("",)
        sentences: list[str] = []
        for length in lengths:
            end = start + length
            if end > len(source):
                break
            word = source[start:end]
            if word not in words or not can_finish[end]:
                continue
            for suffix in build(end):
                sentences.append(word if not suffix else f"{word} {suffix}")
        return tuple(sentences)

    return list(build(0)) if can_finish[0] else []
```

The feasibility DP prevents the sentence builder from entering any dead suffix,
while memoization shares all productive suffix output.

**Complexity:** `O(nD + output_size)` substring checks for `D` distinct word
lengths, plus returned text space.
