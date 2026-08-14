# ICPC300 183: Codeforces 940F - Machine Learning

**Source:** [Codeforces 940F](https://codeforces.com/problemset/problem/940/F)  
**Pattern:** Mo's algorithm with point modifications

## Exact contract

Maintain an array under two operations. Type `1 l r` asks for the smallest
positive integer that is not the frequency of any distinct value in
`a[l..r]`. Type `2 p x` assigns `a[p] = x`. Print every type `1` answer in
operation order.

## First principles

Offline, a query is a triple `(left,right,time)`, where `time` is the number of
updates preceding it. Mo's ordering moves these three coordinates gradually.

Maintain `value_count[x]` and `count_of_counts[f]`, the number of values whose
current frequency is exactly `f`. Adding or removing one array position changes
only two frequency buckets. Applying or rolling back an update uses the same
two operations when its position is inside the current range.

## Cases that decide correctness

- The requested MEX starts at `1`; frequency zero is irrelevant.
- Updates must remember both their old and new values.
- A rolled-back update restores the exact historical value.
- Query answers remain in original order after offline sorting.
- Repeatedly assigning the same value is still a valid update.

## Brute force: process operations online

```python
from collections import Counter


def machine_learning_brute(
    values: list[int], operations: list[tuple[int, ...]]
) -> list[int]:
    current = values.copy()
    answers = []
    for operation in operations:
        if operation[0] == 1:
            _, left, right = operation
            present_frequencies = set(Counter(current[left - 1 : right]).values())
            answer = 1
            while answer in present_frequencies:
                answer += 1
            answers.append(answer)
        else:
            _, position, value = operation
            current[position - 1] = value
    return answers
```

Each query rebuilds all frequencies in its range.

## Better insight: the frequency MEX is small

If frequencies `1..k` are all present, the range has at least
`1+2+...+k` elements. Thus the answer is `O(sqrt(n))`; the difficult part is
maintaining the frequency buckets while range and time move.

## Expert solution: three-dimensional Mo ordering

```python
import sys


def solve() -> None:
    input_stream = sys.stdin.buffer
    size, operation_count = map(int, input_stream.readline().split())
    original = list(map(int, input_stream.readline().split()))

    updates: list[tuple[int, int, int]] = []
    queries: list[tuple[int, int, int, int]] = []
    reading_values = original.copy()
    query_index = 0
    for _ in range(operation_count):
        operation_type, first, second = map(int, input_stream.readline().split())
        if operation_type == 1:
            queries.append((first - 1, second, len(updates), query_index))
            query_index += 1
        else:
            position = first - 1
            updates.append((position, reading_values[position], second))
            reading_values[position] = second

    block_size = max(1, round(size ** (2 / 3)))

    def ordering(query: tuple[int, int, int, int]) -> tuple[int, int, int]:
        left, right, time, _ = query
        left_block = left // block_size
        right_block = right // block_size
        ordered_right = right_block if left_block % 2 == 0 else -right_block
        ordered_time = time if right_block % 2 == 0 else -time
        return (left_block, ordered_right, ordered_time)

    queries.sort(key=ordering)
    current_values = original.copy()
    value_count: dict[int, int] = {}
    count_of_counts = [0] * (size + 2)

    def adjust(value: int, difference: int) -> None:
        old_count = value_count.get(value, 0)
        if old_count:
            count_of_counts[old_count] -= 1
        new_count = old_count + difference
        if new_count:
            value_count[value] = new_count
            count_of_counts[new_count] += 1
        else:
            value_count.pop(value)

    current_left = 0
    current_right = 0
    current_time = 0
    answers = [0] * query_index

    def change_time(forward: bool) -> None:
        nonlocal current_time
        update_index = current_time if forward else current_time - 1
        position, old_value, new_value = updates[update_index]
        before = old_value if forward else new_value
        after = new_value if forward else old_value
        if current_left <= position < current_right:
            adjust(before, -1)
            adjust(after, 1)
        current_values[position] = after
        current_time += 1 if forward else -1

    for query_left, query_right, query_time, original_index in queries:
        while current_time < query_time:
            change_time(True)
        while current_time > query_time:
            change_time(False)
        while current_left > query_left:
            current_left -= 1
            adjust(current_values[current_left], 1)
        while current_right < query_right:
            adjust(current_values[current_right], 1)
            current_right += 1
        while current_left < query_left:
            adjust(current_values[current_left], -1)
            current_left += 1
        while current_right > query_right:
            current_right -= 1
            adjust(current_values[current_right], -1)

        answer = 1
        while count_of_counts[answer]:
            answer += 1
        answers[original_index] = answer

    print("\n".join(map(str, answers)))


if __name__ == "__main__":
    solve()
```

The current range and update time exactly match each offline query before its
MEX is read. Both count layers are updated atomically for every movement.

**Complexity:** about `O((n+q) n^(2/3) + q sqrt(n))` time and `O(n+q)` space.
