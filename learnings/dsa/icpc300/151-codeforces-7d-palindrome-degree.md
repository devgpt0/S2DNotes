# ICPC300 151: Codeforces 7D - Palindrome Degree

**Source:** [Codeforces 7D - Palindrome Degree](https://codeforces.com/problemset/problem/7/D)  
**Rating:** 2200  
**Pattern:** prefix-palindrome detection plus recursive prefix DP  
**Goal:** Sum the palindrome degrees of every prefix of a lowercase string.
A non-palindrome has degree `0`; a palindrome has degree one plus the degree
of its first half.

## 1. First principles

Only prefix lengths matter. If the prefix of length `length` is a palindrome,
its first half is also a prefix, so

```text
degree[length] = 1 + degree[length // 2]
```

Otherwise its degree is zero. The remaining problem is to recognize all
palindromic prefixes without comparing each one from scratch.

## 2. Cases that decide correctness

- Every one-character prefix has degree `1`.
- An even palindrome recurses into its first `length / 2` characters.
- An odd palindrome discards its middle character when taking the first half.
- A non-palindromic prefix contributes zero even if its first half is deep.
- The empty prefix is only the recurrence base and is not included in the sum.

## 3. Brute force: inspect every recursive half

```python
def palindrome_degree_brute(text: str) -> int:
    if not text.islower() or not text.isalpha():
        raise ValueError("text must contain lowercase letters")

    total = 0
    for length in range(1, len(text) + 1):
        current = text[:length]
        degree = 0
        while current == current[::-1]:
            degree += 1
            current = current[: len(current) // 2]
            if not current:
                break
        total += degree
    return total
```

**Complexity:** `O(n^2)` time and `O(n)` temporary space.

## 4. Better: two rolling hashes

```python
def palindrome_degree_hash(text: str) -> int:
    if not text.islower() or not text.isalpha():
        raise ValueError("text must contain lowercase letters")

    moduli = (1_000_000_007, 1_000_000_009)
    base = 911_382_323
    forward = [0, 0]
    backward = [0, 0]
    powers = [1, 1]
    degrees = [0] * (len(text) + 1)
    answer = 0

    for length, character in enumerate(text, start=1):
        value = ord(character) - ord("a") + 1
        for index, modulus in enumerate(moduli):
            forward[index] = (forward[index] * base + value) % modulus
            backward[index] = (backward[index] + value * powers[index]) % modulus
            powers[index] = powers[index] * base % modulus
        if forward == backward:
            degrees[length] = degrees[length // 2] + 1
            answer += degrees[length]
    return answer
```

**Complexity:** `O(n)` time and `O(n)` space. Double hashing makes collisions
negligible but does not make them impossible.

## 5. Expert solution: deterministic Manacher radii

```python
def palindrome_degree_manacher(text: str) -> int:
    if not text.islower() or not text.isalpha():
        raise ValueError("text must contain lowercase letters")
    length = len(text)

    odd = [0] * length
    left = 0
    right = -1
    for center in range(length):
        radius = (
            1 if center > right else min(odd[left + right - center], right - center + 1)
        )
        while (
            center - radius >= 0
            and center + radius < length
            and text[center - radius] == text[center + radius]
        ):
            radius += 1
        odd[center] = radius
        if center + radius - 1 > right:
            left = center - radius + 1
            right = center + radius - 1

    even = [0] * length
    left = 0
    right = -1
    for center in range(length):
        radius = (
            0
            if center > right
            else min(even[left + right - center + 1], right - center + 1)
        )
        while (
            center - radius - 1 >= 0
            and center + radius < length
            and text[center - radius - 1] == text[center + radius]
        ):
            radius += 1
        even[center] = radius
        if center + radius - 1 > right:
            left = center - radius
            right = center + radius - 1

    degrees = [0] * (length + 1)
    answer = 0
    for prefix_length in range(1, length + 1):
        if prefix_length % 2 == 1:
            center = prefix_length // 2
            is_palindrome = odd[center] >= center + 1
        else:
            center = prefix_length // 2
            is_palindrome = even[center] >= center
        if is_palindrome:
            degrees[prefix_length] = degrees[prefix_length // 2] + 1
            answer += degrees[prefix_length]
    return answer
```

### Why the expert code is correct

Manacher's odd and even radii state exactly how far a palindrome extends from
each center. The center of a prefix is fixed by its length, so one radius test
recognizes that prefix deterministically. The recurrence then follows the
definition and refers only to an already processed shorter prefix.

**Complexity:** `O(n)` time and `O(n)` space.

## 6. What to remember

```text
palindromic prefix -> 1 + degree[first half]
all prefix-palindrome tests -> Manacher radii
shorter-half state is already known -> one forward DP pass
```
