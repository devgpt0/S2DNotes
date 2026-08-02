# Correctness, Invariants, and Proofs

## Idea

An accepted-looking algorithm is not enough; you need a short reason it
cannot miss an answer.

## Steps: loop-invariant proof

Use three parts:

1. **Initialization:** the invariant is true before the first iteration.
2. **Maintenance:** one iteration preserves it.
3. **Termination:** when the loop ends, the invariant implies the result.

For binary search below, the invariant is: if `target` exists, its first
position is in the half-open interval `[left, right)`.

```text
[ definitely too small |       unknown       | definitely large enough ]
                        left                 right
```

### C++

```cpp
int lowerBound(const std::vector<int>& values, int target) {
    int left = 0;
    int right = static_cast<int>(values.size());
    while (left < right) {
        const int middle = left + (right - left) / 2;
        if (values[middle] < target) {
            left = middle + 1;
        } else {
            right = middle;
        }
    }
    return left;
}
```

### Python

```python
def lower_bound(values: list[int], target: int) -> int:
    left, right = 0, len(values)
    while left < right:
        middle = left + (right - left) // 2
        if values[middle] < target:
            left = middle + 1
        else:
            right = middle
    return left
```

### Java

```java
static int lowerBound(int[] values, int target) {
    int left = 0;
    int right = values.length;
    while (left < right) {
        int middle = left + (right - left) / 2;
        if (values[middle] < target) {
            left = middle + 1;
        } else {
            right = middle;
        }
    }
    return left;
}
```

## Other proof patterns

- **Induction:** ideal for recursion, trees, and DP.
- **Exchange argument:** replace part of an optimal answer with the greedy
  choice without making it worse.
- **Cut property:** used in minimum spanning trees.
- **Contradiction:** assume the algorithm's answer is not optimal and derive an
  impossibility.
- **Bijection/counting:** show every valid object is generated exactly once.

## First-principles derivation

An algorithm is correct when it never discards a possible answer and its final
state implies the required result.

```text
before loop: invariant is true
one step:    invariant remains true
after loop:  invariant gives the answer
```

The invariant is the bridge between individual code steps and the final claim.

## Classroom board: prove lower bound

Find the first value at least `3` in `[1, 3, 3, 7]`.

```text
invariant: the answer stays inside [left, right)

left right middle value action
0    4     2      3     right = 2
0    2     1      3     right = 1
0    1     0      1     left = 1

stop: [1,1) is empty, so the boundary is index 1
```

Every discarded left part is strictly smaller than `3`; every discarded right
part begins with a value that could still be the answer.

## Pattern recognition

Use invariants for loops and data structures, induction for DP/recursion,
exchange for greedy choices, and cut arguments for spanning trees.

## Termination matters

Every recursive call must move toward a base case. Every loop must shrink a
finite search space or advance a bounded variable. Most binary-search bugs are
termination bugs caused by mixing interval conventions.

## Mastery test

Give a three-sentence proof for your solution before coding. If you cannot,
look for a counterexample rather than adding conditions randomly.

## Complexity

A proof does not change runtime. It must include a separate argument that the
algorithm terminates and that its time and memory fit the constraints.

## Common mistakes

- Proving only the happy path.
- Assuming the result instead of proving a discarded choice is safe.
- Mixing interval conventions halfway through an invariant.
- Omitting termination or base cases.
