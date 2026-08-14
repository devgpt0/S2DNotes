# Focus300 078: LeetCode 517 - Super Washing Machines

**Source:** [LeetCode 517](https://leetcode.com/problems/super-washing-machines/)  
**Difficulty:** Hard  
**Pattern:** prefix-flow lower bounds

## Exact contract

Given a nonempty row of washing machines with nonnegative dress counts, one
move lets any subset of machines simultaneously pass one dress to one adjacent
machine. Return the minimum moves needed to make all counts equal, or `-1` when
equalization is impossible.

## First principles

If the total is divisible by the machine count, let `target` be the final load.
At each boundary, the prefix imbalance is the net number of dresses that must
cross that boundary, requiring at least its absolute value in moves. A machine
with local excess `load - target` must send that many dresses itself, at most
one per move. The maximum of both lower bounds is attainable.

## Cases that decide correctness

- A nondivisible total returns `-1`.
- An already balanced row returns zero.
- Transfers in opposite regions may occur in the same move.
- One machine can send only one dress per move, even if both neighbors exist.
- Prefix imbalance may be positive or negative.

## Brute force: breadth-first search over simultaneous moves

```python
from itertools import product


def washing_machine_moves_brute(machines: list[int]) -> int:
    if not machines or any(load < 0 for load in machines):
        raise ValueError("machines must be nonempty and nonnegative")
    total = sum(machines)
    if total % len(machines):
        return -1
    target = (total // len(machines),) * len(machines)
    initial = tuple(machines)
    level = {initial}
    seen = {initial}
    moves = 0
    while level:
        if target in level:
            return moves
        next_level: set[tuple[int, ...]] = set()
        for state in level:
            choices: list[list[int]] = []
            for index, load in enumerate(state):
                options = [0]
                if load:
                    if index:
                        options.append(-1)
                    if index + 1 < len(state):
                        options.append(1)
                choices.append(options)
            for directions in product(*choices):
                if all(direction == 0 for direction in directions):
                    continue
                next_state = list(state)
                for index, direction in enumerate(directions):
                    if direction:
                        next_state[index] -= 1
                        next_state[index + direction] += 1
                candidate = tuple(next_state)
                if candidate not in seen:
                    seen.add(candidate)
                    next_level.add(candidate)
        level = next_level
        moves += 1
    raise RuntimeError("divisible instances are reachable")
```

This is exact for small rows but explores a combinatorial state graph.

## Better transition: derive unavoidable flow

The running sum of `load - target` is the exact net flow required across the
current boundary. Track its absolute value together with each machine's positive
local excess; no detailed move simulation is needed.

## Expert solution: one prefix-flow scan

```python
def washing_machine_moves(machines: list[int]) -> int:
    if not machines or any(load < 0 for load in machines):
        raise ValueError("machines must be nonempty and nonnegative")
    total = sum(machines)
    if total % len(machines):
        return -1

    target = total // len(machines)
    balance = 0
    answer = 0
    for load in machines:
        excess = load - target
        balance += excess
        answer = max(answer, abs(balance), excess)
    return answer
```

`abs(balance)` is necessary boundary traffic, while a positive `excess` is the
number of moves in which that machine itself must send. Standard parallel
left/right routing realizes all boundary flows within the maximum of these
bounds, so the lower bound is tight.

**Complexity:** `O(n)` time and `O(1)` space.
