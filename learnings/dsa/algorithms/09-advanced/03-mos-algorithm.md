# Mo's Algorithm

## Idea

Mo's algorithm answers offline range queries by sorting them so the current
range moves only a small distance between queries.

## Visual model

```text
sort by left block, then by right endpoint
move current [left, right) one position at a time, adding/removing values
```

## Classroom board: reuse a nearby range

```text
current answer is for [2,7)
next sorted query is [3,9)
remove index 2; add indexes 7 and 8
update answer in three O(1) moves instead of rebuilding seven values
```

## Steps

1. Choose block size near `sqrt(n)`.
2. Sort queries by left block and alternating right direction.
3. Maintain a current half-open range and its answer.
4. Move endpoints with `add` and `remove` operations.
5. Store each result at its original query index.

## First-principles derivation

Answering each static range query from scratch repeats almost the same work.
Reorder queries so consecutive ranges move their boundaries only a short
distance, updating one element at a time.

The maintained data structure always describes exactly the current half-open
range `[left,right)`.

## Classroom board: reuse one range

Array is `[1,2,1,3]`; answer is the number of distinct values.

```text
start current [0,0): {}                 distinct 0

query [0,3):
add index 0 -> {1:1}
add index 1 -> {1:1,2:1}
add index 2 -> {1:2,2:1}                answer 2

next query [1,4):
remove index 0 -> {1:1,2:1}
add index 3    -> {1:1,2:1,3:1}         answer 3
```

Only two boundary changes are needed for the second query instead of scanning
three values again.

## Pattern recognition

Use it for many static range queries when adding/removing one endpoint is cheap
but no easy associative segment-tree merge exists.

## Implementation: number of distinct values

### C++

```cpp
struct Query { int left; int right; int index; };

std::vector<int> distinctQueries(const std::vector<int>& values, std::vector<Query> queries) {
    const int block = std::max(1, static_cast<int>(std::sqrt(values.size())));
    std::sort(queries.begin(), queries.end(), [&](const Query& a, const Query& b) {
        int firstBlock = a.left / block, secondBlock = b.left / block;
        if (firstBlock != secondBlock) return firstBlock < secondBlock;
        return firstBlock & 1 ? a.right > b.right : a.right < b.right;
    });
    std::unordered_map<int, int> frequency;
    std::vector<int> answer(queries.size());
    int left = 0, right = 0, distinct = 0;
    auto add = [&](int value) { if (frequency[value]++ == 0) ++distinct; };
    auto remove = [&](int value) { if (--frequency[value] == 0) --distinct; };
    for (const Query& query : queries) {
        while (left > query.left) add(values[--left]);
        while (right < query.right) add(values[right++]);
        while (left < query.left) remove(values[left++]);
        while (right > query.right) remove(values[--right]);
        answer[query.index] = distinct;
    }
    return answer;
}
```

### Python

```python
from math import isqrt


def distinct_queries(values: list[int], queries: list[tuple[int, int]]) -> list[int]:
    block = max(1, isqrt(len(values)))
    ordered = sorted(
        enumerate(queries),
        key=lambda item: (item[1][0] // block, item[1][1] if item[1][0] // block % 2 == 0 else -item[1][1]),
    )
    frequency: dict[int, int] = {}
    answer = [0] * len(queries)
    left = right = distinct = 0

    def add(value: int) -> None:
        nonlocal distinct
        if frequency.get(value, 0) == 0:
            distinct += 1
        frequency[value] = frequency.get(value, 0) + 1

    def remove(value: int) -> None:
        nonlocal distinct
        frequency[value] -= 1
        if frequency[value] == 0:
            distinct -= 1

    for index, (query_left, query_right) in ordered:
        while left > query_left:
            left -= 1
            add(values[left])
        while right < query_right:
            add(values[right])
            right += 1
        while left < query_left:
            remove(values[left])
            left += 1
        while right > query_right:
            right -= 1
            remove(values[right])
        answer[index] = distinct
    return answer
```

### Java

```java
record Query(int left, int right, int index) {}

static int[] distinctQueries(int[] values, Query[] queries) {
    int block = Math.max(1, (int) Math.sqrt(values.length));
    Arrays.sort(queries, (first, second) -> {
        int firstBlock = first.left() / block;
        int secondBlock = second.left() / block;
        if (firstBlock != secondBlock) return Integer.compare(firstBlock, secondBlock);
        return firstBlock % 2 == 0
            ? Integer.compare(first.right(), second.right())
            : Integer.compare(second.right(), first.right());
    });
    Map<Integer, Integer> frequency = new HashMap<>();
    int[] answer = new int[queries.length];
    int left = 0, right = 0, distinct = 0;
    for (Query query : queries) {
        while (left > query.left()) { int value = values[--left]; if (frequency.merge(value, 1, Integer::sum) == 1) distinct++; }
        while (right < query.right()) { int value = values[right++]; if (frequency.merge(value, 1, Integer::sum) == 1) distinct++; }
        while (left < query.left()) { int value = values[left++]; int count = frequency.merge(value, -1, Integer::sum); if (count == 0) distinct--; }
        while (right > query.right()) { int value = values[--right]; int count = frequency.merge(value, -1, Integer::sum); if (count == 0) distinct--; }
        answer[query.index()] = distinct;
    }
    return answer;
}
```

## Why it works

Reordering is safe because queries are offline. The maintained state always
matches the current range, and the ordering bounds total endpoint movement.

## Complexity

With `O(1)` add/remove, time is about `O((n + q) sqrt(n))`; space is `O(n + q)`.

## Common mistakes

- Applying it when queries must be answered online.
- Mixing inclusive and half-open endpoints.
- Forgetting original query indices.
- Mutating data without using Mo's-with-updates extension.
