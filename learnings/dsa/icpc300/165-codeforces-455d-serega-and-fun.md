# ICPC300 165: Codeforces 455D - Serega and Fun

**Source:** [Codeforces 455D](https://codeforces.com/problemset/problem/455/D)  
**Pattern:** square-root decomposition of an implicit mutable sequence

## Exact contract

Maintain an array of `n` values in `1..n`. Each encoded query gives `l' r' k'`.
With the previous answer `last`, decode each number as

`x = (x' + last - 1) mod n + 1`,

then swap `l` and `r` if needed. Cyclically shift `a[l..r]` right by one
position (move the element at `r` to `l`) and output the number of occurrences
of `k` in the resulting interval. Initially `last = 0`.

## First principles

Split the sequence into blocks of about `sqrt(n)` elements. Each block stores
its order plus a frequency counter. A rank lookup scans block lengths. Removing
at `r` and inserting at `l` touches at most two block interiors; moving one end
element between adjacent blocks restores block sizes.

A range count scans the two boundary fragments and reads counters for complete
middle blocks. Online decoding uses the answer produced after the move.

## Cases that decide correctness

- Decode all three inputs using the same previous answer.
- Normalize `l <= r` only after decoding.
- If `l = r`, the rotation changes nothing.
- Rebalancing must update both order containers and frequency counters.
- Rotating preserves the current interval's multiset but changes future index
  positions.

## Brute force: mutate a Python list

```python
def serega_brute(
    values: list[int], encoded_queries: list[tuple[int, int, int]]
) -> list[int]:
    sequence = values.copy()
    size = len(sequence)
    last = 0
    answers = []
    for raw_left, raw_right, raw_value in encoded_queries:
        left = (raw_left + last - 1) % size
        right = (raw_right + last - 1) % size
        value = (raw_value + last - 1) % size + 1
        if left > right:
            left, right = right, left
        if left < right:
            moved = sequence.pop(right)
            sequence.insert(left, moved)
        last = sequence[left : right + 1].count(value)
        answers.append(last)
    return answers
```

Both insertion and counting can take linear time per query.

## Better insight: index trees do not preserve both requirements

A Fenwick tree can locate ranks but cannot maintain a separate frequency
structure for every possible value under middle insertion. Conversely, value
frequency trees do not maintain sequence order. Blocks are the useful
intermediate representation; balancing them and using full-block counters is
the complete square-root solution below.

## Expert solution: balanced deques with block counters

```python
import sys
from collections import Counter, deque
from itertools import islice
from math import isqrt


def solve() -> None:
    input_stream = sys.stdin.buffer
    size = int(input_stream.readline())
    values = list(map(int, input_stream.readline().split()))
    query_count = int(input_stream.readline())

    block_size = isqrt(size) + 1
    blocks = [
        deque(values[start : start + block_size])
        for start in range(0, size, block_size)
    ]
    frequencies = [Counter(block) for block in blocks]

    def locate(position: int) -> tuple[int, int]:
        for block_index, block in enumerate(blocks):
            if position < len(block):
                return block_index, position
            position -= len(block)
        raise IndexError("sequence position is out of range")

    def decrement(block_index: int, value: int) -> None:
        frequencies[block_index][value] -= 1
        if frequencies[block_index][value] == 0:
            del frequencies[block_index][value]

    def pop_at(position: int) -> int:
        block_index, offset = locate(position)
        block = blocks[block_index]
        block.rotate(-offset)
        value = block.popleft()
        block.rotate(offset)
        decrement(block_index, value)
        return value

    def insert_at(position: int, value: int) -> None:
        block_index, offset = locate(position)
        block = blocks[block_index]
        block.rotate(-offset)
        block.appendleft(value)
        block.rotate(offset)
        frequencies[block_index][value] += 1

    def rebalance() -> None:
        block_index = 0
        while block_index < len(blocks):
            while len(blocks[block_index]) > block_size:
                value = blocks[block_index].pop()
                decrement(block_index, value)
                if block_index + 1 == len(blocks):
                    blocks.append(deque())
                    frequencies.append(Counter())
                blocks[block_index + 1].appendleft(value)
                frequencies[block_index + 1][value] += 1
            while (
                len(blocks[block_index]) < block_size
                and block_index + 1 < len(blocks)
                and blocks[block_index + 1]
            ):
                value = blocks[block_index + 1].popleft()
                decrement(block_index + 1, value)
                blocks[block_index].append(value)
                frequencies[block_index][value] += 1
            if block_index + 1 < len(blocks) and not blocks[block_index + 1]:
                del blocks[block_index + 1]
                del frequencies[block_index + 1]
                continue
            block_index += 1

    def range_count(left: int, right: int, value: int) -> int:
        left_block, left_offset = locate(left)
        right_block, right_offset = locate(right)
        if left_block == right_block:
            return sum(
                item == value
                for item in islice(blocks[left_block], left_offset, right_offset + 1)
            )
        answer = sum(
            item == value for item in islice(blocks[left_block], left_offset, None)
        )
        answer += sum(
            item == value for item in islice(blocks[right_block], right_offset + 1)
        )
        for block_index in range(left_block + 1, right_block):
            answer += frequencies[block_index].get(value, 0)
        return answer

    last = 0
    output = []
    for _ in range(query_count):
        raw_left, raw_right, raw_value = map(int, input_stream.readline().split())
        left = (raw_left + last - 1) % size
        right = (raw_right + last - 1) % size
        value = (raw_value + last - 1) % size + 1
        if left > right:
            left, right = right, left
        if left < right:
            moved = pop_at(right)
            insert_at(left, moved)
            rebalance()
        last = range_count(left, right, value)
        output.append(str(last))
    print("\n".join(output))


if __name__ == "__main__":
    solve()
```

The concatenated deques always equal the logical sequence. Rebalancing moves
only adjacent boundary elements, so order is preserved, while every counter
continues to equal its block multiset.

**Complexity:** `O(sqrt(n))` block work plus `O(sqrt(n))` boundary work per
query, and `O(n)` space.
