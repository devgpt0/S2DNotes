# ICPC300 241: Codeforces 609F - Frogs and mosquitoes

**Source:** [Codeforces 609F](https://codeforces.com/problemset/problem/609/F)  
**Difficulty:** 2300  
**Pattern:** first-reaching frog plus ordered waiting mosquitoes

## Exact contract

Frog `i` stands at `x_i` with tongue length `t_i`. Mosquitoes arrive in order;
each has position `p` and size `b`. The leftmost frog whose interval
`[x_i,x_i+t_i]` contains `p` eats it, increasing its tongue by `b`. Otherwise
the mosquito waits. After a frog grows, it repeatedly eats every newly
reachable waiting mosquito, again in position order. Output each frog's eaten
count and final tongue length in original order.

## First principles

Sort frogs by position. A segment tree of maximum reach finds the first frog in
the prefix `x_i <= p` whose reach is at least `p`.

Waiting mosquito positions are known offline. Compress them, keep a queue of
sizes at each position, and maintain which positions are nonempty in another
segment tree. A growing frog repeatedly asks for the first waiting position in
its current reachable interval; every mosquito is removed once.

## Cases that decide correctness

- Frog choice is by position, not by greatest reach.
- Several mosquitoes may wait at the same coordinate.
- Eating one mosquito can unlock a chain of waiting mosquitoes.
- A frog cannot eat a mosquito left of its own position.
- Output order is the original frog order.

## Brute force: scan frogs and waiting mosquitoes

```python
def frogs_brute(
    frogs: list[tuple[int, int]], mosquitoes: list[tuple[int, int]]
) -> list[tuple[int, int]]:
    ordered = sorted(
        [(position, tongue, index) for index, (position, tongue) in enumerate(frogs)]
    )
    eaten = [0] * len(frogs)
    waiting: list[tuple[int, int]] = []
    for mosquito in mosquitoes:
        waiting.append(mosquito)
        changed = True
        while changed:
            changed = False
            waiting.sort()
            for mosquito_index, (position, size) in enumerate(waiting):
                for frog_index, (frog_position, tongue, original_index) in enumerate(
                    ordered
                ):
                    if frog_position <= position <= frog_position + tongue:
                        ordered[frog_index] = (
                            frog_position,
                            tongue + size,
                            original_index,
                        )
                        eaten[original_index] += 1
                        waiting.pop(mosquito_index)
                        changed = True
                        break
                if changed:
                    break
    answer = [(0, 0)] * len(frogs)
    for position, tongue, original_index in ordered:
        answer[original_index] = (eaten[original_index], tongue)
    return answer
```

Repeated scans are quadratic or worse.

## Better insight: both choices are first-position searches

The eater is the first qualifying frog; its next meal is the first nonempty
waiting coordinate in a dynamic interval. Segment trees support both searches.

## Expert solution: two first-match segment trees

```python
import sys
from bisect import bisect_left, bisect_right
from collections import deque


def solve() -> None:
    input_stream = sys.stdin.buffer
    frog_count, mosquito_count = map(int, input_stream.readline().split())
    frogs = []
    for original_index in range(frog_count):
        position, tongue = map(int, input_stream.readline().split())
        frogs.append([position, tongue, original_index, 0])
    mosquitoes = [
        tuple(map(int, input_stream.readline().split())) for _ in range(mosquito_count)
    ]
    frogs.sort()

    frog_base = 1
    while frog_base < frog_count:
        frog_base *= 2
    maximum_reach = [-1] * (2 * frog_base)
    for index, frog in enumerate(frogs):
        maximum_reach[frog_base + index] = frog[0] + frog[1]
    for node in range(frog_base - 1, 0, -1):
        maximum_reach[node] = max(maximum_reach[node * 2], maximum_reach[node * 2 + 1])

    def update_frog(index: int) -> None:
        node = frog_base + index
        maximum_reach[node] = frogs[index][0] + frogs[index][1]
        node //= 2
        while node:
            maximum_reach[node] = max(
                maximum_reach[node * 2], maximum_reach[node * 2 + 1]
            )
            node //= 2

    def first_frog(node: int, left: int, right: int, limit: int, position: int) -> int:
        if left >= limit or maximum_reach[node] < position:
            return -1
        if right - left == 1:
            return left
        middle = (left + right) // 2
        result = first_frog(node * 2, left, middle, limit, position)
        if result != -1:
            return result
        return first_frog(node * 2 + 1, middle, right, limit, position)

    coordinates = sorted({position for position, _ in mosquitoes})
    queues = [deque() for _ in coordinates]
    waiting_base = 1
    while waiting_base < len(coordinates):
        waiting_base *= 2
    waiting_count = [0] * (2 * waiting_base)

    def set_waiting(index: int, present: int) -> None:
        node = waiting_base + index
        waiting_count[node] = present
        node //= 2
        while node:
            waiting_count[node] = waiting_count[node * 2] + waiting_count[node * 2 + 1]
            node //= 2

    def first_waiting(
        node: int, left: int, right: int, query_left: int, query_right: int
    ) -> int:
        if query_right <= left or right <= query_left or waiting_count[node] == 0:
            return -1
        if right - left == 1:
            return left
        middle = (left + right) // 2
        result = first_waiting(node * 2, left, middle, query_left, query_right)
        if result != -1:
            return result
        return first_waiting(node * 2 + 1, middle, right, query_left, query_right)

    positions = [frog[0] for frog in frogs]
    for position, size in mosquitoes:
        prefix = bisect_right(positions, position)
        frog_index = first_frog(1, 0, frog_base, prefix, position)
        if frog_index == -1:
            waiting_index = bisect_left(coordinates, position)
            queues[waiting_index].append(size)
            set_waiting(waiting_index, 1)
            continue

        frogs[frog_index][1] += size
        frogs[frog_index][3] += 1
        while True:
            left_index = bisect_left(coordinates, frogs[frog_index][0])
            right_index = bisect_right(
                coordinates, frogs[frog_index][0] + frogs[frog_index][1]
            )
            waiting_index = first_waiting(1, 0, waiting_base, left_index, right_index)
            if waiting_index == -1:
                break
            frogs[frog_index][1] += queues[waiting_index].popleft()
            frogs[frog_index][3] += 1
            if not queues[waiting_index]:
                set_waiting(waiting_index, 0)
        update_frog(frog_index)

    answer = [(0, 0)] * frog_count
    for _, tongue, original_index, eaten in frogs:
        answer[original_index] = (eaten, tongue)
    print("\n".join(f"{eaten} {tongue}" for eaten, tongue in answer))


if __name__ == "__main__":
    solve()
```

Both searches return their required leftmost position. Each waiting mosquito is
inserted and removed once.

**Complexity:** `O((n+m) log(n+m))` time and `O(n+m)` space.
