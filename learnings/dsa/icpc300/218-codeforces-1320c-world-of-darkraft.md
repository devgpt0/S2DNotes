# ICPC300 218: Codeforces 1320C - World of Darkraft: Battle for Azathoth

**Source:** [Codeforces 1320C](https://codeforces.com/problemset/problem/1320/C)  
**Pattern:** weapon sweep with suffix-add armor profits

## Exact contract

Buy exactly one weapon and one armor. A weapon has attack and cost; armor has
defense and cost. Monster `(defense,attack,reward)` is defeated exactly when
weapon attack is greater than its defense and armor defense is greater than its
attack. Maximize defeated rewards minus both item costs.

## First principles

Sort weapons by attack and monsters by defense. When a weapon becomes strong
enough for a monster, that reward becomes available to every armor whose
defense exceeds the monster's attack: a suffix addition over armors sorted by
defense.

Initialize every armor leaf to negative cost. A lazy maximum segment tree adds
new rewards to suffixes; its root is the best armor profit for the current
weapon.

## Cases that decide correctness

- Both defeat comparisons are strict.
- Exactly one weapon and one armor must be paid for.
- A monster reward is added once when the weapon sweep passes its defense.
- Multiple items with equal statistics remain valid independent choices.
- The optimum may be negative.

## Brute force: try every equipment pair

```python
def darkraft_brute(
    weapons: list[tuple[int, int]],
    armors: list[tuple[int, int]],
    monsters: list[tuple[int, int, int]],
) -> int:
    answer = -(10**30)
    for weapon_attack, weapon_cost in weapons:
        for armor_defense, armor_cost in armors:
            profit = -weapon_cost - armor_cost
            for monster_defense, monster_attack, reward in monsters:
                if weapon_attack > monster_defense and armor_defense > monster_attack:
                    profit += reward
            answer = max(answer, profit)
    return answer
```

This multiplies all three input dimensions.

## Better insight: one monster affects an armor suffix

After sorting defenses, the armor condition is one suffix boundary. The weapon
condition is handled once by the outer attack sweep.

## Expert solution: lazy suffix rewards

```python
import sys
from bisect import bisect_right


def solve() -> None:
    input_stream = sys.stdin.buffer
    weapon_count, armor_count, monster_count = map(int, input_stream.readline().split())
    weapons = sorted(
        tuple(map(int, input_stream.readline().split())) for _ in range(weapon_count)
    )
    armors = sorted(
        tuple(map(int, input_stream.readline().split())) for _ in range(armor_count)
    )
    monsters = sorted(
        tuple(map(int, input_stream.readline().split())) for _ in range(monster_count)
    )
    defenses = [defense for defense, _ in armors]
    base = 1
    while base < armor_count:
        base *= 2
    negative_infinity = -(10**30)
    maximum = [negative_infinity] * (2 * base)
    lazy = [0] * (2 * base)
    for index, (_, cost) in enumerate(armors):
        maximum[base + index] = -cost
    for node in range(base - 1, 0, -1):
        maximum[node] = max(maximum[node * 2], maximum[node * 2 + 1])

    def add(
        node: int,
        left: int,
        right: int,
        query_left: int,
        query_right: int,
        reward: int,
    ) -> None:
        if query_right <= left or right <= query_left:
            return
        if query_left <= left and right <= query_right:
            maximum[node] += reward
            lazy[node] += reward
            return
        middle = (left + right) // 2
        add(node * 2, left, middle, query_left, query_right, reward)
        add(node * 2 + 1, middle, right, query_left, query_right, reward)
        maximum[node] = lazy[node] + max(maximum[node * 2], maximum[node * 2 + 1])

    answer = negative_infinity
    monster_index = 0
    for weapon_attack, weapon_cost in weapons:
        while (
            monster_index < monster_count and monsters[monster_index][0] < weapon_attack
        ):
            _, monster_attack, reward = monsters[monster_index]
            first_armor = bisect_right(defenses, monster_attack)
            if first_armor < armor_count:
                add(1, 0, base, first_armor, armor_count, reward)
            monster_index += 1
        answer = max(answer, maximum[1] - weapon_cost)
    print(answer)


if __name__ == "__main__":
    solve()
```

At each weapon, every and only defeatable monster has contributed its reward
to every and only compatible armor leaf.

**Complexity:** `O((n+m+p) log(n+m+p))` time and `O(m)` space.
