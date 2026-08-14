# Focus300 085: LeetCode 601 - Human Traffic of Stadium

**Source:** [LeetCode 601](https://leetcode.com/problems/human-traffic-of-stadium/)  
**Difficulty:** Hard  
**Pattern:** maximal runs of consecutive qualifying IDs

## Exact contract

The source SQL table has unique `id` and `visit_date` columns plus `people`.
Return every row that belongs to a run of at least three consecutive IDs where
each row has `people >= 100`. SQL output may be in any order; these Python
models use `(id, date, people)` tuples and return increasing ID order.

## First principles

Filtering on `people >= 100` is necessary but not sufficient. A row qualifies
only when it belongs to a maximal sequence whose IDs increase by exactly one
and whose length reaches three. Once an ID gap or a low-attendance row appears,
the current sequence cannot connect across it.

## Cases that decide correctness

- Consecutiveness is based on `id`, not calendar dates or input order.
- A run longer than three returns every row in that run.
- Overlapping triples must not duplicate rows.
- A low-attendance row breaks a run even when its neighboring IDs qualify.
- Duplicate IDs or dates violate the source schema and fail fast.

## Brute force: test every row against every triple

```python
from collections.abc import Sequence
from datetime import date


StadiumRow = tuple[int, date, int]


def busy_stadium_rows_brute(records: Sequence[StadiumRow]) -> list[StadiumRow]:
    if any(
        type(row) is not tuple
        or len(row) != 3
        or type(row[0]) is not int
        or type(row[1]) is not date
        or type(row[2]) is not int
        for row in records
    ):
        raise TypeError("each record must be an (int, date, int) tuple")
    if any(row[0] <= 0 or row[2] < 0 for row in records):
        raise ValueError("ids must be positive and people must be non-negative")
    if len({row[0] for row in records}) != len(records) or len(
        {row[1] for row in records}
    ) != len(records):
        raise ValueError("ids and visit dates must be unique")

    rows = sorted(records)
    answer: list[StadiumRow] = []
    for target in rows:
        for index in range(len(rows) - 2):
            window = rows[index : index + 3]
            if (
                [row[0] for row in window]
                == [window[0][0], window[0][0] + 1, window[0][0] + 2]
                and all(row[2] >= 100 for row in window)
                and target in window
            ):
                answer.append(target)
                break
    return answer
```

Every row in a qualifying longer run appears in at least one qualifying
three-row window. Testing all windows for every row takes `O(n^2)` time after
sorting and `O(n)` space.

## Better approach: SQL window functions

In SQL, filter qualifying rows and group them by `id - ROW_NUMBER()`. That
difference is constant exactly within consecutive-ID islands. A window count
or grouped count then retains islands of size at least three.

## Expert solution: emit maximal qualifying runs

```python
from collections.abc import Sequence
from datetime import date


StadiumRow = tuple[int, date, int]


def busy_stadium_rows(records: Sequence[StadiumRow]) -> list[StadiumRow]:
    if any(
        type(row) is not tuple
        or len(row) != 3
        or type(row[0]) is not int
        or type(row[1]) is not date
        or type(row[2]) is not int
        for row in records
    ):
        raise TypeError("each record must be an (int, date, int) tuple")
    if any(row[0] <= 0 or row[2] < 0 for row in records):
        raise ValueError("ids must be positive and people must be non-negative")
    if len({row[0] for row in records}) != len(records) or len(
        {row[1] for row in records}
    ) != len(records):
        raise ValueError("ids and visit dates must be unique")

    answer: list[StadiumRow] = []
    run: list[StadiumRow] = []
    for row in sorted(records):
        if row[2] >= 100 and (not run or row[0] == run[-1][0] + 1):
            run.append(row)
            continue
        if len(run) >= 3:
            answer.extend(run)
        run = [row] if row[2] >= 100 else []
    if len(run) >= 3:
        answer.extend(run)
    return answer
```

The scan maintains exactly the current maximal eligible run and emits it once
when broken. The final check handles a run ending at the last row.

**Complexity:** `O(n log n)` time for sorting and `O(n)` output space; the scan
itself is `O(n)`.
