# Focus300 101: LeetCode 726 - Number of Atoms

**Source:** [LeetCode 726](https://leetcode.com/problems/number-of-atoms/)  
**Difficulty:** Hard  
**Pattern:** nested parsing with scoped frequency maps

## Exact contract

Given a valid chemical `formula`, return every atom in lexicographic order,
followed by its total count when that count exceeds one. An atom begins with an
uppercase letter and may continue with lowercase letters. A number applies to
the atom or parenthesized group immediately before it.

## First principles

Parentheses delay multiplication: the suffix after `)` cannot be applied until
the whole group is known. A stack isolates each open group. Closing a group
scales its atom counts once and merges them into the surrounding group.


## Classroom board: see the repeated work once

```text
brute force tries every choice.
the optimized solution keeps only the state that must survive to the
next step.
```



## Step-by-step transformation

1. Read the input and identify the smallest state that still determines the answer.
2. Process one element, node, or row at a time while preserving that state.
3. Discard work that can no longer change the result.
4. Convert the surviving state into the output the problem requests.

The examples and code below show this transformation on the specific problem instance.


## Diagram: input to output

```text

        input
            |
            v
        core invariant
            |
            v
        process one step at a time
            |
            v
        output
```

The note shows the main idea, the repeated work, and the small state that turns the input into the output.

## Cases that decide correctness

- A missing suffix means a multiplier of one.
- Atom names such as `Mg` are one token, not two atoms.
- Groups may be nested, and a multiplier applies to every atom in that group.
- The final string omits count `1` and sorts by atom name.
- Source input is a non-empty, syntactically valid formula.

## Brute force: materialize every atom occurrence

```python
from collections import Counter


def count_atoms_brute(formula: str) -> str:
    if not formula:
        raise ValueError("formula must be non-empty")

    index = 0

    def parse_number() -> int:
        nonlocal index
        start = index
        while index < len(formula) and formula[index].isdigit():
            index += 1
        return int(formula[start:index]) if start < index else 1

    def expand_group() -> list[str]:
        nonlocal index
        atoms: list[str] = []
        while index < len(formula) and formula[index] != ")":
            if formula[index] == "(":
                index += 1
                nested = expand_group()
                if index >= len(formula) or formula[index] != ")":
                    raise ValueError("unclosed parenthesis")
                index += 1
                atoms.extend(nested * parse_number())
                continue
            if not formula[index].isupper():
                raise ValueError("expected an atom or opening parenthesis")
            start = index
            index += 1
            while index < len(formula) and formula[index].islower():
                index += 1
            atoms.extend([formula[start:index]] * parse_number())
        return atoms

    expanded = expand_group()
    if index != len(formula):
        raise ValueError("unmatched closing parenthesis")
    counts = Counter(expanded)
    return "".join(
        atom + (str(count) if count > 1 else "")
        for atom, count in sorted(counts.items())
    )
```

This is correct but takes `O(E)` space and time before sorting, where `E` is
the fully expanded number of atom occurrences.

## Better transition: aggregate before expanding

A recursive parser can return one count map per group. A stack performs the
same delayed merge without recursion and never constructs repeated atom tokens.

## Expert solution: stack of count maps

```python
from collections import Counter


def count_of_atoms(formula: str) -> str:
    if not formula:
        raise ValueError("formula must be non-empty")

    scopes: list[Counter[str]] = [Counter()]
    index = 0

    def parse_number(start: int) -> tuple[int, int]:
        stop = start
        while stop < len(formula) and formula[stop].isdigit():
            stop += 1
        return (int(formula[start:stop]) if start < stop else 1, stop)

    while index < len(formula):
        character = formula[index]
        if character == "(":
            scopes.append(Counter())
            index += 1
        elif character == ")":
            if len(scopes) == 1:
                raise ValueError("unmatched closing parenthesis")
            group = scopes.pop()
            multiplier, index = parse_number(index + 1)
            for atom, count in group.items():
                scopes[-1][atom] += count * multiplier
        elif character.isupper():
            stop = index + 1
            while stop < len(formula) and formula[stop].islower():
                stop += 1
            atom = formula[index:stop]
            multiplier, index = parse_number(stop)
            scopes[-1][atom] += multiplier
        else:
            raise ValueError("expected an atom or parenthesis")

    if len(scopes) != 1:
        raise ValueError("unclosed parenthesis")
    return "".join(
        atom + (str(count) if count > 1 else "")
        for atom, count in sorted(scopes[0].items())
    )
```

Each token is consumed once. Every group is scaled exactly when its closing
parenthesis is read, so the root map contains the complete counts.

**Complexity:** `O(n + a log a)` time and `O(n + a)` space, where `a` is the
number of distinct atoms and the stack depth is at most `n`.
