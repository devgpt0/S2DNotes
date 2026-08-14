# ICPC300 262: Codeforces 1316E - Team Building

**Source:** [Codeforces 1316E - Team Building](https://codeforces.com/problemset/problem/1316/E)  
**Rating:** 2200  
**Pattern:** sorted candidates plus role-mask dynamic programming  
**Goal:** Assign distinct people to every specialist role and choose at most
`audience_limit` other people for their audience values. Maximize the total.

## 1. First principles

There are at most seven specialist roles, so a bitmask can record exactly which
ones are filled. Sort people by audience value from largest to smallest.

After processing `index` people with `mask.bit_count()` specialists, exactly
`index - mask.bit_count()` processed people were available for the audience.
If that number is below the limit, taking the current non-specialist audience
value is always optimal because later values are no larger.

## 2. Cases that decide correctness

- One person cannot fill two roles or be both a specialist and audience member.
- Exactly every role must be filled; the audience may use fewer people.
- Equal audience values can be processed in any order.
- A zero audience limit removes only the audience transition.
- There must be at least as many people as specialist roles.

## 3. Brute force: enumerate specialist assignments

```python
from itertools import permutations


def maximum_team_score_brute(
    audience: list[int],
    skills: list[list[int]],
    audience_limit: int,
) -> int:
    if (
        not audience
        or type(audience_limit) is not int
        or not 0 <= audience_limit <= len(audience)
        or len(skills) != len(audience)
        or any(type(value) is not int or value < 0 for value in audience)
    ):
        raise ValueError("invalid audience data")
    role_count = len(skills[0])
    if role_count > len(audience) or any(
        len(row) != role_count
        or any(type(value) is not int or value < 0 for value in row)
        for row in skills
    ):
        raise ValueError("invalid skill matrix")

    answer = -1
    for assigned in permutations(range(len(audience)), role_count):
        specialists = set(assigned)
        score = sum(skills[person][role] for role, person in enumerate(assigned))
        remaining = sorted(
            (
                audience[person]
                for person in range(len(audience))
                if person not in specialists
            ),
            reverse=True,
        )
        answer = max(answer, score + sum(remaining[:audience_limit]))
    return answer
```

**Complexity:** `O(P(n, p) * (n log n + p))` time and `O(n)` space.

## 4. Better approach: mask DP without sorting

A DP may track both the role mask and the number of audience members chosen.
That is correct but adds a factor of `audience_limit`. Sorting makes the
audience count implicit.

## 5. Expert solution: greedy audience slots inside mask DP

```python
def maximum_team_score(
    audience: list[int],
    skills: list[list[int]],
    audience_limit: int,
) -> int:
    if (
        not audience
        or type(audience_limit) is not int
        or not 0 <= audience_limit <= len(audience)
        or len(skills) != len(audience)
        or any(type(value) is not int or value < 0 for value in audience)
    ):
        raise ValueError("invalid audience data")
    role_count = len(skills[0])
    if role_count > len(audience) or any(
        len(row) != role_count
        or any(type(value) is not int or value < 0 for value in row)
        for row in skills
    ):
        raise ValueError("invalid skill matrix")

    people = sorted(
        zip(audience, skills, strict=True),
        key=lambda person: person[0],
        reverse=True,
    )
    unreachable = -1
    dp = [unreachable] * (1 << role_count)
    dp[0] = 0
    for index, (base_value, role_values) in enumerate(people):
        next_dp = [unreachable] * len(dp)
        for mask, score in enumerate(dp):
            if score == unreachable:
                continue
            audience_used = index - mask.bit_count()
            non_specialist_score = score
            if audience_used < audience_limit:
                non_specialist_score += base_value
            next_dp[mask] = max(next_dp[mask], non_specialist_score)
            for role, role_value in enumerate(role_values):
                if not mask >> role & 1:
                    next_mask = mask | 1 << role
                    next_dp[next_mask] = max(next_dp[next_mask], score + role_value)
        dp = next_dp
    return dp[-1]
```

### Why the expert code is correct

Every transition makes the current person either a specialist or a
non-specialist. For a fixed role mask, sorting proves that the first available
non-specialists fill the audience quota optimally. Thus the DP enumerates all
specialist assignments while greedily making the only optimal audience choice.

**Complexity:** `O(n p 2^p)` time and `O(2^p)` space.

## 6. What to remember

```text
few roles -> subset mask
sort by base value -> audience choice becomes forced
processed minus specialists -> audience slots already encountered
```
