# Focus300 118: LeetCode 793 - Preimage Size of Factorial Zeroes Function

**Source:** [LeetCode 793](https://leetcode.com/problems/preimage-size-of-factorial-zeroes-function/)  
**Difficulty:** Hard  
**Pattern:** lower bounds on a monotone staircase

## Exact contract

Let `f(x)` be the number of trailing zeroes in `x!` for nonnegative integer
`x`. Given `0 <= k <= 1_000_000_000`, return the number of `x` satisfying
`f(x) == k`. For this function the answer is always `5` or `0`.

## First principles

Each factor `5` paired with an abundant factor `2` creates a trailing zero, so
`f(x) = floor(x/5) + floor(x/25) + ...`. This function is monotone. The values
equal to `k` form the half-open interval from the first `x` with `f(x) >= k` to
the first `x` with `f(x) >= k + 1`.


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

- `0!` through `4!` all have zero trailing zeroes, so `k = 0` returns `5`.
- Powers of five make the function jump and can skip a requested value.
- Count every power of five dividing a number, not only its first factor five.
- Binary search must find the first qualifying value, not any qualifying value.
- The search domain includes nonnegative `x`.

## Brute force: evaluate consecutive factorial indices

```python
def factorial_zero_preimage_brute(target: int) -> int:
    if type(target) is not int:
        raise TypeError("target must be an integer")
    if not 0 <= target <= 1_000_000_000:
        raise ValueError("target must be between 0 and 1000000000")

    value = 0
    matches = 0
    while True:
        quotient = value
        zeroes = 0
        while quotient:
            quotient //= 5
            zeroes += quotient
        if zeroes == target:
            matches += 1
        elif zeroes > target:
            return matches
        value += 1
```

The scan takes `O(x log x)` time up to the first index beyond the target
preimage and `O(1)` space.

## Better approach: binary-search one boundary

Find the first `x` with `f(x) >= k`. If `f(x) == k`, monotonicity and the
five-number plateaus imply the answer is `5`; otherwise it is `0`. Searching
both adjacent lower bounds avoids relying on that plateau fact explicitly.

## Expert solution: subtract two monotone lower bounds

```python
def factorial_zero_preimage(target: int) -> int:
    if type(target) is not int:
        raise TypeError("target must be an integer")
    if not 0 <= target <= 1_000_000_000:
        raise ValueError("target must be between 0 and 1000000000")

    def trailing_zeroes(value: int) -> int:
        result = 0
        while value:
            value //= 5
            result += value
        return result

    def first_at_least(required: int) -> int:
        low = 0
        high = 5 * required + 5
        while low < high:
            middle = (low + high) // 2
            if trailing_zeroes(middle) >= required:
                high = middle
            else:
                low = middle + 1
        return low

    return first_at_least(target + 1) - first_at_least(target)
```

The two lower bounds delimit exactly the integer plateau where `f(x) == k`.
Their difference is its size, including zero when a jump skips `k`.

**Complexity:** `O(log^2(k + 2))` time and `O(1)` space.
