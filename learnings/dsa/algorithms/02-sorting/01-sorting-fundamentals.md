# Sorting Fundamentals and Comparators

## Idea

Sorting often converts a global search into a local scan. Before implementing
a sort, use the language library unless the problem specifically needs the
algorithm: library sorts are tested, optimized, and less error-prone.

## Properties

- **Stable:** equal keys keep their original relative order.
- **In place:** uses `O(1)` or `O(log n)` auxiliary memory.
- **Comparison sort:** learns order only through comparisons; it needs
  `Omega(n log n)` comparisons in the worst case.

## Classroom board: sort records by two rules

```text
(Asha, 8), (Ben, 10), (Cara, 8)

rule 1: higher score first
rule 2: equal scores use name A-Z

result: (Ben, 10), (Asha, 8), (Cara, 8)
```

Write the rules in words before writing the comparator.

## Steps

1. Decide the primary and tie-breaking keys.
2. Decide each key's direction.
3. Use a consistent total-order comparator or tuple key.
4. Preserve original indices if the answer needs them.

## First-principles derivation

Sorting imposes an order that later operations can exploit. A comparator must
answer which of two records comes first and must be consistent for every
triple of records.

The invariant after sorting is that no later element should precede an earlier
one under the comparator.

## Pattern recognition

Sort when ordered neighbors enable a scan, grouping, interval processing,
binary search, two pointers, or a greedy choice.

## Sort records by `(score descending, name ascending)`

The comparator must define a consistent total order. Never use subtraction for
fixed-width integer comparison because it can overflow.

### C++

```cpp
struct Player {
    std::string name;
    int score;
};

void rankPlayers(std::vector<Player>& players) {
    std::sort(players.begin(), players.end(), [](const Player& left, const Player& right) {
        if (left.score != right.score) {
            return left.score > right.score;
        }
        return left.name < right.name;
    });
}
```

### Python

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class Player:
    name: str
    score: int


def rank_players(players: list[Player]) -> list[Player]:
    return sorted(players, key=lambda player: (-player.score, player.name))
```

### Java

```java
record Player(String name, int score) {}

static void rankPlayers(List<Player> players) {
    players.sort(
        Comparator.comparingInt(Player::score)
            .reversed()
            .thenComparing(Player::name)
    );
}
```

## Why it works

The comparator defines which record must come first, and the library sort
arranges every pair consistently with that rule.

## Complexity

Time is `O(n log n)`. Extra space depends on the language implementation.

## Common mistakes

- Using subtraction in a comparator and overflowing.
- Returning inconsistent comparison results.
- Losing original indices or mutating input unexpectedly.
