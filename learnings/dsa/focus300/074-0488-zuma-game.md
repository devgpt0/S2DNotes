# Focus300 074: LeetCode 488 - Zuma Game

**Source:** [LeetCode 488](https://leetcode.com/problems/zuma-game/)  
**Difficulty:** Hard  
**Pattern:** chain-reaction reduction with memoized hand states

## Exact contract

Given a board string and hand string over colors `R`, `Y`, `B`, `G`, and `W`,
insert one hand ball anywhere per step. Whenever at least three adjacent balls
share a color, remove that group and continue removing newly formed groups.
Return the minimum insertions that clear the board, or `-1` if impossible.

## First principles

Always reduce a board to stability before making another decision. In a stable
board, each color run has length one or two. Clearing a chosen run directly
needs `3 - run_length` matching hand balls; its removal may join and clear
neighboring runs. Memoize the stable board plus remaining color counts.


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

- One insertion may trigger several removals.
- Hand balls of the same color are interchangeable.
- Different insertion positions can reduce to the same stable board.
- A run cannot be cleared when the hand lacks its required color count.
- The answer counts inserted balls, not chain-reaction removals.

## Brute force: breadth-first search over every insertion

```python
def zuma_min_steps_brute(board: str, hand: str) -> int:
    colors = set("RYBGW")
    if (
        not board
        or not hand
        or any(character not in colors for character in board + hand)
    ):
        raise ValueError("board and hand must use Zuma colors")

    def reduce(current: str) -> str:
        while True:
            pieces: list[str] = []
            index = 0
            changed = False
            while index < len(current):
                end = index + 1
                while end < len(current) and current[end] == current[index]:
                    end += 1
                if end - index >= 3:
                    changed = True
                else:
                    pieces.append(current[index:end])
                index = end
            next_board = "".join(pieces)
            if not changed:
                return next_board
            current = next_board

    initial = (reduce(board), "".join(sorted(hand)))
    level = {initial}
    steps = 0
    seen = {initial}
    while level:
        next_level: set[tuple[str, str]] = set()
        for current, remaining in level:
            if not current:
                return steps
            for hand_index, color in enumerate(remaining):
                if hand_index and remaining[hand_index - 1] == color:
                    continue
                next_hand = remaining[:hand_index] + remaining[hand_index + 1 :]
                for position in range(len(current) + 1):
                    next_board = reduce(current[:position] + color + current[position:])
                    state = (next_board, next_hand)
                    if state not in seen:
                        seen.add(state)
                        next_level.add(state)
        level = next_level
        steps += 1
    return -1
```

BFS is exact but explores many equivalent insertions and positions.

## Better transition: remove one stable run at a time

An optimal sequence can be viewed as choosing which stable run is completed
next. Spend exactly the matching balls needed to reach length three, collapse
the board, and recurse on the remaining multiset of hand colors.

## Expert solution: memoized run completion

```python
from functools import cache


def zuma_min_steps(board: str, hand: str) -> int:
    colors = "RYBGW"
    if (
        not board
        or not hand
        or any(character not in colors for character in board + hand)
    ):
        raise ValueError("board and hand must use Zuma colors")

    def reduce(current: str) -> str:
        while True:
            pieces: list[str] = []
            index = 0
            while index < len(current):
                end = index + 1
                while end < len(current) and current[end] == current[index]:
                    end += 1
                if end - index < 3:
                    pieces.append(current[index:end])
                index = end
            next_board = "".join(pieces)
            if next_board == current:
                return current
            current = next_board

    initial_counts = tuple(hand.count(color) for color in colors)

    @cache
    def search(current: str, counts: tuple[int, ...]) -> int:
        current = reduce(current)
        if not current:
            return 0
        best = len(hand) + 1
        index = 0
        while index < len(current):
            end = index + 1
            while end < len(current) and current[end] == current[index]:
                end += 1
            color_index = colors.index(current[index])
            needed = 3 - (end - index)
            if counts[color_index] >= needed:
                remaining = list(counts)
                remaining[color_index] -= needed
                suffix = search(current[:index] + current[end:], tuple(remaining))
                if suffix >= 0:
                    best = min(best, needed + suffix)
            index = end
        return -1 if best > len(hand) else best

    return search(board, initial_counts)
```

Every stable run must eventually be completed by matching insertions or vanish
in a chain reaction after another run is removed. Choosing the next directly
completed run therefore covers an optimal ordering; memoization merges all
orders reaching the same stable state and hand multiset.

**Complexity:** Exponential worst-case time, bounded by the small board and
five-ball hand constraints, with memoized state space.
