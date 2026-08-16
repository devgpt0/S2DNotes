# Focus300 080: LeetCode 552 - Student Attendance Record II

**Source:** [LeetCode 552](https://leetcode.com/problems/student-attendance-record-ii/)  
**Difficulty:** Hard  
**Pattern:** six-state automaton and matrix exponentiation

## Exact contract

Count length-`n` attendance strings over `P`, `A`, and `L` that contain fewer
than two `A` characters total and never contain three consecutive `L`
characters. Return the count modulo `1_000_000_007` for `1 <= n <= 100000`.

## First principles

Future validity depends only on whether an absence has already occurred and the
current trailing-late run length 0, 1, or 2. These six states form a finite
automaton. Appending `P` resets the late run, appending `A` is allowed only from
zero-absence states, and appending `L` increases a run below two.


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

- Two total absences are forbidden even when separated.
- Three consecutive lates are forbidden; two are valid.
- `P` and `A` both reset the trailing-late count.
- Every prefix state counts distinct strings, not just reachability.
- All arithmetic uses modulo `1_000_000_007`.

## Brute force: enumerate every attendance string

```python
from itertools import product


MODULO = 1_000_000_007


def attendance_record_count_brute(length: int) -> int:
    if not 1 <= length <= 100_000:
        raise ValueError("length must be between 1 and 100000")
    return (
        sum(
            record.count("A") < 2 and "LLL" not in record
            for record in map("".join, product("PAL", repeat=length))
        )
        % MODULO
    )
```

This takes `O(3^n * n)` time.

## Better approach: roll the six automaton states

```python
MODULO = 1_000_000_007


def attendance_record_count_dp(length: int) -> int:
    if not 1 <= length <= 100_000:
        raise ValueError("length must be between 1 and 100000")

    states = [[0] * 3 for _ in range(2)]
    states[0][0] = 1
    for _ in range(length):
        next_states = [[0] * 3 for _ in range(2)]
        for absent in range(2):
            for late in range(3):
                count = states[absent][late]
                next_states[absent][0] += count
                if absent == 0:
                    next_states[1][0] += count
                if late < 2:
                    next_states[absent][late + 1] += count
        states = [
            [count % MODULO for count in absent_states] for absent_states in next_states
        ]
    return sum(map(sum, states)) % MODULO
```

This is `O(n)` time and `O(1)` state space.

## Expert solution: exponentiate the six-state transition

```python
MODULO = 1_000_000_007
STATE_COUNT = 6


def attendance_record_count(length: int) -> int:
    if not 1 <= length <= 100_000:
        raise ValueError("length must be between 1 and 100000")

    transition = [[0] * STATE_COUNT for _ in range(STATE_COUNT)]
    for absent in range(2):
        for late in range(3):
            source = absent * 3 + late
            transition[absent * 3][source] += 1
            if absent == 0:
                transition[3][source] += 1
            if late < 2:
                transition[absent * 3 + late + 1][source] += 1

    def multiply(first: list[list[int]], second: list[list[int]]) -> list[list[int]]:
        return [
            [
                sum(
                    first[row][middle] * second[middle][column]
                    for middle in range(STATE_COUNT)
                )
                % MODULO
                for column in range(STATE_COUNT)
            ]
            for row in range(STATE_COUNT)
        ]

    vector = [1, 0, 0, 0, 0, 0]
    power = transition
    exponent = length
    while exponent:
        if exponent & 1:
            vector = [
                sum(
                    power[row][column] * vector[column] for column in range(STATE_COUNT)
                )
                % MODULO
                for row in range(STATE_COUNT)
            ]
        power = multiply(power, power)
        exponent >>= 1
    return sum(vector) % MODULO
```

The matrix contains exactly the valid one-character transitions between the
six sufficient states. Matrix powers compose days, so applying the `n`th power
to the empty-record state counts every valid length-`n` record once.

**Complexity:** `O(log n)` time with constant `6 x 6` matrices and `O(1)`
space.
