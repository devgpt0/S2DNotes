# ICPC300 082: CSES - Movie Festival Queries

**Source:** [CSES - Movie Festival Queries](https://cses.fi/problemset/task/1664/)  
**Pattern:** interval scheduling + binary lifting  
**Goal:** For each time range `[start, end]`, find the maximum number of
non-overlapping movies that fit completely inside it.

## 1. First principles

For one query, the optimal interval-scheduling rule is to repeatedly select the
eligible movie with the earliest ending time. The next choice depends only on
the previous ending time.

Precompute that greedy successor for every movie. Binary lifting then jumps
through `1, 2, 4, ...` greedy choices while the final movie still ends within
the query.

## 2. Cases that decide correctness

- A movie may start exactly when the previous movie ends.
- A movie ending after the query boundary is unusable.
- No eligible first movie produces `0`.
- Nested movies require choosing the earlier ending one.
- Queries need not align with movie endpoints.

## 3. Brute force: try every possible next movie

```python
def movie_festival_queries_brute(
    movies: list[tuple[int, int]], queries: list[tuple[int, int]]
) -> list[int]:
    if any(start >= end for start, end in movies):
        raise ValueError("every movie must have start < end")

    answers: list[int] = []
    for query_start, query_end in queries:

        def search(current_time: int) -> int:
            best = 0
            for start, end in movies:
                if start >= current_time and end <= query_end:
                    best = max(best, 1 + search(end))
            return best

        answers.append(search(query_start))
    return answers
```

**Complexity:** exponential time per query and `O(n)` recursion space.

## 4. Better: run the greedy scan per query

Sort movies by ending time. Each query scans that order and accepts every movie
that starts after the current time and ends within the query.

```python
def movie_festival_queries_greedy(
    movies: list[tuple[int, int]], queries: list[tuple[int, int]]
) -> list[int]:
    if any(start >= end for start, end in movies):
        raise ValueError("every movie must have start < end")

    by_end = sorted(movies, key=lambda movie: movie[1])
    answers: list[int] = []
    for query_start, query_end in queries:
        current_time = query_start
        watched = 0
        for start, end in by_end:
            if start >= current_time and end <= query_end:
                watched += 1
                current_time = end
        answers.append(watched)
    return answers
```

**Complexity:** `O(n log n + nq)` time and `O(n)` space.

## 5. Expert solution: greedy successor doubling

For movies sorted by start, a suffix minimum finds the earliest-ending movie
whose start is at least a given time. Doubling tables compose those choices.

```python
from bisect import bisect_left


def movie_festival_queries_binary_lifting(
    movies: list[tuple[int, int]], queries: list[tuple[int, int]]
) -> list[int]:
    if any(start >= end for start, end in movies):
        raise ValueError("every movie must have start < end")
    if not movies:
        return [0] * len(queries)

    ordered = sorted(movies)
    starts = [start for start, _ in ordered]
    ends = [end for _, end in ordered]
    best_suffix = [0] * len(ordered)
    best_suffix[-1] = len(ordered) - 1
    for index in range(len(ordered) - 2, -1, -1):
        candidate = best_suffix[index + 1]
        best_suffix[index] = index if ends[index] <= ends[candidate] else candidate

    def first_movie(time: int) -> int:
        index = bisect_left(starts, time)
        return -1 if index == len(ordered) else best_suffix[index]

    level_count = max(1, len(ordered).bit_length())
    jump = [[-1] * len(ordered) for _ in range(level_count)]
    for movie in range(len(ordered)):
        jump[0][movie] = first_movie(ends[movie])
    for level in range(1, level_count):
        for movie in range(len(ordered)):
            middle = jump[level - 1][movie]
            if middle != -1:
                jump[level][movie] = jump[level - 1][middle]

    answers: list[int] = []
    for query_start, query_end in queries:
        movie = first_movie(query_start)
        if movie == -1 or ends[movie] > query_end:
            answers.append(0)
            continue

        watched = 1
        for level in range(level_count - 1, -1, -1):
            candidate = jump[level][movie]
            if candidate != -1 and ends[candidate] <= query_end:
                watched += 1 << level
                movie = candidate
        answers.append(watched)
    return answers
```

### Why the expert code is correct

Earliest finish is the standard exchange-optimal first choice. Each jump table
entry applies that same choice repeatedly, so the largest jumps fitting before
the query end count exactly the greedy optimum.

**Complexity:** `O((n + q) log n)` time and `O(n log n)` space.

## 6. What to remember

```text
maximum compatible intervals -> earliest finish greedily
many time-range queries -> precompute greedy successor
repeat successors quickly -> binary lifting
```
