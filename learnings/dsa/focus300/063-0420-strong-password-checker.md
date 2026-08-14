# Focus300 063: LeetCode 420 - Strong Password Checker

**Source:** [LeetCode 420](https://leetcode.com/problems/strong-password-checker/)  
**Difficulty:** Hard  
**Pattern:** coordinate length, character classes, and run repairs

## Exact contract

Return the minimum insertions, deletions, and replacements needed to make a
password length `6..20`, contain a lowercase letter, uppercase letter, and
digit, and contain no three equal consecutive characters.

## First principles

For a run of length `L`, replacements needed without deletion are `L//3`.
When length exceeds 20, deletions are mandatory and should also reduce run
replacements:

- a run with `L mod 3 = 0` saves one replacement after one deletion;
- remainder one saves one after two deletions;
- remaining replacement savings cost three deletions each.

Missing character classes can be repaired by the same replacements, so take a
maximum rather than adding them.

## Cases that decide correctness

- Short passwords can use insertions to fix length, missing classes, and runs.
- Length `6..20` needs only replacements and missing-class repairs.
- Overlength passwords must pay every required deletion.
- Deletion order is determined by run length modulo three.
- Separate runs are repaired independently.

## Brute force: breadth-first search over edit operations

```python
from collections import deque


def strong_password_checker_brute(password: str) -> int:
    def strong(value: str) -> bool:
        return (
            6 <= len(value) <= 20
            and any(character.islower() for character in value)
            and any(character.isupper() for character in value)
            and any(character.isdigit() for character in value)
            and all(
                value[index] != value[index + 1] or value[index] != value[index + 2]
                for index in range(len(value) - 2)
            )
        )

    alphabet = sorted(set(password) | {"a", "A", "0"})
    maximum_length = max(6, min(len(password), 20))
    queue = deque([(password, 0)])
    seen = {password}
    while queue:
        value, distance = queue.popleft()
        if strong(value):
            return distance
        candidates: list[str] = []
        if len(value) < maximum_length:
            for index in range(len(value) + 1):
                for character in alphabet:
                    candidates.append(value[:index] + character + value[index:])
        for index in range(len(value)):
            candidates.append(value[:index] + value[index + 1 :])
            for character in alphabet:
                if character != value[index]:
                    candidates.append(value[:index] + character + value[index + 1 :])
        for candidate in candidates:
            if candidate not in seen:
                seen.add(candidate)
                queue.append((candidate, distance + 1))
    raise RuntimeError("a strong password is always reachable")
```

This is useful only for very short validation inputs because the edit graph is
exponential.

## Better insight: only run lengths modulo three affect deletion priority

Length regime fixes the mandatory operation type. Within the overlength case,
spend deletions where they reduce the replacement count with the fewest edits.

## Expert solution: greedy run deletion accounting

```python
def strong_password_checker(password: str) -> int:
    missing_types = int(not any(character.islower() for character in password))
    missing_types += int(not any(character.isupper() for character in password))
    missing_types += int(not any(character.isdigit() for character in password))

    runs: list[int] = []
    start = 0
    while start < len(password):
        end = start + 1
        while end < len(password) and password[end] == password[start]:
            end += 1
        if end - start >= 3:
            runs.append(end - start)
        start = end

    if len(password) < 6:
        return max(missing_types, 6 - len(password))

    replacements = sum(length // 3 for length in runs)
    if len(password) <= 20:
        return max(missing_types, replacements)

    deletions = len(password) - 20
    remaining = deletions
    remainder_zero = sum(length % 3 == 0 for length in runs)
    used = min(remaining, remainder_zero)
    replacements -= used
    remaining -= used

    remainder_one = sum(length % 3 == 1 for length in runs)
    used = min(remaining // 2, remainder_one)
    replacements -= used
    remaining -= 2 * used

    replacements -= min(replacements, remaining // 3)
    return deletions + max(missing_types, replacements)
```

Mandatory deletions are assigned in exact replacement-saving order; the
remaining replacements simultaneously satisfy run and character-class needs.

**Complexity:** `O(n)` time and `O(number_of_runs)` space.
