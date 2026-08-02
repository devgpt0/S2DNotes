# Backtracking

## Idea

Backtracking builds one partial answer, tries a choice, recurses, then undoes
the choice. It explores only valid branches.

## Visual model

```text
choose -> explore -> undo -> try next choice
```

## Classroom board: permutations of `[A,B]`

```text
position 0 choose A -> position 1 choose B -> save [A,B]
undo B, undo A
position 0 choose B -> position 1 choose A -> save [B,A]
undo A, undo B
```

Undoing restores the exact board before the next branch.

## Steps

1. Define what the partial state means.
2. If it is complete, save the answer.
3. Try each legal next choice.
4. Apply the choice, recurse, and undo it exactly.

## First-principles derivation

A solution is a sequence of choices. Explore one choice, update the partial
state, recurse, and undo exactly that change before trying the next choice.

The state must represent only the current path; pruning is safe only when no
completion of that path can be valid.

## Pattern recognition

Use it to enumerate permutations, combinations, placements, paths, or
constraint-satisfaction answers when input is small and invalid branches can
be rejected early.

## Implementation: all permutations

### C++

```cpp
void buildPermutations(std::vector<int>& values, int position, std::vector<std::vector<int>>& answer) {
    if (position == static_cast<int>(values.size())) {
        answer.push_back(values);
        return;
    }
    for (int choice = position; choice < static_cast<int>(values.size()); ++choice) {
        std::swap(values[position], values[choice]);
        buildPermutations(values, position + 1, answer);
        std::swap(values[position], values[choice]);
    }
}
```

### Python

```python
def permutations(values: list[int]) -> list[list[int]]:
    answer: list[list[int]] = []

    def build(position: int) -> None:
        if position == len(values):
            answer.append(values.copy())
            return
        for choice in range(position, len(values)):
            values[position], values[choice] = values[choice], values[position]
            build(position + 1)
            values[position], values[choice] = values[choice], values[position]

    build(0)
    return answer
```

### Java

```java
static void buildPermutations(int[] values, int position, List<int[]> answer) {
    if (position == values.length) {
        answer.add(values.clone());
        return;
    }
    for (int choice = position; choice < values.length; choice++) {
        swap(values, position, choice);
        buildPermutations(values, position + 1, answer);
        swap(values, position, choice);
    }
}
```

## Why it works

At each position, the loop tries every remaining value exactly once. Undoing
restores the identical state needed for the next choice.

## Complexity

There are `n!` outputs and copying each costs `O(n)`, so time is `O(n * n!)`.
The recursion uses `O(n)` space excluding output.

## Common mistakes

- Forgetting to undo shared state.
- Saving the same mutable list instead of a copy.
- Generating duplicates when input values repeat; sort and skip equal choices
  at the same depth.
