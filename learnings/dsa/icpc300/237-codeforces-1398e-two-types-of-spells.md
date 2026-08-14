# ICPC300 237: Codeforces 1398E - Two Types of Spells

**Source:** [Codeforces 1398E - Two Types of Spells](https://codeforces.com/problemset/problem/1398/E)  
**Difficulty:** 2200  
**Pattern:** dynamic top-k sum with a mandatory-type correction

## Exact contract

Maintain a multiset of fire spells (`type 0`) and lightning spells (`type 1`).
An operation adds power `p` or removes power `-p` of its type. In a casting
order, every lightning spell doubles the next spell. After each update, return
the maximum total damage.

## First principles

All powers contribute once. With `L` lightning spells, at most `L` following
spells are doubled, so tentatively add the largest `L` powers. If all selected
spells are lightning, one selected lightning must be last and cannot be doubled:
replace the smallest selected power by the largest unselected fire power when
one exists.

## Cases that decide correctness

- Duplicate `(type,power)` spells are distinct multiset occurrences.
- With no lightning, damage is the ordinary sum.
- With no fire, one lightning necessarily receives no doubling.
- At a threshold tie, prefer selecting fire; it avoids correction for free.
- Removal must match an existing spell of the same type and power.

## Brute force: enumerate every casting order

```python
from itertools import permutations


def spell_damage_brute(operations: list[tuple[int, int]]) -> list[int]:
    spells: list[tuple[int, int]] = []
    answers: list[int] = []
    for spell_type, signed_power in operations:
        if (
            spell_type not in (0, 1)
            or type(signed_power) is not int
            or signed_power == 0
        ):
            raise ValueError("invalid spell update")
        spell = spell_type, abs(signed_power)
        if signed_power > 0:
            spells.append(spell)
        else:
            try:
                spells.remove(spell)
            except ValueError as error:
                raise ValueError("removing a missing spell") from error

        best = 0
        for order in permutations(spells):
            damage = sum(power for _, power in order)
            damage += sum(
                order[index + 1][1]
                for index in range(len(order) - 1)
                if order[index][0] == 1
            )
            best = max(best, damage)
        answers.append(best)
    return answers
```

This is factorial in the active spell count.

## Better approach: sort the active multiset after every update

Sort by descending power, preferring fire on ties, select the first `L`, and
apply the all-lightning correction. This is `O(q^2 log q)` over all updates.

## Expert solution: offline-compressed Fenwick order statistics

```python
def maximum_spell_damage(operations: list[tuple[int, int]]) -> list[int]:
    coordinates = sorted({abs(power) for _, power in operations})
    if any(
        spell_type not in (0, 1) or type(power) is not int or power == 0
        for spell_type, power in operations
    ):
        raise ValueError("invalid spell update")
    if not coordinates:
        return []
    coordinate_index = {power: index for index, power in enumerate(coordinates)}
    size = len(coordinates)
    counts = [0] * (size + 1)
    sums = [0] * (size + 1)
    fire_counts = [0] * (size + 1)

    def add(tree: list[int], position: int, delta: int) -> None:
        position += 1
        while position <= size:
            tree[position] += delta
            position += position & -position

    def prefix(tree: list[int], count: int) -> int:
        result = 0
        while count:
            result += tree[count]
            count -= count & -count
        return result

    def kth(tree: list[int], rank: int) -> int:
        position = 0
        accumulated = 0
        step = 1 << (size.bit_length() - 1)
        while step:
            following = position + step
            if following <= size and accumulated + tree[following] < rank:
                position = following
                accumulated += tree[following]
            step //= 2
        return position

    def sum_smallest(amount: int) -> int:
        if amount == 0:
            return 0
        position = kth(counts, amount)
        count_before = prefix(counts, position)
        sum_before = prefix(sums, position)
        return sum_before + (amount - count_before) * coordinates[position]

    active: dict[tuple[int, int], int] = {}
    total_count = 0
    total_power = 0
    lightning_count = 0
    fire_count = 0
    answers: list[int] = []

    for spell_type, signed_power in operations:
        power = abs(signed_power)
        key = spell_type, power
        delta = 1 if signed_power > 0 else -1
        if delta == -1 and active.get(key, 0) == 0:
            raise ValueError("removing a missing spell")
        active[key] = active.get(key, 0) + delta
        position = coordinate_index[power]
        add(counts, position, delta)
        add(sums, position, delta * power)
        if spell_type == 0:
            add(fire_counts, position, delta)
            fire_count += delta
        else:
            lightning_count += delta
        total_count += delta
        total_power += delta * power

        selected = lightning_count
        bonus = total_power - sum_smallest(total_count - selected)
        if selected:
            threshold_position = kth(counts, total_count - selected + 1)
            count_above = total_count - prefix(counts, threshold_position + 1)
            slots_at_threshold = selected - count_above
            fire_above = fire_count - prefix(fire_counts, threshold_position + 1)
            fire_at_threshold = prefix(fire_counts, threshold_position + 1) - prefix(
                fire_counts, threshold_position
            )
            selected_has_fire = fire_above > 0 or (
                fire_at_threshold > 0 and slots_at_threshold > 0
            )
            if not selected_has_fire:
                bonus -= coordinates[threshold_position]
                if fire_count:
                    bonus += coordinates[kth(fire_counts, fire_count)]
        answers.append(total_power + bonus)
    return answers
```

Fenwick counts locate the top-`L` threshold and Fenwick sums obtain its total.
Fire counts decide whether a tie can include fire and provide the best swap when
the mandatory correction applies.

**Complexity:** `O(q log q)` time and `O(q)` space.
