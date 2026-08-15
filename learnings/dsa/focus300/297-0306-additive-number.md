# Focus300 297: LeetCode 306 - Additive Number

**Source:** [LeetCode 306](https://leetcode.com/problems/additive-number/)  
**Difficulty:** Medium  
**Pattern:** backtracking over numeric prefixes

## Exact contract

Decide whether the string forms an additive sequence where each number equals the sum of the previous two.

## First principles

The first two numbers determine the entire rest of the sequence. That means the search space is only the choice of the first split points plus a deterministic validation walk.

## Cases that decide correctness

- Leading zeroes are invalid unless the number is exactly zero.
- The sequence needs at least three numbers.
- Very large prefixes may exceed 32-bit limits in some languages.
- Once a prefix mismatch appears, the current split is invalid immediately.

## Brute force

```python
def is_additive_number_brute(num):
    def add(a, b):
        carry = 0
        res = []
        i, j = len(a) - 1, len(b) - 1
        while i >= 0 or j >= 0 or carry:
            s = carry
            if i >= 0:
                s += ord(a[i]) - 48
                i -= 1
            if j >= 0:
                s += ord(b[j]) - 48
                j -= 1
            res.append(str(s % 10))
            carry = s // 10
        return "".join(reversed(res))

    n = len(num)
    for i in range(1, n):
        for j in range(i + 1, n):
            a, b = num[:i], num[i:j]
            if (a.startswith("0") and a != "0") or (b.startswith("0") and b != "0"):
                continue
            k = j
            while k < n:
                c = add(a, b)
                if not num.startswith(c, k):
                    break
                k += len(c)
                a, b = b, c
            if k == n:
                return True
    return False
```

Try every split point and reparse the entire suffix repeatedly.

## Better insight

Fix the first two numbers and then validate the rest greedily.

## Expert solution

```python
def is_additive_number(num):
    def add(a, b):
        carry = 0
        res = []
        i, j = len(a) - 1, len(b) - 1
        while i >= 0 or j >= 0 or carry:
            s = carry
            if i >= 0:
                s += ord(a[i]) - 48
                i -= 1
            if j >= 0:
                s += ord(b[j]) - 48
                j -= 1
            res.append(str(s % 10))
            carry = s // 10
        return "".join(reversed(res))

    n = len(num)
    for i in range(1, n):
        for j in range(i + 1, n):
            a, b = num[:i], num[i:j]
            if (a.startswith("0") and a != "0") or (b.startswith("0") and b != "0"):
                continue
            k = j
            while k < n:
                c = add(a, b)
                if not num.startswith(c, k):
                    break
                k += len(c)
                a, b = b, c
            if k == n:
                return True
    return False
```

Enumerate the initial splits, then walk forward checking that each next chunk equals the sum of the previous two chunks.

**Complexity:** Exponential in the number of initial split choices, with linear validation per candidate.
