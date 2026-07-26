# Problem 8: Longest Substring Without Repeating Characters (LeetCode #3)

**Difficulty:** Medium · **Pattern:** Sliding window

## Problem Statement

Return the length of the longest substring containing no repeated character.

## Example

`"abcabcbb"` → `3` from `"abc"`.

## Constraints

`0 <= s.length <= 5 * 10^4`; `s` may contain letters, digits, symbols, and spaces.

## Observation

The active window is valid precisely when each character occurs once.

## Learning diagram

```text
expand right -> duplicate? -> jump left past last occurrence -> update best
```

## Algorithm for the optimal approach

Store last-seen indices and keep the active window duplicate-free.

## Pattern to remember

> Longest valid substring -> sliding window.

## Solution 1: Brute Force

### Observation

Check every substring for duplicate characters. Time: `O(n^3)`. Space: `O(min(n, alphabet))`.

### Algorithm

1. Choose every index as a substring start.
2. Extend to the right while storing characters in a set.
3. Stop when a repeated character appears.
4. Update the best length after every unique extension.

### C++ code

```cpp
class Solution {
   public:
    int lengthOfLongestSubstring(string text) {
        int best = 0;

        for (int start = 0; start < static_cast<int>(text.size()); ++start) {
            unordered_set<char> used;

            for (int end = start; end < static_cast<int>(text.size()); ++end) {
                if (used.contains(text[end])) {
                    break;
                }

                used.insert(text[end]);
                best = max(best, end - start + 1);
            }
        }

        return best;
    }
};
```

### Complexity

- Time: `O(n^2)` expected
- Space: `O(min(n, alphabet size))`

## How we derive the optimal solution

```text
Restart a uniqueness set at every index
             |
             v
Most neighboring substrings share almost all characters
             |
             v
Keep one moving window and remove characters from the left
             |
             v
Set-based window: O(n) time
             |
             v
Store last-seen indices to jump the left boundary directly
```

## Solution 2: Optimized (Set Window)

Expand right and repeatedly remove from left until the new character is unique. Time: `O(n)`. Space: `O(min(n, alphabet))`.

### C++

```cpp
int lengthSet(string s) {
    unordered_set<char> seen;
    int left = 0, best = 0;
    for (int right = 0; right < (int)s.size(); ++right) {
        while (seen.count(s[right])) seen.erase(s[left++]);
        seen.insert(s[right]);
        best = max(best, right - left + 1);
    }
    return best;
}
```

### Python

```python
def length_set(s: str) -> int:
    seen: set[str] = set()
    left = best = 0
    for right, char in enumerate(s):
        while char in seen:
            seen.remove(s[left])
            left += 1
        seen.add(char)
        best = max(best, right - left + 1)
    return best
```

### Java

```java
int lengthSet(String s) {
    Set<Character> seen = new HashSet<>();
    int left = 0, best = 0;
    for (int right = 0; right < s.length(); right++) {
        while (seen.contains(s.charAt(right))) seen.remove(s.charAt(left++));
        seen.add(s.charAt(right));
        best = Math.max(best, right - left + 1);
    }
    return best;
}
```

### Go

```go
func lengthSet(s string) int {
	chars := []rune(s)
	seen := map[rune]bool{}
	left, best := 0, 0
	for right, char := range chars {
		for seen[char] {
			delete(seen, chars[left])
			left++
		}
		seen[char] = true
		best = max(best, right-left+1)
	}
	return best
}
```

## Approach 3 — Competitive Programming (Last Seen Index)

Jump the left boundary past a duplicate's previous index. Time: `O(n)`. Space: `O(min(n, alphabet))`.

### C++

```cpp
int lengthOfLongestSubstring(string s) {
    vector<int> last(256, -1);
    int left = 0, best = 0;
    for (int right = 0; right < (int)s.size(); ++right) {
        left = max(left, last[(unsigned char)s[right]] + 1);
        last[(unsigned char)s[right]] = right;
        best = max(best, right - left + 1);
    }
    return best;
}
```

### Python

```python
def length_of_longest_substring(s: str) -> int:
    last: dict[str, int] = {}
    left = best = 0
    for right, char in enumerate(s):
        left = max(left, last.get(char, -1) + 1)
        last[char] = right
        best = max(best, right - left + 1)
    return best
```

### Java

```java
int lengthOfLongestSubstring(String s) {
    int[] last = new int[128];
    Arrays.fill(last, -1);
    int left = 0, best = 0;
    for (int right = 0; right < s.length(); right++) {
        char c = s.charAt(right);
        left = Math.max(left, last[c] + 1);
        last[c] = right;
        best = Math.max(best, right - left + 1);
    }
    return best;
}
```

### Go

```go
func lengthOfLongestSubstring(s string) int {
	last := map[rune]int{}
	chars := []rune(s)
	left, best := 0, 0
	for right, char := range chars {
		if index, ok := last[char]; ok {
			left = max(left, index+1)
		}
		last[char] = right
		best = max(best, right-left+1)
	}
	return best
}
```

## Comparison

| Approach | Time | Space |
| --- | --- | --- |
| Brute force | `O(n^3)` | `O(n)` |
| Set window | `O(n)` | `O(n)` |
| Last-seen window | `O(n)` | `O(n)` |
