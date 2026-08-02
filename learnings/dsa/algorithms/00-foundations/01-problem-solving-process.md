# A Repeatable Problem-Solving Process

## Idea

Competitive programming rewards a reliable process more than flashes of
inspiration.

## Steps

## 1. Translate the statement

Write down:

- the exact output;
- input sizes and value ranges;
- whether order matters;
- whether values can repeat or be negative;
- whether the answer must be exact, modulo a number, or approximate.

Turn the constraints into a time budget:

| Largest `n` | Usually feasible |
| ---: | --- |
| `20` | `O(2^n)` |
| `40` | `O(2^(n/2))` |
| `500` | `O(n^3)` may fit |
| `5,000` | about `O(n^2)` |
| `200,000` | `O(n log n)` or `O(n)` |
| `10^7` | usually `O(n)` with small constants |

These are estimates, not laws. Language, constant factors, and the time limit
matter.

## 2. Build the smallest correct model

Start with a brute-force solution. It exposes what choices exist and gives an
oracle for testing. Then ask which work is repeated.

```text
enumerate everything -> identify repeated work -> store or avoid that work
                                            -> prove nothing was lost
```

Common transformations:

- repeated range sum -> prefix sum;
- repeated membership test -> hash set;
- sorted monotone decision -> binary search;
- overlapping recursive states -> dynamic programming;
- shortest unweighted steps -> BFS;
- repeated minimum extraction -> heap.

## First-principles derivation

Every optimized solution begins with a correct but possibly slow model.

```text
statement -> exact input/output -> brute force
          -> repeated work or useful structure
          -> optimization -> invariant -> tests
```

Optimization is safe only when you can explain why it preserves every valid
answer.

## Classroom board: improve a pair-sum solution

Find how many index pairs in `[1, 5, 3, 3]` sum to `6`.

```text
Brute force checks all 6 pairs:
(1,5) yes  (1,3) no  (1,3) no
(5,3) no   (5,3) no  (3,3) yes
answer = 2

Repeated work: comparing many pairs.
Useful structure: after sorting, a small sum needs a larger left value;
a large sum needs a smaller right value.

sorted: [1, 3, 3, 5]
         L        R  -> 1 + 5 = 6, count 1
            L  R     -> 3 + 3 = 6, count 2
```

The improved method still needs a proof for duplicates and for how pointers
move. The brute result becomes its test oracle.

## Pattern recognition

Use this process on every problem. Constraints choose the possible complexity;
repeated work and structural guarantees point to the algorithm.

## 3. State the invariant before coding

Examples: “the window contains no duplicate,” “all popped heap distances are
final,” or “`dp[i]` is optimal for the first `i` items.” If the invariant is
unclear, the code will usually be unclear too.

## 4. Test deliberately

Use this order:

1. the sample;
2. minimum valid input;
3. all values equal;
4. strictly increasing and decreasing inputs;
5. answer at the first and last position;
6. overflow-sized values;
7. random small cases checked against brute force.

## A tiny brute-force oracle

The example counts pairs whose sum is `target`. This `O(n^2)` code is useful
for validating a faster implementation on small arrays.

### C++

```cpp
long long countPairsBrute(const std::vector<int>& values, int target) {
    long long count = 0;
    for (int left = 0; left < static_cast<int>(values.size()); ++left) {
        for (int right = left + 1; right < static_cast<int>(values.size()); ++right) {
            if (values[left] + values[right] == target) {
                ++count;
            }
        }
    }
    return count;
}
```

### Python

```python
def count_pairs_brute(values: list[int], target: int) -> int:
    count = 0
    for left in range(len(values)):
        for right in range(left + 1, len(values)):
            if values[left] + values[right] == target:
                count += 1
    return count
```

### Java

```java
static long countPairsBrute(int[] values, int target) {
    long count = 0;
    for (int left = 0; left < values.length; left++) {
        for (int right = left + 1; right < values.length; right++) {
            if (values[left] + values[right] == target) {
                count++;
            }
        }
    }
    return count;
}
```

## Mastery test

Before submitting, you should be able to answer: why is it correct, why does
it terminate, what is its worst-case complexity, and which input is most
likely to break it?

## Complexity

Problem analysis should take minutes, but it prevents coding an approach that
cannot fit. Always state the final algorithm's time and auxiliary space.

## Common mistakes

- Coding before translating the constraints.
- Optimizing before a correct brute-force model exists.
- Testing only the sample.
- Naming a pattern without stating its invariant.
