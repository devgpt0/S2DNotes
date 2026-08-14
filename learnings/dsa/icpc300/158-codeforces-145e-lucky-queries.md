# ICPC300 158: Codeforces 145E - Lucky Queries

**Source:** [Codeforces 145E - Lucky Queries](https://codeforces.com/problemset/problem/145/E)  
**Rating:** 2400  
**Pattern:** segment tree with four subsequence summaries and a flip tag  
**Goal:** Maintain a string of `4` and `7` under range flips. A `count`
operation asks for the longest subsequence of the whole string whose digits are
nondecreasing: zero or more `4`s followed by zero or more `7`s.

The code uses zero-based inclusive switch ranges; subtract one from the source
input.

## 1. First principles

For each segment store four values:

```text
count4, count7, best47, best74
```

For adjacent segments `left + right`, a best `4...7` subsequence either uses
all available `4`s from the left before a best `4...7` from the right, or a
best `4...7` from the left before all available `7`s from the right:

```text
best47 = max(left.count4 + right.best47,
             left.best47 + right.count7)
```

Flipping swaps `count4` with `count7` and swaps `best47` with `best74`.

## 2. Cases that decide correctness

- A one-character segment has both monotone-subsequence lengths equal to one.
- A valid answer may contain only `4`s or only `7`s.
- Switch ranges are inclusive.
- Two flips on the same segment cancel, so the lazy tag is a Boolean XOR.
- The answer is always the root's `best47`, not a substring length.

## 3. Brute force: enumerate every subsequence on count

```python
def lucky_queries_brute(
    text: str,
    operations: list[tuple[str] | tuple[str, int, int]],
) -> list[int]:
    if not text or any(character not in "47" for character in text):
        raise ValueError("text must be a nonempty string of 4 and 7")

    current = list(text)
    answers: list[int] = []
    for operation in operations:
        command = operation[0]
        if command == "switch":
            if len(operation) != 3:
                raise ValueError("switch requires two endpoints")
            left, right = operation[1], operation[2]
            if not 0 <= left <= right < len(current):
                raise ValueError("invalid switch range")
            for index in range(left, right + 1):
                current[index] = "7" if current[index] == "4" else "4"
        elif command == "count":
            if len(operation) != 1:
                raise ValueError("count has no endpoints")
            answer = 0
            for chosen in range(1 << len(current)):
                seen_seven = False
                length = 0
                valid = True
                for index, character in enumerate(current):
                    if chosen >> index & 1 == 0:
                        continue
                    if character == "4" and seen_seven:
                        valid = False
                        break
                    seen_seven |= character == "7"
                    length += 1
                if valid:
                    answer = max(answer, length)
            answers.append(answer)
        else:
            raise ValueError("unknown operation")
    return answers
```

**Complexity:** `O(q n 2^n)` time and `O(n+q)` space.

## 4. Better: rescan after every switch

```python
def lucky_queries_scan(
    text: str,
    operations: list[tuple[str] | tuple[str, int, int]],
) -> list[int]:
    if not text or any(character not in "47" for character in text):
        raise ValueError("text must be a nonempty string of 4 and 7")

    current = list(text)
    answers: list[int] = []
    for operation in operations:
        command = operation[0]
        if command == "switch":
            if len(operation) != 3:
                raise ValueError("switch requires two endpoints")
            left, right = operation[1], operation[2]
            if not 0 <= left <= right < len(current):
                raise ValueError("invalid switch range")
            for index in range(left, right + 1):
                current[index] = "7" if current[index] == "4" else "4"
        elif command == "count":
            if len(operation) != 1:
                raise ValueError("count has no endpoints")
            count4 = 0
            best47 = 0
            for character in current:
                if character == "4":
                    count4 += 1
                    best47 = max(best47, count4)
                else:
                    best47 += 1
            answers.append(best47)
        else:
            raise ValueError("unknown operation")
    return answers
```

**Complexity:** `O(qn)` time and `O(n+q)` space.

## 5. Expert solution: lazy four-state segment tree

```python
def lucky_queries_segment_tree(
    text: str,
    operations: list[tuple[str] | tuple[str, int, int]],
) -> list[int]:
    if not text or any(character not in "47" for character in text):
        raise ValueError("text must be a nonempty string of 4 and 7")

    size = len(text)
    count4 = [0] * (4 * size)
    count7 = [0] * (4 * size)
    best47 = [0] * (4 * size)
    best74 = [0] * (4 * size)
    flipped = [False] * (4 * size)

    def merge(node: int) -> None:
        left = 2 * node
        right = left + 1
        count4[node] = count4[left] + count4[right]
        count7[node] = count7[left] + count7[right]
        best47[node] = max(
            count4[left] + best47[right],
            best47[left] + count7[right],
        )
        best74[node] = max(
            count7[left] + best74[right],
            best74[left] + count4[right],
        )

    def build(node: int, left: int, right: int) -> None:
        if left == right:
            count4[node] = int(text[left] == "4")
            count7[node] = int(text[left] == "7")
            best47[node] = 1
            best74[node] = 1
            return
        middle = (left + right) // 2
        build(2 * node, left, middle)
        build(2 * node + 1, middle + 1, right)
        merge(node)

    def apply_flip(node: int) -> None:
        count4[node], count7[node] = count7[node], count4[node]
        best47[node], best74[node] = best74[node], best47[node]
        flipped[node] = not flipped[node]

    def push(node: int) -> None:
        if not flipped[node]:
            return
        apply_flip(2 * node)
        apply_flip(2 * node + 1)
        flipped[node] = False

    def update(
        node: int,
        left: int,
        right: int,
        update_left: int,
        update_right: int,
    ) -> None:
        if update_left <= left and right <= update_right:
            apply_flip(node)
            return
        push(node)
        middle = (left + right) // 2
        if update_left <= middle:
            update(2 * node, left, middle, update_left, update_right)
        if update_right > middle:
            update(
                2 * node + 1,
                middle + 1,
                right,
                update_left,
                update_right,
            )
        merge(node)

    build(1, 0, size - 1)
    answers: list[int] = []
    for operation in operations:
        command = operation[0]
        if command == "switch":
            if len(operation) != 3:
                raise ValueError("switch requires two endpoints")
            left, right = operation[1], operation[2]
            if not 0 <= left <= right < size:
                raise ValueError("invalid switch range")
            update(1, 0, size - 1, left, right)
        elif command == "count":
            if len(operation) != 1:
                raise ValueError("count has no endpoints")
            answers.append(best47[1])
        else:
            raise ValueError("unknown operation")
    return answers
```

### Why the expert code is correct

The four stored values describe every way a monotone two-symbol subsequence can
cross a segment boundary. The merge checks both possible locations of that
boundary. Flipping exchanges the roles of `4` and `7`, so swapping both count
and direction pairs transforms the summary exactly without visiting leaves.
Thus the root summary remains correct after every range flip.

**Complexity:** `O(n + q log n)` time and `O(n+q)` space.

## 6. What to remember

```text
two-symbol monotone subsequence -> store both directions
concatenate segments -> try the split in both summaries
flip 4 and 7 -> swap counts and directional answers
```
