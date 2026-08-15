# Focus300 247: LeetCode 166 - Fraction to Recurring Decimal

**Source:** [LeetCode 166](https://leetcode.com/problems/fraction-to-recurring-decimal/)  
**Difficulty:** Medium  
**Pattern:** long division with remainder tracking

## Exact contract

Convert a fraction into its decimal string form and place repeating digits in parentheses.

## First principles

Long division generates one digit per remainder. A repeated remainder means the decimal expansion has entered a cycle, and the cycle start is exactly where that remainder first appeared.

## Cases that decide correctness

- A zero numerator returns `0`.
- A zero denominator is invalid.
- The sign depends on whether numerator and denominator have opposite signs.
- A terminating decimal has no parentheses.

## Brute force

```python
def fraction_to_decimal_brute(numerator, denominator):
    if numerator == 0:
        return "0"
    sign = "-" if (numerator < 0) ^ (denominator < 0) else ""
    numerator, denominator = abs(numerator), abs(denominator)
    integer = numerator // denominator
    remainder = numerator % denominator
    if remainder == 0:
        return sign + str(integer)
    decimals = []
    seen = {}
    while remainder and remainder not in seen:
        seen[remainder] = len(decimals)
        remainder *= 10
        decimals.append(str(remainder // denominator))
        remainder %= denominator
    if remainder in seen:
        i = seen[remainder]
        decimals.insert(i, "(")
        decimals.append(")")
    return sign + str(integer) + "." + "".join(decimals)
```

Perform floating-point division and hope the repeated cycle appears in the printed digits.

## Better insight

Track each remainder's first position in the output string.

## Expert solution

```python
def fraction_to_decimal(numerator, denominator):
    if numerator == 0:
        return "0"
    sign = "-" if (numerator < 0) ^ (denominator < 0) else ""
    numerator, denominator = abs(numerator), abs(denominator)
    integer, remainder = divmod(numerator, denominator)
    if remainder == 0:
        return sign + str(integer)
    seen = {}
    digits = []
    while remainder:
        if remainder in seen:
            i = seen[remainder]
            digits.insert(i, "(")
            digits.append(")")
            break
        seen[remainder] = len(digits)
        remainder *= 10
        digit, remainder = divmod(remainder, denominator)
        digits.append(str(digit))
    return f"{sign}{integer}." + "".join(digits)
```

Generate integer and fractional parts separately, record every seen remainder, and insert parentheses when a remainder repeats.

**Complexity:** O(k) time and space, where `k` is the number of generated decimal digits before termination or repetition.
