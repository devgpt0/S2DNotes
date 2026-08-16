# Focus300 294: LeetCode 299 - Bulls and Cows

**Source:** [LeetCode 299](https://leetcode.com/problems/bulls-and-cows/)  
**Difficulty:** Easy  
**Pattern:** frequency accounting

## Exact contract

Return the number of bulls and cows for the secret and guess strings.

## First principles

A bull is a position match; a cow is a value match in the wrong position. Counting exact matches first and then balancing the leftover frequencies prevents double counting.


## Classroom board: see the repeated work once

```text
brute force tries every choice.
the optimized solution keeps only the state that must survive to the
next step.
```



## Step-by-step transformation

1. Compress the input into counts, prefixes, bit masks, or another compact state.
2. Update that state once per element instead of recomputing earlier work.
3. Combine the stored pieces to recover the value the problem asks for.
4. Return the final count, sum, or constructed answer.

These notes transform input into output by reducing the data to a compact invariant first, then rebuilding the answer from that invariant.


## Diagram: compress the input first

```text

            raw values
                |
                v
            counts / prefix / bit state
                |
                v
            combine stored facts
                |
                v
            final answer
```

The algorithm first compresses the input into a small invariant, then rebuilds the answer from that compact state.

## Cases that decide correctness

- A character can contribute to at most one cow after bull removal.
- Repeated digits or letters need frequency balancing.
- Positions that already match are bulls, not cows.
- The output format must separate bulls and cows clearly.

## Brute force

```python
from collections import Counter

def get_hint_brute(secret, guess):
    bulls = sum(a == b for a, b in zip(secret, guess))
    s = Counter(secret)
    g = Counter(guess)
    cows = sum(min(s[d], g[d]) for d in s) - bulls
    return f"{bulls}A{cows}B"
```

Compare every unmatched position against every other position.

## Better insight

Track exact matches and leftover frequency differences in one pass.

## Expert solution

```python
from collections import Counter

def get_hint(secret, guess):
    bulls = sum(a == b for a, b in zip(secret, guess))
    s = Counter(secret)
    g = Counter(guess)
    cows = sum(min(s[d], g[d]) for d in s) - bulls
    return f"{bulls}A{cows}B"
```

Count bulls directly, then use a frequency balance to compute cows from the unmatched characters.

**Complexity:** O(n) time and O(1) space for fixed-size alphabets.
