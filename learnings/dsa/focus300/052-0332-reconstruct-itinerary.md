# Focus300 052: LeetCode 332 - Reconstruct Itinerary

**Source:** [LeetCode 332 - Reconstruct Itinerary](https://leetcode.com/problems/reconstruct-itinerary/)  
**Difficulty:** Hard  
**Pattern:** lexicographic Eulerian trail  

## Exact contract

Tickets are directed edges `(origin, destination)`. Starting at `JFK`, use
every ticket exactly once and return the lexicographically smallest valid
airport itinerary. Duplicate tickets are distinct edges. The source guarantees
at least one valid itinerary.

## First principles

This is an Eulerian trail in a directed multigraph. Choosing the smallest edge
greedily can get stuck. Hierholzer's algorithm instead follows available edges
until it cannot continue, then commits that airport in reverse order; sorting
outgoing edges makes the resulting valid trail lexicographically smallest.


## Classroom board: visit each region or node once

```text
mark what is already seen, expand to neighbors, and stop when the region
is fully explored.
```



## Step-by-step transformation

1. Choose a start state such as a cell, node, or partial path.
2. Mark the state as visited or temporarily commit the choice.
3. Expand to valid neighbors or next choices while the invariant still holds.
4. Undo the temporary choice when the branch finishes, then return the collected answer.

These problems transform the input into output by exploring one branch at a time and backtracking whenever a branch can no longer produce a valid solution.


## Diagram: search and undo

```text

            start state
                |
                v
            choose one path
                |
                v
            explore neighbors
                |
                v
            undo and try next path
                |
                v
            answer
```

These notes use search, visit markers, and backtracking to turn one starting state into the final valid path or count.

## Cases that decide correctness

- Duplicate tickets must be consumed separately.
- A locally smallest destination may be a dead end.
- Airports not reachable from `JFK` invalidate the source guarantee.
- The itinerary contains exactly `tickets + 1` airports.
- Reverse postorder, not forward traversal order, is the Eulerian route.

## Brute force: backtrack through sorted unused tickets

```python
Ticket = tuple[str, str]


def reconstruct_itinerary_brute(tickets: list[Ticket]) -> list[str]:
    if any(
        not isinstance(origin, str)
        or not origin
        or not isinstance(destination, str)
        or not destination
        for origin, destination in tickets
    ):
        raise ValueError("airports must be nonempty strings")
    used = [False] * len(tickets)
    ordered_indices = sorted(range(len(tickets)), key=lambda index: tickets[index][1])
    route = ["JFK"]

    def search() -> bool:
        if len(route) == len(tickets) + 1:
            return True
        current = route[-1]
        for ticket_index in ordered_indices:
            origin, destination = tickets[ticket_index]
            if used[ticket_index] or origin != current:
                continue
            used[ticket_index] = True
            route.append(destination)
            if search():
                return True
            route.pop()
            used[ticket_index] = False
        return False

    if not search():
        raise ValueError("no itinerary uses every ticket from JFK")
    return route
```

**Complexity:** `O(m! * m)` time and `O(m)` space.

## Better approach: edge-count backtracking

Grouping duplicate edges by destination reduces symmetric branches, but the
search remains exponential. Eulerian postorder removes backtracking entirely.

## Expert solution: iterative Hierholzer traversal

```python
Ticket = tuple[str, str]


def reconstruct_itinerary(tickets: list[Ticket]) -> list[str]:
    if any(
        not isinstance(origin, str)
        or not origin
        or not isinstance(destination, str)
        or not destination
        for origin, destination in tickets
    ):
        raise ValueError("airports must be nonempty strings")
    outgoing: dict[str, list[str]] = {}
    for origin, destination in sorted(tickets, reverse=True):
        outgoing.setdefault(origin, []).append(destination)

    stack = ["JFK"]
    reverse_route = []
    while stack:
        current = stack[-1]
        destinations = outgoing.get(current)
        if destinations:
            stack.append(destinations.pop())
        else:
            reverse_route.append(stack.pop())
    route = reverse_route[::-1]
    if len(route) != len(tickets) + 1:
        raise ValueError("no itinerary uses every ticket from JFK")
    return route
```

Hierholzer commits a vertex only after exhausting its remaining suffix trail,
so every edge appears once in the reversed route. Taking the smallest remaining
destination whenever a suffix begins yields the smallest valid Eulerian trail.

**Complexity:** `O(m log m)` time and `O(m)` space.

