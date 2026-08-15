# Focus300 230: LeetCode 134 - Gas Station

**Source:** [LeetCode 134](https://leetcode.com/problems/gas-station/)  
**Difficulty:** Medium  
**Pattern:** greedy feasibility scan

## Exact contract

Find a starting station from which a full circuit is possible, or report that no such start exists.

## First principles

If the total gas is less than the total cost, no start can work. Otherwise, any segment that drives the running balance negative cannot contain a valid start inside it.

## Cases that decide correctness

- A globally negative total balance means impossible.
- The valid start may be near the end of the array.
- A station can be skipped entirely if the running balance already failed before it.
- Exactly one feasible start is enough.

## Brute force

```python
def can_complete_circuit_brute(gas, cost):
    n = len(gas)
    for start in range(n):
        fuel = 0
        ok = True
        for step in range(n):
            i = (start + step) % n
            fuel += gas[i] - cost[i]
            if fuel < 0:
                ok = False
                break
        if ok:
            return start
    return -1
```

Try each station as a start and simulate the full loop.

## Better insight

Track the running surplus and reset the candidate start whenever the surplus drops below zero.

## Expert solution

```python
def can_complete_circuit(gas, cost):
    total = tank = start = 0
    for i, (g, c) in enumerate(zip(gas, cost)):
        diff = g - c
        total += diff
        tank += diff
        if tank < 0:
            start = i + 1
            tank = 0
    return start if total >= 0 else -1
```

Make one pass to verify total feasibility and another greedy pass to choose the first station after each deficit run.

**Complexity:** O(n) time and O(1) space.
