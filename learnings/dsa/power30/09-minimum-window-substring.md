# Problem 9: Minimum Window Substring (LeetCode #76)

**Difficulty:** Hard · **Pattern:** Sliding window

## Problem Statement

Return the shortest substring of `s` containing every character of `t`, including duplicates; return `""` when none exists.

## Example

`s = "ADOBECODEBANC"`, `t = "ABC"` → `"BANC"`.

## Constraints

`1 <= s.length, t.length <= 10^5`; strings use English letters.

## Observation

Expand until the window covers `t`, then shrink only while it remains valid.

## Learning diagram

```text
expand until valid -> shrink while valid -> record shortest -> repeat
```

## Algorithm for the optimal approach

Count required occurrences, expand until covered, then shrink without losing coverage.

## Pattern to remember

> Shortest valid substring -> expand, then shrink.

## Solution 1: Brute Force

### Observation

Enumerate windows and count their characters. Time: `O(n^2)` or worse. Space: `O(alphabet)`.

### Algorithm

1. Choose every possible left boundary.
2. Expand the right boundary one character at a time.
3. Count the characters in the current substring.
4. When it covers `t`, record its length and stop expanding that start.
5. Return the shortest recorded window.

### C++ code

```cpp
class Solution {
   private:
    bool covers(const array<int, 128>& have, const array<int, 128>& need) {
        for (int character = 0; character < 128; ++character) {
            if (have[character] < need[character]) {
                return false;
            }
        }
        return true;
    }

   public:
    string minWindow(string source, string target) {
        array<int, 128> need{};
        for (char character : target) {
            ++need[static_cast<unsigned char>(character)];
        }

        int bestStart = 0;
        int bestLength = INT_MAX;

        for (int left = 0; left < static_cast<int>(source.size()); ++left) {
            array<int, 128> have{};

            for (int right = left; right < static_cast<int>(source.size());
                 ++right) {
                ++have[static_cast<unsigned char>(source[right])];

                if (covers(have, need)) {
                    if (right - left + 1 < bestLength) {
                        bestStart = left;
                        bestLength = right - left + 1;
                    }
                    break;
                }
            }
        }

        return bestLength == INT_MAX ? ""
                                     : source.substr(bestStart, bestLength);
    }
};
```

### Complexity

- Time: `O(n^2 * alphabet size)`
- Space: `O(alphabet size)`

## How we derive the optimal solution

```text
Start a new search from every left boundary
                |
                v
Coverage changes by only one character when a boundary moves
                |
                v
Reuse counts in one sliding window
                |
                v
Expand until valid, then shrink while valid
                |
                v
O(|s| + |t|) time with a fixed-size counter
```

## Solution 2: Optimized (Hash Map Window)

Track formed requirement types against required types. Time: `O(n)`. Space: `O(alphabet)`.

### C++

```cpp
string minWindowMap(string s, string t) {
    unordered_map<char, int> need, have;
    for (char c : t) ++need[c];
    int formed = 0, left = 0, start = 0, len = INT_MAX;
    for (int right = 0; right < (int)s.size(); ++right) {
        if (++have[s[right]] == need[s[right]]) ++formed;
        while (formed == (int)need.size()) {
            if (right - left + 1 < len) start = left, len = right - left + 1;
            if (have[s[left]]-- == need[s[left++]]) --formed;
        }
    }
    return len == INT_MAX ? "" : s.substr(start, len);
}
```

### Python

```python
def min_window_map(s: str, t: str) -> str:
    need = Counter(t)
    have: dict[str, int] = {}
    formed = left = start = 0
    length = float("inf")
    for right, char in enumerate(s):
        have[char] = have.get(char, 0) + 1
        formed += have[char] == need[char]
        while formed == len(need):
            if right - left + 1 < length:
                left, start, length = left, left, right - left + 1
            char = s[left]
            formed -= have[char] == need[char]
            have[char] -= 1
            left += 1
    return "" if length == float("inf") else s[start : start + length]
```

### Java

```java
String minWindowMap(String s, String t) {
    Map<Character, Integer> need = new HashMap<>(), have = new HashMap<>();
    for (char c : t.toCharArray()) need.merge(c, 1, Integer::sum);
    int formed = 0, left = 0, start = 0, length = Integer.MAX_VALUE;
    for (int right = 0; right < s.length(); right++) {
        char c = s.charAt(right);
        have.merge(c, 1, Integer::sum);
        if (have.get(c).equals(need.get(c)))
            formed++;
        while (formed == need.size()) {
            if (right - left + 1 < length) {
                start = left;
                length = right - left + 1;
            }
            c = s.charAt(left++);
            if (have.get(c).equals(need.get(c)))
                formed--;
            have.put(c, have.get(c) - 1);
        }
    }
    return length == Integer.MAX_VALUE ? "" : s.substring(start, start + length);
}
```

### Go

```go
func minWindowMap(s, t string) string {
	need, have := map[byte]int{}, map[byte]int{}
	for i := range t {
		need[t[i]]++
	}
	formed, left, start, length := 0, 0, 0, len(s)+1
	for right := range s {
		c := s[right]
		have[c]++
		if have[c] == need[c] {
			formed++
		}
		for formed == len(need) {
			if right-left+1 < length {
				start, length = left, right-left+1
			}
			c = s[left]
			if have[c] == need[c] {
				formed--
			}
			have[c]--
			left++
		}
	}
	if length == len(s)+1 {
		return ""
	}
	return s[start : start+length]
}
```

## Approach 3 — Competitive Programming (Fixed Frequency Array)

For ASCII input, use a fixed counter and one `missing` count. Time: `O(n)`. Space: `O(1)`.

### C++

```cpp
string minWindow(string s, string t) {
    vector<int> need(128);
    for (char c : t) ++need[c];
    int left = 0, start = 0, missing = t.size(), length = INT_MAX;
    for (int right = 0; right < (int)s.size(); ++right) {
        if (need[s[right]]-- > 0) --missing;
        while (!missing) {
            if (right - left + 1 < length)
                start = left, length = right - left + 1;
            if (++need[s[left++]] > 0) ++missing;
        }
    }
    return length == INT_MAX ? "" : s.substr(start, length);
}
```

### Python

```python
def min_window(s: str, t: str) -> str:
    need = [0] * 128
    for char in t:
        need[ord(char)] += 1
    left = start = 0
    missing = len(t)
    length = float("inf")
    for right, char in enumerate(s):
        need[ord(char)] -= 1
        missing -= need[ord(char)] >= 0
        while missing == 0:
            if right - left + 1 < length:
                start, length = left, right - left + 1
            need[ord(s[left])] += 1
            missing += need[ord(s[left])] > 0
            left += 1
    return "" if length == float("inf") else s[start : start + length]
```

### Java

```java
String minWindow(String s, String t) {
    int[] need = new int[128];
    for (char c : t.toCharArray()) need[c]++;
    int left = 0, start = 0, missing = t.length(), length = Integer.MAX_VALUE;
    for (int right = 0; right < s.length(); right++) {
        if (need[s.charAt(right)]-- > 0)
            missing--;
        while (missing == 0) {
            if (right - left + 1 < length) {
                start = left;
                length = right - left + 1;
            }
            if (++need[s.charAt(left++)] > 0)
                missing++;
        }
    }
    return length == Integer.MAX_VALUE ? "" : s.substring(start, start + length);
}
```

### Go

```go
func minWindow(s, t string) string {
	need := [128]int{}
	for i := range t {
		need[t[i]]++
	}
	left, start, missing, length := 0, 0, len(t), len(s)+1
	for right := range s {
		if need[s[right]] > 0 {
			missing--
		}
		need[s[right]]--
		for missing == 0 {
			if right-left+1 < length {
				start, length = left, right-left+1
			}
			need[s[left]]++
			if need[s[left]] > 0 {
				missing++
			}
			left++
		}
	}
	if length == len(s)+1 {
		return ""
	}
	return s[start : start+length]
}
```

## Comparison

| Approach | Time | Space |
| --- | --- | --- |
| Brute force | `O(n^2)`+ | `O(alphabet)` |
| Hash map window | `O(n)` | `O(alphabet)` |
| Fixed counter | `O(n)` | `O(1)` |
