# ICPC300 156: Codeforces 264C - Choosing Balls

**Source:** [Codeforces 264C - Choosing Balls](https://codeforces.com/problemset/problem/264/C)  
**Rating:** 2300  
**Pattern:** subsequence DP with the best two color states  
**Goal:** For each coefficient pair `(same, different)`, choose a subsequence
of balls with maximum score. A chosen ball contributes `same * beauty` when
its color equals the previous chosen color and `different * beauty` otherwise.
The first chosen ball uses `different`, and choosing nothing scores zero.

## 1. First principles

The future only needs the previous chosen color and the best score ending in
that color. For a ball of color `color`, there are three useful choices:

```text
start here:             different * beauty
continue same color:    best[color] + same * beauty
change from a color x:  best[x] + different * beauty, where x != color
```

Only the largest state whose color differs from `color` is needed. Keeping the
largest two color states makes that choice constant time.

## 2. Cases that decide correctness

- The empty subsequence keeps every answer at least zero.
- The first chosen ball uses the `different` coefficient.
- Skipped balls do not change the previous chosen color.
- Negative coefficients can make a negative intermediate same-color state
  useful later, so every color state must be retained.
- Equal beauties are separate balls and remain in their original order.

## 3. Brute force: enumerate every subsequence

```python
def choosing_balls_brute(
    beauties: list[int],
    colors: list[int],
    queries: list[tuple[int, int]],
) -> list[int]:
    if not beauties or len(beauties) != len(colors):
        raise ValueError("beauties and colors must have equal positive length")
    if any(beauty <= 0 for beauty in beauties):
        raise ValueError("beauties must be positive")
    if any(color <= 0 for color in colors):
        raise ValueError("colors must be positive")

    answers: list[int] = []
    for same, different in queries:
        answer = 0
        for chosen in range(1 << len(beauties)):
            score = 0
            previous_color: int | None = None
            for index, (beauty, color) in enumerate(zip(beauties, colors)):
                if chosen >> index & 1 == 0:
                    continue
                coefficient = same if previous_color == color else different
                score += coefficient * beauty
                previous_color = color
            answer = max(answer, score)
        answers.append(answer)
    return answers
```

**Complexity:** `O(q n 2^n)` time and `O(q)` output space.

## 4. Better: try every previous chosen ball

```python
def choosing_balls_quadratic(
    beauties: list[int],
    colors: list[int],
    queries: list[tuple[int, int]],
) -> list[int]:
    if not beauties or len(beauties) != len(colors):
        raise ValueError("beauties and colors must have equal positive length")
    if any(beauty <= 0 for beauty in beauties):
        raise ValueError("beauties must be positive")
    if any(color <= 0 for color in colors):
        raise ValueError("colors must be positive")

    answers: list[int] = []
    for same, different in queries:
        ending = [0] * len(beauties)
        answer = 0
        for index, beauty in enumerate(beauties):
            ending[index] = different * beauty
            for previous in range(index):
                coefficient = same if colors[previous] == colors[index] else different
                ending[index] = max(
                    ending[index],
                    ending[previous] + coefficient * beauty,
                )
            answer = max(answer, ending[index])
        answers.append(answer)
    return answers
```

**Complexity:** `O(q n^2)` time and `O(n+q)` space.

## 5. Expert solution: best two distinct colors

```python
def choosing_balls_best_two(
    beauties: list[int],
    colors: list[int],
    queries: list[tuple[int, int]],
) -> list[int]:
    if not beauties or len(beauties) != len(colors):
        raise ValueError("beauties and colors must have equal positive length")
    if any(beauty <= 0 for beauty in beauties):
        raise ValueError("beauties must be positive")
    if any(color <= 0 for color in colors):
        raise ValueError("colors must be positive")

    negative_infinity = -(10**30)
    answers: list[int] = []
    for same, different in queries:
        best_by_color: dict[int, int] = {}
        first_score = 0
        first_color: int | None = None
        second_score = negative_infinity

        for beauty, color in zip(beauties, colors):
            old_score = best_by_color.get(color, negative_infinity)
            different_base = first_score if first_color != color else second_score
            new_score = max(
                old_score,
                different * beauty,
                different_base + different * beauty,
            )
            if old_score != negative_infinity:
                new_score = max(new_score, old_score + same * beauty)
            best_by_color[color] = new_score

            if first_color == color:
                first_score = new_score
            elif new_score > first_score:
                second_score = first_score
                first_score = new_score
                first_color = color
            elif new_score > second_score:
                second_score = new_score

        answers.append(first_score)
    return answers
```

### Why the expert code is correct

`best_by_color[color]` stores exactly the best processed subsequence ending in
that color, including negative states. A transition from another color needs
only the largest state not labeled `color`; that is the global best unless its
label is `color`, in which case it is the second best. The empty state of score
zero is also a valid different-color base. Thus every legal last-step choice is
considered, and no illegal same-color transition uses the wrong coefficient.

**Complexity:** `O(qn)` time and `O(n+q)` space.

## 6. What to remember

```text
subsequence future -> only its last color matters
change color -> best state excluding one color
exclude one maximum -> keep the best two labeled states
```
