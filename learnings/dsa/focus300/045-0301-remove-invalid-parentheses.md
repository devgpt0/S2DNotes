# Focus300 045: LeetCode 301 - Remove Invalid Parentheses

**Source:** [LeetCode 301](https://leetcode.com/problems/remove-invalid-parentheses/)  
**Difficulty:** Hard  
**Pattern:** minimum-removal counting and constrained DFS

## Exact contract

Given a nonempty string of lowercase letters and parentheses, remove the
minimum number of parentheses needed to make it valid. Return every distinct
result and no non-minimal result. Letters cannot be removed. Output order is
unrestricted.

## First principles

A scan determines the unavoidable removals: unmatched closing parentheses and
opening parentheses left unmatched at the end. DFS then chooses exactly those
removals while maintaining a nonnegative open-parenthesis balance.

## Cases that decide correctness

- Letters never affect balance and must remain.
- A prefix may never contain more kept `)` than kept `(`.
- Duplicate parentheses can produce the same text through different removals.
- The empty string is a valid result when all parentheses must be removed.
- Every returned string uses the same minimum removal count.

## Brute force: inspect every parenthesis subset

```python
def remove_invalid_parentheses_brute(text: str) -> list[str]:
    if not text or any(
        character not in "()" and not "a" <= character <= "z" for character in text
    ):
        raise ValueError("text must contain lowercase letters and parentheses")

    positions = [index for index, character in enumerate(text) if character in "()"]
    position_bit = {position: bit for bit, position in enumerate(positions)}

    def valid(candidate: str) -> bool:
        balance = 0
        for character in candidate:
            if character == "(":
                balance += 1
            elif character == ")":
                balance -= 1
                if balance < 0:
                    return False
        return balance == 0

    best_removed = len(positions) + 1
    answers: set[str] = set()
    for removed_mask in range(1 << len(positions)):
        removed = removed_mask.bit_count()
        if removed > best_removed:
            continue
        candidate = "".join(
            character
            for index, character in enumerate(text)
            if index not in position_bit or removed_mask >> position_bit[index] & 1 == 0
        )
        if not valid(candidate):
            continue
        if removed < best_removed:
            best_removed = removed
            answers.clear()
        answers.add(candidate)
    return sorted(answers)
```

This is `O(2^p * n)` time for `p` parentheses.

## Better approach: breadth-first search by removal count

```python
def remove_invalid_parentheses_bfs(text: str) -> list[str]:
    if not text or any(
        character not in "()" and not "a" <= character <= "z" for character in text
    ):
        raise ValueError("text must contain lowercase letters and parentheses")

    def valid(candidate: str) -> bool:
        balance = 0
        for character in candidate:
            if character == "(":
                balance += 1
            elif character == ")":
                balance -= 1
                if balance < 0:
                    return False
        return balance == 0

    level = {text}
    while level:
        answers = sorted(candidate for candidate in level if valid(candidate))
        if answers:
            return answers
        level = {
            candidate[:index] + candidate[index + 1 :]
            for candidate in level
            for index, character in enumerate(candidate)
            if character in "()"
        }
    return [""]
```

BFS stops at the first depth containing a valid string, so all results use the
minimum number of removals.

## Expert solution: remove exactly the unavoidable counts

```python
def remove_invalid_parentheses(text: str) -> list[str]:
    if not text or any(
        character not in "()" and not "a" <= character <= "z" for character in text
    ):
        raise ValueError("text must contain lowercase letters and parentheses")

    remove_left = 0
    remove_right = 0
    for character in text:
        if character == "(":
            remove_left += 1
        elif character == ")":
            if remove_left:
                remove_left -= 1
            else:
                remove_right += 1

    answers: set[str] = set()
    built: list[str] = []

    def search(index: int, balance: int, left: int, right: int) -> None:
        if index == len(text):
            if balance == 0 and left == 0 and right == 0:
                answers.add("".join(built))
            return
        character = text[index]
        if character == "(":
            if left:
                search(index + 1, balance, left - 1, right)
            built.append(character)
            search(index + 1, balance + 1, left, right)
            built.pop()
        elif character == ")":
            if right:
                search(index + 1, balance, left, right - 1)
            if balance:
                built.append(character)
                search(index + 1, balance - 1, left, right)
                built.pop()
        else:
            built.append(character)
            search(index + 1, balance, left, right)
            built.pop()

    search(0, 0, remove_left, remove_right)
    return sorted(answers)
```

The initial scan proves that `remove_left + remove_right` removals are necessary
and sufficient. DFS removes exactly those counts and never creates a negative
balance, so every leaf is valid and minimal; the set removes duplicate texts.

**Complexity:** Exponential worst-case search time and `O(n)` recursion space,
excluding the output.
