# ICPC300 209: Codeforces 1149B - Three Religions

**Source:** [Codeforces 1149B - Three Religions](https://codeforces.com/problemset/problem/1149/B)  
**Difficulty:** 2400  
**Pattern:** persistent 3D interleaving-subsequence frontier

## Exact contract

Three lowercase strings start empty. Each operation appends one character to a
chosen string or deletes its last character. After every operation, decide
whether some interleaving of the three current strings is a subsequence of one
fixed lowercase base string. Operations use `(action, index, character)`, where
delete uses an empty character.

## First principles

Let `dp[i,j,k]` be the smallest base-string cursor after matching an
interleaving of the three prefixes. Its last character comes from exactly one
of the three strings, giving three predecessor transitions. Smaller cursors
dominate larger ones.

Appending to one string creates only one new 2D boundary slice. Deleting needs
no recomputation because all prefix states remain stored.

## Cases that decide correctness

- Interleaving preserves order inside each of the three strings.
- Different interleavings reaching one state keep only the smallest cursor.
- Deleting from an empty string is invalid.
- A failed state uses a cursor strictly beyond the base length.
- A deleted prefix may later be restored, so its DP cells must remain intact.

## Brute force: enumerate interleaving choices

```python
from functools import cache


def three_religions_brute(
    base: str, operations: list[tuple[str, int, str]]
) -> list[bool]:
    if not base or any(character < "a" or character > "z" for character in base):
        raise ValueError("base must be nonempty and lowercase")
    strings: list[list[str]] = [[], [], []]
    answers: list[bool] = []

    for action, religion, character in operations:
        if type(religion) is not int or not 0 <= religion < 3:
            raise ValueError("religion index must be in [0, 2]")
        if action == "append":
            if (
                type(character) is not str
                or len(character) != 1
                or not "a" <= character <= "z"
            ):
                raise ValueError("append requires one lowercase character")
            strings[religion].append(character)
        elif action == "delete":
            if type(character) is not str or character != "" or not strings[religion]:
                raise ValueError("invalid delete")
            strings[religion].pop()
        else:
            raise ValueError("unknown operation")

        @cache
        def search(first: int, second: int, third: int, cursor: int) -> bool:
            positions = (first, second, third)
            if all(positions[index] == len(strings[index]) for index in range(3)):
                return True
            for index in range(3):
                if positions[index] == len(strings[index]):
                    continue
                found = base.find(strings[index][positions[index]], cursor)
                if found == -1:
                    continue
                following = list(positions)
                following[index] += 1
                if search(*following, found + 1):
                    return True
            return False

        answers.append(search(0, 0, 0, 0))
    return answers
```

The number of interleavings is exponential before memoization and remains too
large for source bounds.

## Better approach: rebuild the complete 3D DP

Recomputing every current `(i,j,k)` state after each operation is polynomial
and uses the same minimum-cursor recurrence, but costs `O(qL^3 log n)` with
binary searches for next occurrences. The expert update computes only the new
boundary slice in `O(L^2)`.

## Expert solution: update one persistent boundary slice

```python
from array import array


def three_religions(base: str, operations: list[tuple[str, int, str]]) -> list[bool]:
    if not base or any(character < "a" or character > "z" for character in base):
        raise ValueError("base must be nonempty and lowercase")

    lengths = [0, 0, 0]
    maximum_lengths = [0, 0, 0]
    for action, religion, character in operations:
        if type(religion) is not int or not 0 <= religion < 3:
            raise ValueError("religion index must be in [0, 2]")
        if action == "append":
            if (
                type(character) is not str
                or len(character) != 1
                or not "a" <= character <= "z"
            ):
                raise ValueError("append requires one lowercase character")
            lengths[religion] += 1
            maximum_lengths[religion] = max(
                maximum_lengths[religion], lengths[religion]
            )
        elif action == "delete":
            if type(character) is not str or character != "" or lengths[religion] == 0:
                raise ValueError("invalid delete")
            lengths[religion] -= 1
        else:
            raise ValueError("unknown operation")

    base_size = len(base)
    next_by_character: list[array] = []
    for letter in range(26):
        next_positions = array("i", [base_size]) * (base_size + 1)
        nearest = base_size
        target = chr(ord("a") + letter)
        for position in range(base_size - 1, -1, -1):
            if base[position] == target:
                nearest = position
            next_positions[position] = nearest
        next_by_character.append(next_positions)

    first_size = maximum_lengths[0] + 1
    second_size = maximum_lengths[1] + 1
    third_size = maximum_lengths[2] + 1
    infinity = base_size + 1
    states = array("i", [infinity]) * (first_size * second_size * third_size)
    states[0] = 0

    def state_index(first: int, second: int, third: int) -> int:
        return (first * second_size + second) * third_size + third

    def advance(cursor: int, character: str) -> int:
        if cursor > base_size:
            return infinity
        position = next_by_character[ord(character) - ord("a")][cursor]
        return position + 1 if position < base_size else infinity

    strings: list[list[str]] = [[], [], []]
    answers: list[bool] = []

    def recompute(first: int, second: int, third: int) -> None:
        best = infinity
        if first:
            best = min(
                best,
                advance(
                    states[state_index(first - 1, second, third)],
                    strings[0][first - 1],
                ),
            )
        if second:
            best = min(
                best,
                advance(
                    states[state_index(first, second - 1, third)],
                    strings[1][second - 1],
                ),
            )
        if third:
            best = min(
                best,
                advance(
                    states[state_index(first, second, third - 1)],
                    strings[2][third - 1],
                ),
            )
        states[state_index(first, second, third)] = best

    for action, religion, character in operations:
        if action == "delete":
            strings[religion].pop()
        else:
            strings[religion].append(character)
            first_length, second_length, third_length = map(len, strings)
            if religion == 0:
                for second in range(second_length + 1):
                    for third in range(third_length + 1):
                        recompute(first_length, second, third)
            elif religion == 1:
                for first in range(first_length + 1):
                    for third in range(third_length + 1):
                        recompute(first, second_length, third)
            else:
                for first in range(first_length + 1):
                    for second in range(second_length + 1):
                        recompute(first, second, third_length)

        current = state_index(*(len(text) for text in strings))
        answers.append(states[current] <= base_size)
    return answers
```

The recurrence considers every possible source of the last interleaving
character. Append creates exactly the states containing the new final
character, while all older prefix cells remain valid across deletes.

**Complexity:** `O(26n + qL^2)` time and `O(L^3 + 26n)` packed integer space,
where `L` is the maximum maintained string length.
