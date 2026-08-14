# 133. A Simple Task — Codeforces 558E

**Source:** [Codeforces 558E - A Simple Task](https://codeforces.com/problemset/problem/558/E)  
**Difficulty:** 2300

## 1. Problem in plain words

Given a lowercase string, process queries `(left, right, order)`. Sort that substring increasingly when `order = 1` and decreasingly when `order = 0`. Print the final string after all queries.

The source uses one-based endpoints. The functions below use zero-based endpoints.

## 2. First principles

Sorting a lowercase substring only needs its 26 letter counts. Once those counts are known, the sorted result is forced: write each letter in alphabetic or reverse-alphabetic order for exactly its count.

A segment tree can store 26 counts per segment and lazily mark a whole segment as one letter. Each query first obtains the counts, then overwrites the interval with at most 26 constant-letter ranges.

## 3. Cases that define correctness

- A one-character interval is unchanged.
- Letters with zero count create no assigned range.
- Repeated and nested queries must see all earlier assignments.
- `order = 0` reverses letter order, not the original substring.

## 4. Brute force

Slice, sort, optionally reverse, and write the slice back.

```python
def sort_substrings_brute_force(text: str, queries: list[tuple[int, int, int]]) -> str:
    if not text or any(not "a" <= character <= "z" for character in text):
        raise ValueError("text must be a nonempty lowercase string")

    data = list(text)
    for left, right, order in queries:
        if not 0 <= left <= right < len(data) or order not in (0, 1):
            raise ValueError("invalid query")
        part = sorted(data[left : right + 1], reverse=order == 0)
        data[left : right + 1] = part
    return "".join(data)
```

The worst-case cost is `O(q n log n)` time and `O(n)` temporary space.

## 5. Better approach: count the fixed alphabet

Sorting is unnecessary. Count the 26 letters in one pass over the interval, then write them back in the requested order.

```python
def sort_substrings_by_counting(text: str, queries: list[tuple[int, int, int]]) -> str:
    if not text or any(not "a" <= character <= "z" for character in text):
        raise ValueError("text must be a nonempty lowercase string")

    data = list(text)
    for left, right, order in queries:
        if not 0 <= left <= right < len(data) or order not in (0, 1):
            raise ValueError("invalid query")
        counts = [0] * 26
        for index in range(left, right + 1):
            counts[ord(data[index]) - ord("a")] += 1
        position = left
        letters = range(26) if order == 1 else range(25, -1, -1)
        for letter in letters:
            for _ in range(counts[letter]):
                data[position] = chr(ord("a") + letter)
                position += 1
    return "".join(data)
```

This takes `O(qn + 26q)` time in the worst case and `O(n + 26)` space.

## 6. Expert solution: lazy frequency segment tree

Each node stores a 26-entry frequency vector. A lazy value means its whole segment currently contains one letter. Query the interval's vector, then assign consecutive ranges in ascending or descending letter order.

```python
def sort_substrings(text: str, queries: list[tuple[int, int, int]]) -> str:
    if not text or any(not "a" <= character <= "z" for character in text):
        raise ValueError("text must be a nonempty lowercase string")

    size = len(text)
    counts = [[0] * 26 for _ in range(4 * size)]
    lazy = [-1] * (4 * size)

    def build(node: int, left: int, right: int) -> None:
        if left == right:
            counts[node][ord(text[left]) - ord("a")] = 1
            return
        middle = (left + right) // 2
        build(node * 2, left, middle)
        build(node * 2 + 1, middle + 1, right)
        for letter in range(26):
            counts[node][letter] = (
                counts[node * 2][letter] + counts[node * 2 + 1][letter]
            )

    def assign_node(node: int, left: int, right: int, letter: int) -> None:
        counts[node] = [0] * 26
        counts[node][letter] = right - left + 1
        lazy[node] = letter

    def push(node: int, left: int, right: int) -> None:
        letter = lazy[node]
        if letter == -1 or left == right:
            return
        middle = (left + right) // 2
        assign_node(node * 2, left, middle, letter)
        assign_node(node * 2 + 1, middle + 1, right, letter)
        lazy[node] = -1

    def query(
        node: int, left: int, right: int, query_left: int, query_right: int
    ) -> list[int]:
        if query_left <= left and right <= query_right:
            return counts[node].copy()
        push(node, left, right)
        middle = (left + right) // 2
        result = [0] * 26
        if query_left <= middle:
            part = query(node * 2, left, middle, query_left, query_right)
            for letter in range(26):
                result[letter] += part[letter]
        if middle < query_right:
            part = query(node * 2 + 1, middle + 1, right, query_left, query_right)
            for letter in range(26):
                result[letter] += part[letter]
        return result

    def assign(
        node: int,
        left: int,
        right: int,
        query_left: int,
        query_right: int,
        letter: int,
    ) -> None:
        if query_left <= left and right <= query_right:
            assign_node(node, left, right, letter)
            return
        push(node, left, right)
        middle = (left + right) // 2
        if query_left <= middle:
            assign(node * 2, left, middle, query_left, query_right, letter)
        if middle < query_right:
            assign(node * 2 + 1, middle + 1, right, query_left, query_right, letter)
        for current in range(26):
            counts[node][current] = (
                counts[node * 2][current] + counts[node * 2 + 1][current]
            )

    build(1, 0, size - 1)
    for left, right, order in queries:
        if not 0 <= left <= right < size or order not in (0, 1):
            raise ValueError("invalid query")
        interval_counts = query(1, 0, size - 1, left, right)
        position = left
        letters = range(26) if order == 1 else range(25, -1, -1)
        for letter in letters:
            amount = interval_counts[letter]
            if amount:
                assign(1, 0, size - 1, position, position + amount - 1, letter)
                position += amount

    result = [""] * size

    def materialize(node: int, left: int, right: int) -> None:
        if left == right:
            result[left] = chr(ord("a") + counts[node].index(1))
            return
        push(node, left, right)
        middle = (left + right) // 2
        materialize(node * 2, left, middle)
        materialize(node * 2 + 1, middle + 1, right)

    materialize(1, 0, size - 1)
    return "".join(result)
```

## 7. Why the expert solution is correct

Every node vector equals the letter multiset of its segment; lazy assignment replaces that multiset by the correct number of one letter. A query therefore obtains exactly the substring's multiset. Writing its counts into consecutive ranges in the requested alphabet order produces exactly the sorted substring and changes nothing outside it.

With alphabet size `26`, time is `O(26² q log n + 26n)` and space is `O(26n)`.
