# Focus300 089: LeetCode 639 - Decode Ways II

**Source:** [LeetCode 639](https://leetcode.com/problems/decode-ways-ii/)  
**Difficulty:** Hard  
**Pattern:** multiplicity-aware rolling dynamic programming

## Exact contract

Count decodings of a nonempty string containing decimal digits and `*`, where
`1` through `26` map to `A` through `Z` and each `*` independently represents
one digit from `1` through `9`. Zero is valid only as part of `10` or `20`.
Return the count modulo `1_000_000_007`; length is at most 100,000.

## First principles

Every decoding ends with either one encoded character or two. The number of
ways contributed by those endings depends only on the last one or two source
symbols. Wildcards change the multiplier: `*` has nine single-digit choices,
while `**` has fifteen valid two-digit choices (`11..19` and `21..26`).

## Cases that decide correctness

- A leading `0` has no decoding.
- `*0` has two pair interpretations: `10` and `20`.
- `1*` has nine pair interpretations, `2*` has six, and `3*` has none.
- `**` contributes 15 as a pair, not 81.
- Apply the modulus throughout, not only after enormous intermediate counts.

## Brute force: expand every wildcard

```python
from itertools import product


MODULO = 1_000_000_007


def decode_ways_wildcard_brute(encoded: str) -> int:
    if type(encoded) is not str:
        raise TypeError("encoded must be a string")
    if not 1 <= len(encoded) <= 100_000:
        raise ValueError("encoded length must be between 1 and 100000")
    if any(character not in "0123456789*" for character in encoded):
        raise ValueError("encoded may contain only decimal digits and '*'")

    answer = 0
    for replacements in product("123456789", repeat=encoded.count("*")):
        replacement_iterator = iter(replacements)
        expanded = "".join(
            next(replacement_iterator) if character == "*" else character
            for character in encoded
        )
        previous_two = 1
        previous_one = int(expanded[0] != "0")
        for index in range(1, len(expanded)):
            current = previous_one if expanded[index] != "0" else 0
            if "10" <= expanded[index - 1 : index + 1] <= "26":
                current += previous_two
            previous_two, previous_one = previous_one, current
        answer = (answer + previous_one) % MODULO
    return answer
```

With `w` wildcards, this takes `O(9^w * n)` time and `O(n)` expansion space.

## Better approach: store a DP value for every prefix

For each prefix length, combine the previous prefix through a valid single
symbol and the prefix two positions back through a valid pair. A full array
gives `O(n)` time and `O(n)` space; only its final two values are ever needed.

## Expert solution: roll two multiplicity-weighted states

```python
MODULO = 1_000_000_007


def decode_ways_wildcard(encoded: str) -> int:
    if type(encoded) is not str:
        raise TypeError("encoded must be a string")
    if not 1 <= len(encoded) <= 100_000:
        raise ValueError("encoded length must be between 1 and 100000")
    if any(character not in "0123456789*" for character in encoded):
        raise ValueError("encoded may contain only decimal digits and '*'")

    def single_ways(character: str) -> int:
        if character == "*":
            return 9
        return int(character != "0")

    def pair_ways(first: str, second: str) -> int:
        if first == "*" and second == "*":
            return 15
        if first == "*":
            return 2 if second <= "6" else 1
        if second == "*":
            if first == "1":
                return 9
            if first == "2":
                return 6
            return 0
        return int("10" <= first + second <= "26")

    previous_two = 1
    previous_one = single_ways(encoded[0])
    for index in range(1, len(encoded)):
        current = (
            previous_one * single_ways(encoded[index])
            + previous_two * pair_ways(encoded[index - 1], encoded[index])
        ) % MODULO
        previous_two, previous_one = previous_one, current
    return previous_one
```

The two terms partition decodings by whether their final letter consumes one
or two symbols. The helper multipliers count exactly the wildcard assignments
valid for that final letter.

**Complexity:** `O(n)` time and `O(1)` auxiliary space.
