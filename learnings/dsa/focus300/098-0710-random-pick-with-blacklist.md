# Focus300 098: LeetCode 710 - Random Pick with Blacklist

**Source:** [LeetCode 710](https://leetcode.com/problems/random-pick-with-blacklist/)  
**Difficulty:** Hard  
**Pattern:** compact-domain random sampling with sparse remapping

## Exact contract

Initialize with `n` and distinct blacklisted integers from `[0, n)`, leaving at
least one allowed value. Each `pick()` must return every allowed integer with
equal probability. The follow-up requires few random-generator calls and memory
proportional to the blacklist rather than to `n`.

## First principles

Let `allowed_count = n - len(blacklist)`. One uniform draw from
`[0, allowed_count)` already has the correct number of equally likely outcomes.
Every blacklisted value inside that compact range can be bijectively remapped
to an allowed value in `[allowed_count, n)`. Unblocked compact values map to
themselves.

## Cases that decide correctness

- The blacklist may be empty.
- Almost every value may be blocked.
- Only blocked values below `allowed_count` need mappings.
- Upper-range blocked values must be skipped as replacement targets.
- Each expert `pick()` must make exactly one uniform random draw.

## Brute force: rejection sampling

```python
from collections.abc import Callable
import secrets


class RejectionBlacklistPicker:
    def __init__(
        self,
        upper_bound: int,
        blacklist: list[int],
        random_index: Callable[[int], int] = secrets.randbelow,
    ) -> None:
        if type(upper_bound) is not int or not 1 <= upper_bound <= 1_000_000_000:
            raise ValueError("upper_bound must be an integer in the source range")
        if type(blacklist) is not list or len(blacklist) > min(
            100_000, upper_bound - 1
        ):
            raise ValueError("blacklist length is outside the source range")
        if any(
            type(value) is not int or not 0 <= value < upper_bound
            for value in blacklist
        ):
            raise ValueError("blacklist values must be integers in [0, upper_bound)")
        if len(blacklist) != len(set(blacklist)):
            raise ValueError("blacklist values must be distinct")
        if not callable(random_index):
            raise TypeError("random_index must be callable")
        self._upper_bound = upper_bound
        self._blocked = set(blacklist)
        self._random_index = random_index

    def pick(self) -> int:
        while True:
            candidate = self._random_index(self._upper_bound)
            if type(candidate) is not int or not 0 <= candidate < self._upper_bound:
                raise RuntimeError("random_index returned an invalid index")
            if candidate not in self._blocked:
                return candidate
```

It is uniform, but when `A` of `n` values are allowed it needs `n/A` random
draws on average and has no finite worst-case number of draws.

## Better approach: materialize all allowed values

```python
from collections.abc import Callable
import secrets


class AllowedArrayPicker:
    def __init__(
        self,
        upper_bound: int,
        blacklist: list[int],
        random_index: Callable[[int], int] = secrets.randbelow,
    ) -> None:
        if type(upper_bound) is not int or not 1 <= upper_bound <= 1_000_000_000:
            raise ValueError("upper_bound must be an integer in the source range")
        if type(blacklist) is not list or len(blacklist) > min(
            100_000, upper_bound - 1
        ):
            raise ValueError("blacklist length is outside the source range")
        if any(
            type(value) is not int or not 0 <= value < upper_bound
            for value in blacklist
        ):
            raise ValueError("blacklist values must be integers in [0, upper_bound)")
        if len(blacklist) != len(set(blacklist)):
            raise ValueError("blacklist values must be distinct")
        if not callable(random_index):
            raise TypeError("random_index must be callable")
        blocked = set(blacklist)
        self._allowed = [value for value in range(upper_bound) if value not in blocked]
        self._random_index = random_index

    def pick(self) -> int:
        index = self._random_index(len(self._allowed))
        if type(index) is not int or not 0 <= index < len(self._allowed):
            raise RuntimeError("random_index returned an invalid index")
        return self._allowed[index]
```

One draw is enough, but initialization takes `O(n)` time and space.

## Expert solution: remap blocked compact indices

```python
from collections.abc import Callable
import secrets


class BlacklistPicker:
    def __init__(
        self,
        upper_bound: int,
        blacklist: list[int],
        random_index: Callable[[int], int] = secrets.randbelow,
    ) -> None:
        if type(upper_bound) is not int or not 1 <= upper_bound <= 1_000_000_000:
            raise ValueError("upper_bound must be an integer in the source range")
        if type(blacklist) is not list or len(blacklist) > min(
            100_000, upper_bound - 1
        ):
            raise ValueError("blacklist length is outside the source range")
        if any(
            type(value) is not int or not 0 <= value < upper_bound
            for value in blacklist
        ):
            raise ValueError("blacklist values must be integers in [0, upper_bound)")
        blocked = set(blacklist)
        if len(blocked) != len(blacklist):
            raise ValueError("blacklist values must be distinct")
        if not callable(random_index):
            raise TypeError("random_index must be callable")

        self._allowed_count = upper_bound - len(blocked)
        self._mapping: dict[int, int] = {}
        self._random_index = random_index
        replacement = self._allowed_count
        for blocked_value in sorted(
            value for value in blocked if value < self._allowed_count
        ):
            while replacement in blocked:
                replacement += 1
            self._mapping[blocked_value] = replacement
            replacement += 1

    def pick(self) -> int:
        compact_index = self._random_index(self._allowed_count)
        if (
            type(compact_index) is not int
            or not 0 <= compact_index < self._allowed_count
        ):
            raise RuntimeError("random_index returned an invalid index")
        return self._mapping.get(compact_index, compact_index)
```

The mapping is a bijection from compact outcomes to allowed values, so a
uniform compact draw remains uniform after remapping.

**Complexity:** `O(B)` expected initialization time and space for blacklist
size `B`, then `O(1)` time and exactly one random draw per `pick()`.
