# Focus300 149: LeetCode 913 - Cat and Mouse

**Source:** [LeetCode 913](https://leetcode.com/problems/cat-and-mouse/)  
**Difficulty:** Hard  
**Pattern:** retrograde game-state analysis

## Exact contract

In an undirected graph, the mouse starts at node `1`, the cat at node `2`, and
the mouse moves first. Players alternate along edges; the cat may not enter
node `0`. The mouse wins by reaching `0`, and the cat wins by occupying the
mouse's node. With optimal play, return `1` for a mouse win, `2` for a cat win,
or `0` for a draw.

## First principles

A state is `(mouse, cat, turn)`. Terminal states have known outcomes. A player
wins a state if any legal child is their win; they lose if every legal child is
the opponent's win. States that cannot be forced into either terminal attractor
remain draws because play can cycle forever.


## Classroom board: see the repeated work once

```text
brute force tries every choice.
the optimized solution keeps only the state that must survive to the
next step.
```



## Step-by-step transformation

1. Read the input and identify the smallest state that still determines the answer.
2. Process one element, node, or row at a time while preserving that state.
3. Discard work that can no longer change the result.
4. Convert the surviving state into the output the problem requests.

The examples and code below show this transformation on the specific problem instance.


## Diagram: input to output

```text

        input
            |
            v
        core invariant
            |
            v
        process one step at a time
            |
            v
        output
```

The note shows the main idea, the repeated work, and the small state that turns the input into the output.

## Cases that decide correctness

- The mouse moves first from `(1, 2)`.
- The cat may never move to node `0`.
- Mouse at `0` is a mouse win; equal mouse and cat nodes are a cat win.
- Revisiting states is possible and is not automatically a loss.
- A player with no legal move loses that state.

## Brute force: repeatedly scan every unresolved state

```python
def cat_mouse_game_brute(graph: list[list[int]]) -> int:
    size = len(graph)
    if size < 3 or any(
        not neighbors or any(not 0 <= neighbor < size for neighbor in neighbors)
        for neighbors in graph
    ):
        raise ValueError("graph must contain at least three valid adjacency lists")

    draw = 0
    mouse_win = 1
    cat_win = 2
    outcomes = [[[draw, draw] for _ in range(size)] for _ in range(size)]
    for cat in range(1, size):
        outcomes[0][cat] = [mouse_win, mouse_win]
        outcomes[cat][cat] = [cat_win, cat_win]

    changed = True
    while changed:
        changed = False
        for mouse in range(size):
            for cat in range(1, size):
                for turn in range(2):
                    if outcomes[mouse][cat][turn] != draw:
                        continue
                    if turn == 0:
                        children = [
                            outcomes[next_mouse][cat][1] for next_mouse in graph[mouse]
                        ]
                        player_win = mouse_win
                        opponent_win = cat_win
                    else:
                        children = [
                            outcomes[mouse][next_cat][0]
                            for next_cat in graph[cat]
                            if next_cat != 0
                        ]
                        player_win = cat_win
                        opponent_win = mouse_win
                    if any(result == player_win for result in children):
                        outcomes[mouse][cat][turn] = player_win
                        changed = True
                    elif not children or all(
                        result == opponent_win for result in children
                    ):
                        outcomes[mouse][cat][turn] = opponent_win
                        changed = True
    return outcomes[1][2][0]
```

The monotone fixed-point scan is exact, but it can revisit all `O(n^2)` states
for many rounds and inspect every outgoing move each time.

## Better transition: propagate only newly solved states

Maintain each state's remaining unresolved degree. Once a child becomes a win
for the parent player, that parent is solved immediately. Otherwise decrement
the degree; reaching zero proves that every move loses.

## Expert solution: reverse BFS from terminal states

```python
from collections import deque


def cat_mouse_game(graph: list[list[int]]) -> int:
    size = len(graph)
    if size < 3 or any(
        not neighbors or any(not 0 <= neighbor < size for neighbor in neighbors)
        for neighbors in graph
    ):
        raise ValueError("graph must contain at least three valid adjacency lists")

    draw = 0
    mouse_win = 1
    cat_win = 2
    outcomes = [[[draw, draw] for _ in range(size)] for _ in range(size)]
    degree = [
        [
            [len(graph[mouse]), sum(neighbor != 0 for neighbor in graph[cat])]
            for cat in range(size)
        ]
        for mouse in range(size)
    ]
    queue: deque[tuple[int, int, int]] = deque()

    for cat in range(1, size):
        for turn in range(2):
            outcomes[0][cat][turn] = mouse_win
            queue.append((0, cat, turn))
            outcomes[cat][cat][turn] = cat_win
            queue.append((cat, cat, turn))

    for mouse in range(1, size):
        for cat in range(1, size):
            for turn in range(2):
                if outcomes[mouse][cat][turn] == draw and degree[mouse][cat][turn] == 0:
                    outcomes[mouse][cat][turn] = cat_win if turn == 0 else mouse_win
                    queue.append((mouse, cat, turn))

    while queue:
        mouse, cat, turn = queue.popleft()
        result = outcomes[mouse][cat][turn]
        if turn == 0:
            parents = (
                (mouse, previous_cat, 1)
                for previous_cat in graph[cat]
                if previous_cat != 0
            )
        else:
            parents = ((previous_mouse, cat, 0) for previous_mouse in graph[mouse])

        for parent_mouse, parent_cat, parent_turn in parents:
            if outcomes[parent_mouse][parent_cat][parent_turn] != draw:
                continue
            player_win = mouse_win if parent_turn == 0 else cat_win
            if result == player_win:
                outcomes[parent_mouse][parent_cat][parent_turn] = player_win
                queue.append((parent_mouse, parent_cat, parent_turn))
            else:
                degree[parent_mouse][parent_cat][parent_turn] -= 1
                if degree[parent_mouse][parent_cat][parent_turn] == 0:
                    outcomes[parent_mouse][parent_cat][parent_turn] = (
                        cat_win if parent_turn == 0 else mouse_win
                    )
                    queue.append((parent_mouse, parent_cat, parent_turn))

    return outcomes[1][2][0]
```

Every solved child processes its reverse edges once. Any state never colored by
the terminal attractors permits infinite avoidance and is therefore a draw.

**Complexity:** `O(n * e)` time and `O(n^2)` space.
