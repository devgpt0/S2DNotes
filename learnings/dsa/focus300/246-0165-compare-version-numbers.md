# Focus300 246: LeetCode 165 - Compare Version Numbers

**Source:** [LeetCode 165](https://leetcode.com/problems/compare-version-numbers/)  
**Difficulty:** Easy  
**Pattern:** segment-wise numeric comparison

## Exact contract

Compare two dotted version strings and return whether the first is less than, equal to, or greater than the second.

## First principles

Each dot-separated segment is a base-10 integer with leading zeroes ignored. The comparison is lexicographic by numeric segments, not by raw text length.


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

- Trailing zero segments do not change the version.
- Segments of different lengths compare by numeric value.
- Leading zeroes must be ignored.
- Missing segments behave like zero.

## Brute force

```python
def compare_version_brute(version1, version2):
    a = [int(x) for x in version1.split(".")]
    b = [int(x) for x in version2.split(".")]
    n = max(len(a), len(b))
    a += [0] * (n - len(a))
    b += [0] * (n - len(b))
    return (a > b) - (a < b)
```

Convert the whole string to a single number, which fails on multi-segment versions.

## Better insight

Split on dots and compare integer segments one by one.

## Expert solution

```python
def compare_version(version1, version2):
    parts1 = list(map(int, version1.split(".")))
    parts2 = list(map(int, version2.split(".")))
    n = max(len(parts1), len(parts2))
    parts1 += [0] * (n - len(parts1))
    parts2 += [0] * (n - len(parts2))
    return (parts1 > parts2) - (parts1 < parts2)
```

Walk both version strings in parallel, parse each segment numerically, and compare the first unequal pair.

**Complexity:** O(n) time and O(1) extra space beyond the parsed segments.
