# ICPC300 202: Codeforces 580E - Kefa and Watch

**Source:** [Codeforces 580E - Kefa and Watch](https://codeforces.com/problemset/problem/580/E)  
**Difficulty:** 2300  
**Pattern:** lazy range assignment with position-weighted hashes

## Exact contract

Maintain a decimal string under zero-based half-open operations:

- `("assign", left, right, digit)` replaces every position in `[left, right)`;
- `("equal", left, right, shift)` asks whether
  `text[left:right-shift] == text[left+shift:right]`.

Return the Boolean answers in query order.

## First principles

Store `sum(digit[i] * base^i)` for every segment under two moduli. A range
assignment becomes `digit * sum(base^i)` for that interval. The two queried
pieces keep global exponents, so shifting the left hash by `shift` aligns it
with the right hash.

## Cases that decide correctness

- Assignment overwrites, rather than adds to, an older lazy tag.
- Query pieces always have equal length.
- Digit zero legitimately has hash zero.
- Additions and comparisons use both moduli.
- Lazy tags must be pushed before partial updates or queries.

## Brute force: mutate a character list

```python
def kefa_watch_brute(
    text: str, operations: list[tuple[str, int, int, int]]
) -> list[bool]:
    if not text or any(character < "0" or character > "9" for character in text):
        raise ValueError("text must be a nonempty decimal string")
    characters = list(text)
    answers: list[bool] = []
    for action, left, right, value in operations:
        if (
            type(left) is not int
            or type(right) is not int
            or not 0 <= left < right <= len(characters)
        ):
            raise ValueError("invalid interval")
        if action == "assign":
            if type(value) is not int or not 0 <= value <= 9:
                raise ValueError("assignment digit must be in [0, 9]")
            characters[left:right] = [str(value)] * (right - left)
        elif action == "equal":
            if type(value) is not int or not 0 < value < right - left:
                raise ValueError("shift must be inside the interval")
            answers.append(
                characters[left : right - value] == characters[left + value : right]
            )
        else:
            raise ValueError("unknown operation")
    return answers
```

Assignments and comparisons take linear time in the interval length.

## Better approach: no separate intermediate

Rebuilding prefix hashes after every assignment makes queries constant-time but
updates `O(n)`. Once hashes must be maintained hierarchically, range assignment
requires the same lazy segment-tree invariant used below.

## Expert solution: double-hash lazy segment tree

```python
def kefa_watch(text: str, operations: list[tuple[str, int, int, int]]) -> list[bool]:
    if not text or any(character < "0" or character > "9" for character in text):
        raise ValueError("text must be a nonempty decimal string")
    size = len(text)
    base = 911_382_323
    moduli = (1_000_000_007, 1_000_000_009)

    powers: list[list[int]] = []
    power_sums: list[list[int]] = []
    for modulus in moduli:
        current_powers = [1] * (size + 1)
        current_sums = [0] * (size + 1)
        reduced_base = base % modulus
        for index in range(size):
            current_powers[index + 1] = current_powers[index] * reduced_base % modulus
            current_sums[index + 1] = (
                current_sums[index] + current_powers[index]
            ) % modulus
        powers.append(current_powers)
        power_sums.append(current_sums)

    tree = [[0] * (4 * size) for _ in moduli]
    lazy = [-1] * (4 * size)

    def pull(node: int) -> None:
        for hash_index, modulus in enumerate(moduli):
            tree[hash_index][node] = (
                tree[hash_index][node * 2] + tree[hash_index][node * 2 + 1]
            ) % modulus

    def apply(node: int, left: int, right: int, digit: int) -> None:
        for hash_index, modulus in enumerate(moduli):
            geometric_sum = (
                power_sums[hash_index][right] - power_sums[hash_index][left]
            ) % modulus
            tree[hash_index][node] = digit * geometric_sum % modulus
        lazy[node] = digit

    def build(node: int, left: int, right: int) -> None:
        if right - left == 1:
            apply(node, left, right, ord(text[left]) - ord("0"))
            return
        middle = (left + right) // 2
        build(node * 2, left, middle)
        build(node * 2 + 1, middle, right)
        pull(node)
        lazy[node] = -1

    def push(node: int, left: int, right: int) -> None:
        digit = lazy[node]
        if digit == -1 or right - left == 1:
            return
        middle = (left + right) // 2
        apply(node * 2, left, middle, digit)
        apply(node * 2 + 1, middle, right, digit)
        lazy[node] = -1

    def assign(
        node: int,
        left: int,
        right: int,
        query_left: int,
        query_right: int,
        digit: int,
    ) -> None:
        if query_right <= left or right <= query_left:
            return
        if query_left <= left and right <= query_right:
            apply(node, left, right, digit)
            return
        push(node, left, right)
        middle = (left + right) // 2
        assign(node * 2, left, middle, query_left, query_right, digit)
        assign(node * 2 + 1, middle, right, query_left, query_right, digit)
        pull(node)

    def query(
        node: int, left: int, right: int, query_left: int, query_right: int
    ) -> tuple[int, int]:
        if query_right <= left or right <= query_left:
            return 0, 0
        if query_left <= left and right <= query_right:
            return tree[0][node], tree[1][node]
        push(node, left, right)
        middle = (left + right) // 2
        first = query(node * 2, left, middle, query_left, query_right)
        second = query(node * 2 + 1, middle, right, query_left, query_right)
        return (
            (first[0] + second[0]) % moduli[0],
            (first[1] + second[1]) % moduli[1],
        )

    build(1, 0, size)
    answers: list[bool] = []
    for action, left, right, value in operations:
        if (
            type(left) is not int
            or type(right) is not int
            or not 0 <= left < right <= size
        ):
            raise ValueError("invalid interval")
        if action == "assign":
            if type(value) is not int or not 0 <= value <= 9:
                raise ValueError("assignment digit must be in [0, 9]")
            assign(1, 0, size, left, right, value)
        elif action == "equal":
            if type(value) is not int or not 0 < value < right - left:
                raise ValueError("shift must be inside the interval")
            first = query(1, 0, size, left, right - value)
            second = query(1, 0, size, left + value, right)
            answers.append(
                all(
                    first[index] * powers[index][value] % moduli[index] == second[index]
                    for index in range(2)
                )
            )
        else:
            raise ValueError("unknown operation")
    return answers
```

Each node hash exactly represents its current digits at global powers. Lazy
assignment preserves that invariant, and aligned double hashes compare the two
equal-length pieces.

**Complexity:** `O((n+q) log n)` time and `O(n)` space.
