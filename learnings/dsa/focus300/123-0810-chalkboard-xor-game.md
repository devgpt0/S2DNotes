# Focus300 123: LeetCode 810 - Chalkboard XOR Game

**Source:** [LeetCode 810](https://leetcode.com/problems/chalkboard-xor-game/)  
**Difficulty:** Hard  
**Pattern:** impartial-game invariant from XOR and parity

## Exact contract

Alice and Bob alternately remove one number, with Alice first. A player wins at
the start of their turn when the XOR of all remaining numbers is already zero.
Otherwise, a player who removes a number and thereby makes the XOR zero loses.
Both play optimally; return whether Alice wins.

## First principles

If the current XOR is zero, the current player has already won. Otherwise, an
even number of remaining values always offers a safe removal: if every removal
made XOR zero, every value would equal the current XOR, but an even number of
equal values XORs to zero, a contradiction.

That safe move leaves an odd count and nonzero XOR. By induction, every odd,
nonzero state is losing and every even, nonzero state is winning.


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

- Initial XOR zero is an immediate Alice win.
- A single nonzero value is losing: removing it makes XOR zero.
- Zero-valued elements still affect the parity of the move count.
- Duplicate values are independent removable entries.
- The closed form relies on optimal play, not a greedy value choice.

## Brute force: minimax over every removable index

```python
from functools import cache, reduce
from operator import xor


def xor_game_brute(numbers: list[int]) -> bool:
    if type(numbers) is not list or not 1 <= len(numbers) <= 1_000:
        raise ValueError("numbers length must be between 1 and 1,000")
    if any(type(value) is not int or not 0 <= value < 2**16 for value in numbers):
        raise ValueError("numbers must be integers in [0, 2^16)")

    @cache
    def current_player_wins(state: tuple[int, ...]) -> bool:
        current_xor = reduce(xor, state, 0)
        if current_xor == 0:
            return True
        for index, value in enumerate(state):
            if current_xor ^ value == 0:
                continue
            next_state = state[:index] + state[index + 1 :]
            if not current_player_wins(next_state):
                return True
        return False

    return current_player_wins(tuple(sorted(numbers)))
```

This explores exponentially many multisets and is useful only for small cases.

## Better insight: the game state collapses to XOR zero and length parity

The inductive winning classes mean no move search is needed. Values influence
the answer only through their combined XOR.

## Expert solution: apply the invariant directly

```python
from functools import reduce
from operator import xor


def xor_game(numbers: list[int]) -> bool:
    if type(numbers) is not list or not 1 <= len(numbers) <= 1_000:
        raise ValueError("numbers length must be between 1 and 1,000")
    if any(type(value) is not int or not 0 <= value < 2**16 for value in numbers):
        raise ValueError("numbers must be integers in [0, 2^16)")
    return reduce(xor, numbers, 0) == 0 or len(numbers) % 2 == 0
```

Zero XOR wins immediately; otherwise the parity induction says exactly the
even-length positions are winning.

**Complexity:** `O(n)` time and `O(1)` extra space.
