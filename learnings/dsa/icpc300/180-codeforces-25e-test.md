# ICPC300 180: Codeforces 25E - Test

**Source:** [Codeforces 25E - Test](https://codeforces.com/problemset/problem/25/E)  
**Pattern:** three-string shortest common superstring by overlap permutations

## Exact contract

Given exactly three nonempty lowercase strings, output the minimum length of a
string containing all three as substrings.

## First principles

Remove any input already contained in another input. For a fixed order of the
remaining strings, the shortest superstring uses the largest suffix-prefix
overlap at each join. With at most three strings, enumerate every order and
take the shortest result.

KMP computes the overlap of `left` into `right`: the final prefix-function value
of `right + separator + left` is the longest prefix of `right` that is a suffix
of `left`.

## Cases that decide correctness

- Duplicate strings collapse to one required substring.
- A string contained anywhere inside another needs no separate join.
- Overlap direction matters, so all permutations are required.
- A later string may already be contained in the current merged text.
- The overlap may be zero or the full length of the appended string.

## Brute force: enumerate candidate texts by length

```python
from itertools import product


def shortest_test_superstring_brute(strings: list[str]) -> int:
    if len(strings) != 3 or any(
        not text or any(character < "a" or character > "z" for character in text)
        for text in strings
    ):
        raise ValueError("exactly three nonempty lowercase strings are required")

    alphabet = sorted(set("".join(strings)))
    for length in range(max(map(len, strings)), sum(map(len, strings)) + 1):
        for characters in product(alphabet, repeat=length):
            candidate = "".join(characters)
            if all(text in candidate for text in strings):
                return length
    raise RuntimeError("a concatenation is always a valid superstring")
```

The alphabetic product makes this useful only for very small strings.

## Better approach: direct overlap checks

```python
from itertools import permutations


def shortest_test_superstring_direct(strings: list[str]) -> int:
    if len(strings) != 3 or any(
        not text or any(character < "a" or character > "z" for character in text)
        for text in strings
    ):
        raise ValueError("exactly three nonempty lowercase strings are required")

    unique = list(dict.fromkeys(strings))
    required = [
        text
        for text in unique
        if not any(text != candidate and text in candidate for candidate in unique)
    ]

    def merge(left: str, right: str) -> str:
        if right in left:
            return left
        for overlap in range(min(len(left), len(right)), -1, -1):
            if left.endswith(right[:overlap]):
                return left + right[overlap:]
        raise RuntimeError("zero overlap always exists")

    if len(required) == 1:
        return len(required[0])

    def merged_length(order: tuple[str, ...]) -> int:
        combined = order[0]
        for text in order[1:]:
            combined = merge(combined, text)
        return len(combined)

    return min(merged_length(order) for order in permutations(required))
```

This is simple but repeated slicing and suffix comparison can take quadratic
time in the string lengths.

## Expert solution: KMP overlap for every permutation

```python
from itertools import permutations


def shortest_test_superstring(strings: list[str]) -> int:
    if len(strings) != 3 or any(
        not text or any(character < "a" or character > "z" for character in text)
        for text in strings
    ):
        raise ValueError("exactly three nonempty lowercase strings are required")

    unique = list(dict.fromkeys(strings))
    required = [
        text
        for text in unique
        if not any(text != candidate and text in candidate for candidate in unique)
    ]

    def merge(left: str, right: str) -> str:
        if right in left:
            return left
        combined = right + "#" + left
        prefix = [0] * len(combined)
        border = 0
        for index in range(1, len(combined)):
            while border and combined[index] != combined[border]:
                border = prefix[border - 1]
            if combined[index] == combined[border]:
                border += 1
            prefix[index] = border
        return left + right[prefix[-1] :]

    if len(required) == 1:
        return len(required[0])

    def merged_length(order: tuple[str, ...]) -> int:
        combined = order[0]
        for text in order[1:]:
            combined = merge(combined, text)
        return len(combined)

    return min(merged_length(order) for order in permutations(required))
```

For each fixed order, maximal adjacent overlap gives its shortest possible
superstring. Every shortest common superstring induces some order of first
appearances, so enumerating all orders includes an optimum.

**Complexity:** `O(total_input_length)` time up to the constant six
permutations, and `O(total_input_length)` auxiliary space.
