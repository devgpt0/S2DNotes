# ICPC300 174: Codeforces 626F - Group Projects

**Source:** [Codeforces 626F - Group Projects](https://codeforces.com/problemset/problem/626/F)  
**Pattern:** sorted sweep DP with unfinished groups

## Exact contract

Partition `n` distinct students into nonempty, unlabeled groups. A group's
cost is its maximum skill minus its minimum skill. Count partitions whose total
cost is at most `x`, modulo `1_000_000_007`.

## First principles

Sort the skills and sweep from left to right. A group is *open* after its
minimum has been chosen but before its maximum is fixed. Across a skill gap
`d`, every open group gains exactly `d` cost, so a state needs only
`(open_groups, cost)`.

For the next student, the choices are:

- start a new open group;
- make a singleton, or append to one of the open groups without closing it;
- append to and close one of the open groups.

## Cases that decide correctness

- Students are distinct even when their skill values are equal.
- Groups are unlabeled; opening order induced by sorted students is canonical.
- A singleton opens and closes at one value and contributes zero cost.
- Only states with no open group are complete partitions.
- Equal adjacent skills add zero cost across their gap.

## Brute force: enumerate canonical set partitions

```python
MODULO = 1_000_000_007


def group_projects_brute(skills: list[int], budget: int) -> int:
    if not skills or any(type(skill) is not int for skill in skills):
        raise ValueError("skills must be a nonempty integer list")
    if type(budget) is not int or budget < 0:
        raise ValueError("budget must be a nonnegative integer")

    groups: list[tuple[int, int]] = []
    answer = 0

    def search(student: int, cost: int) -> None:
        nonlocal answer
        if cost > budget:
            return
        if student == len(skills):
            answer = (answer + 1) % MODULO
            return

        skill = skills[student]
        for group_index, (minimum, maximum) in enumerate(groups):
            replacement = min(minimum, skill), max(maximum, skill)
            groups[group_index] = replacement
            search(
                student + 1, cost + replacement[1] - replacement[0] - maximum + minimum
            )
            groups[group_index] = minimum, maximum

        groups.append((skill, skill))
        search(student + 1, cost)
        groups.pop()

    search(0, 0)
    return answer
```

Creating a new group only after all existing groups produces every set
partition once. The Bell-number running time limits this to tiny inputs.

## Better approach: no separate intermediate

Any polynomial solution must aggregate partial partitions by their number of
open groups and accumulated cost. A dense table and the sparse table below are
implementations of that same DP invariant, not different approaches.

## Expert solution: charge gaps to open groups

```python
MODULO = 1_000_000_007


def count_group_projects(skills: list[int], budget: int) -> int:
    if not skills or any(type(skill) is not int for skill in skills):
        raise ValueError("skills must be a nonempty integer list")
    if type(budget) is not int or budget < 0:
        raise ValueError("budget must be a nonnegative integer")

    ordered = sorted(skills)
    states: dict[tuple[int, int], int] = {(0, 0): 1}
    previous = ordered[0]

    for skill in ordered:
        gap = skill - previous
        following: dict[tuple[int, int], int] = {}
        for (open_groups, cost), ways in states.items():
            charged_cost = cost + open_groups * gap
            if charged_cost > budget:
                continue

            opened = (open_groups + 1, charged_cost)
            following[opened] = (following.get(opened, 0) + ways) % MODULO

            unchanged = (open_groups, charged_cost)
            following[unchanged] = (
                following.get(unchanged, 0) + ways * (open_groups + 1)
            ) % MODULO

            if open_groups:
                closed = (open_groups - 1, charged_cost)
                following[closed] = (
                    following.get(closed, 0) + ways * open_groups
                ) % MODULO
        states = following
        previous = skill

    return (
        sum(ways for (open_groups, _), ways in states.items() if open_groups == 0)
        % MODULO
    )
```

The gap charge is exact because each open group has selected a minimum on the
left and will select a maximum on the right. The three transitions enumerate
all legal roles of the current sorted student with the correct multiplicity.

**Complexity:** `O(n^2 x)` time in the dense worst case and `O(nx)` space.
