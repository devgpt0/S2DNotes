# ICPC300 028: CSES - Task Assignment

**Source:** [CSES - Task Assignment](https://cses.fi/problemset/task/2129/)  
**Pattern:** minimum-cost perfect bipartite matching (Hungarian algorithm)

## Exact contract

Input gives `n` (`1 <= n <= 200`) and an `n x n` cost matrix. Entry `cost[i][j]`
is the cost of assigning employee `i` to task `j`. Assign every employee one
different task and minimize the total cost.

Output the minimum total cost, followed by `n` lines `a b` describing that
employee `a` receives task `b`. Employee and task numbers are one-based.

## First principles

An assignment is a permutation: no two employees may use the same task. The
Hungarian algorithm maintains dual prices `u` for employees and `v` for tasks.
Reduced cost `cost[i][j] - u[i] - v[j]` stays nonnegative. Each iteration finds
a zero-reduced-cost augmenting path that extends the matching by one employee,
while the smallest slack update creates the next needed zero edge.

## Cases that decide correctness

- The output needs the actual employee-task pairs, not only their cost.
- Equal costs may produce several valid optimal assignments.
- A greedy cheapest task per employee fails because an early employee can take
  the only cheap option of a later employee.
- Total cost can exceed 32-bit range.

## Brute force: try every task permutation

```python
from itertools import permutations


def assignment_brute(costs: list[list[int]]) -> tuple[int, tuple[int, ...]]:
    task_orders = permutations(range(len(costs)))
    return min(
        (sum(costs[employee][task] for employee, task in enumerate(order)), order)
        for order in task_orders
    )
```

**Complexity:** `O(n! n)` time and `O(n)` space.

## Better: bitmask dynamic programming

```python
def assignment_bitmask_dp(costs: list[list[int]]) -> int:
    size = len(costs)
    infinity = 10**30
    best = [infinity] * (1 << size)
    best[0] = 0

    for used_tasks in range(1 << size):
        employee = used_tasks.bit_count()
        if employee == size:
            continue
        for task in range(size):
            if used_tasks & (1 << task) == 0:
                next_mask = used_tasks | (1 << task)
                candidate = best[used_tasks] + costs[employee][task]
                if candidate < best[next_mask]:
                    best[next_mask] = candidate

    return best[-1]
```

The mask records exactly which tasks are occupied; its bit count selects the
next employee. This is practical near `n <= 20`, not `n = 200`.

**Complexity:** `O(n 2^n)` time and `O(2^n)` space.

## Expert solution: Hungarian algorithm

```python
import sys


def minimum_assignment(costs: list[list[int]]) -> tuple[int, list[int]]:
    size = len(costs)
    employee_potential = [0] * (size + 1)
    task_potential = [0] * (size + 1)
    matched_employee = [0] * (size + 1)
    previous_task = [0] * (size + 1)
    infinity = 10**30

    for employee in range(1, size + 1):
        matched_employee[0] = employee
        minimum_slack = [infinity] * (size + 1)
        used = [False] * (size + 1)
        task = 0

        while True:
            used[task] = True
            current_employee = matched_employee[task]
            delta = infinity
            next_task = 0

            for candidate_task in range(1, size + 1):
                if used[candidate_task]:
                    continue
                reduced_cost = (
                    costs[current_employee - 1][candidate_task - 1]
                    - employee_potential[current_employee]
                    - task_potential[candidate_task]
                )
                if reduced_cost < minimum_slack[candidate_task]:
                    minimum_slack[candidate_task] = reduced_cost
                    previous_task[candidate_task] = task
                if minimum_slack[candidate_task] < delta:
                    delta = minimum_slack[candidate_task]
                    next_task = candidate_task

            for candidate_task in range(size + 1):
                if used[candidate_task]:
                    employee_potential[matched_employee[candidate_task]] += delta
                    task_potential[candidate_task] -= delta
                else:
                    minimum_slack[candidate_task] -= delta

            task = next_task
            if matched_employee[task] == 0:
                break

        while task != 0:
            prior = previous_task[task]
            matched_employee[task] = matched_employee[prior]
            task = prior

    assigned_task = [0] * size
    for task in range(1, size + 1):
        assigned_task[matched_employee[task] - 1] = task - 1
    total_cost = sum(
        costs[employee][task] for employee, task in enumerate(assigned_task)
    )
    return total_cost, assigned_task


def solve() -> None:
    data = list(map(int, sys.stdin.buffer.read().split()))
    size = data[0]
    costs = [data[1 + row * size : 1 + (row + 1) * size] for row in range(size)]
    total_cost, assigned_task = minimum_assignment(costs)
    output = [str(total_cost)]
    output.extend(
        f"{employee + 1} {task + 1}" for employee, task in enumerate(assigned_task)
    )
    print("\n".join(output))


if __name__ == "__main__":
    solve()
```

The dual update preserves nonnegative reduced costs and makes at least one new
edge tight. Augmenting through `previous_task` increases matching size by one;
after `n` iterations the matching is perfect and complementary slackness makes
it optimal.

**Complexity:** `O(n^3)` time and `O(n)` auxiliary space beyond the matrix.

