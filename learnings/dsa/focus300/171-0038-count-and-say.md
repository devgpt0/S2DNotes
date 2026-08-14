# Focus300 171: LeetCode 38 - Count and Say

**Source:** [LeetCode 38](https://leetcode.com/problems/count-and-say/)  
**Difficulty:** Medium  
**Pattern:** run-length transformation

## Exact contract

The sequence starts with `count_and_say(1) = "1"`. Each later term describes
the consecutive equal-digit runs of the previous term as `count` followed by
`digit`. Given `1 <= n <= 30`, return the `n`th term.

## First principles

Only adjacent equal digits form one run. Scan left to right, find the first
different digit, emit the run length and digit, and continue from that boundary.
Applying this deterministic transformation `n - 1` times produces the answer.

## Cases that decide correctness

- `n = 1` returns the seed without transformation.
- Runs end at either a different digit or the end of the string.
- Equal digits separated by another digit belong to different runs.
- Run lengths may contain more than one decimal digit.
- Counts describe the previous term, never the partially built next term.

## Brute force: recursive terms with repeated concatenation

```python
def count_and_say_brute(term: int) -> str:
    if not 1 <= term <= 30:
        raise ValueError("term must be between 1 and 30")
    if term == 1:
        return "1"

    previous = count_and_say_brute(term - 1)
    answer = ""
    start = 0
    for index in range(1, len(previous) + 1):
        if index == len(previous) or previous[index] != previous[start]:
            answer += str(index - start) + previous[start]
            start = index
    return answer
```

The recursion retains prior terms, and repeated immutable-string concatenation
can make building a term quadratic in its length.

## Better transition: collect output fragments

Each term depends only on the preceding term. Build run descriptions in a list,
join once, and iterate so no recursion or repeated full-string copy is needed.

## Expert solution: iterative run-length encoding

```python
def count_and_say(term: int) -> str:
    if not 1 <= term <= 30:
        raise ValueError("term must be between 1 and 30")

    current = "1"
    for _ in range(term - 1):
        pieces: list[str] = []
        start = 0
        for index in range(1, len(current) + 1):
            if index == len(current) or current[index] != current[start]:
                pieces.append(str(index - start))
                pieces.append(current[start])
                start = index
        current = "".join(pieces)
    return current
```

Every character of every generated term is read once and written once.

**Complexity:** `O(total generated characters)` time and `O(length of the final
term)` working space.
