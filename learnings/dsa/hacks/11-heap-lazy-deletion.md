# Heaps and Lazy Deletion

## First principles

A heap orders stored entries but does not know which entries are still
logically valid. Keep validity in a separate source of truth, insert new
priorities, and discard stale entries only when they reach the top.

## Why it matters

Python's `heapq` has no efficient decrease-key or arbitrary deletion. Strong
solutions add the new entry and ignore old entries when popped.

## Technique: stale-entry check

```python
import heapq


def dijkstra(graph: list[list[tuple[int, int]]], start: int) -> list[int]:
    distance = [10**30] * len(graph)
    distance[start] = 0
    heap = [(0, start)]
    while heap:
        current_distance, vertex = heapq.heappop(heap)
        if current_distance != distance[vertex]:
            continue
        for neighbor, weight in graph[vertex]:
            candidate = current_distance + weight
            if candidate < distance[neighbor]:
                distance[neighbor] = candidate
                heapq.heappush(heap, (candidate, neighbor))
    return distance
```

## Technique: removable priority queue

For a heap plus a frequency map, remove invalid tops before reading:

```python
def clean_top(heap: list[int], removed: dict[int, int]) -> None:
    import heapq

    while heap and removed.get(heap[0], 0):
        value = heapq.heappop(heap)
        removed[value] -= 1
```

## Pattern recognition

Use lazy deletion when priorities change, items expire, or two heaps share
logical membership.

## Expert habit

State the source of truth. In Dijkstra it is `distance`; in a removable heap it
is the live-count map. The heap may contain historical entries.

## Visual worked example: skip an old priority

```text
best distance to B starts as 5
heap: [(5,B)]

later discover distance 3
distance[B] = 3
heap: [(3,B), (5,B)]

pop (3,B): equals distance[B] -> process
pop (5,B): differs from distance[B] -> stale, skip
```

The heap is historical storage; `distance` or a live-count map defines the
current logical state.

## Traps

- Reading `heap[0]` before cleaning stale entries.
- Assuming heap iteration is sorted.
- Using `-value` for a max-heap but forgetting to negate on output.
- Letting stale entries grow without a memory check in very long simulations.
