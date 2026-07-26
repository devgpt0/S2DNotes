# Problem 25: Combination Sum (LeetCode #39)

**Difficulty:** Medium  
**Core pattern:** Choose/explore/unchoose backtracking

## Problem statement

Return every unique combination whose sum is `target`. Each distinct candidate
may be selected any number of times.

## Example

```text
candidates = [2, 3, 6, 7], target = 7

2 + 2 + 3 = 7
7         = 7

answer = [[2,2,3], [7]]
```

## Observation

Generate combinations in non-decreasing index order. Then `[2, 3, 2]` is never
generated separately from `[2, 2, 3]`, so no deduplication set is needed.

```text
remain = 7
choose 2 -> remain 5 -> choose 2 -> remain 3 -> choose 3 -> 0 [2,2,3]
         -> remain 5 -> choose 3 -> remain 2 (stop when values are too large)
choose 3 -> remain 4 -> choose 3 -> remain 1 (stop)
choose 7 -> remain 0 [7]
```

## Solution 1: Generate Ordered Sequences and Deduplicate

### Observation

Trying every candidate at every level creates different orders of the same
combination and wastes exponential work.

### Algorithm

1. Try every candidate at every recursive level.
2. Stop when the remaining target is negative.
3. When remaining becomes zero, sort the path and add it to a set.
4. The set removes different orders of the same combination.

### C++ code

```cpp
class Solution {
   private:
    void search(const vector<int>& candidates, int remaining, vector<int>& path,
                set<vector<int>>& uniqueCombinations) {
        if (remaining < 0) {
            return;
        }
        if (remaining == 0) {
            vector<int> combination = path;
            sort(combination.begin(), combination.end());
            uniqueCombinations.insert(combination);
            return;
        }

        for (int value : candidates) {
            path.push_back(value);
            search(candidates, remaining - value, path, uniqueCombinations);
            path.pop_back();
        }
    }

   public:
    vector<vector<int>> combinationSum(vector<int>& candidates, int target) {
        vector<int> path;
        set<vector<int>> uniqueCombinations;
        search(candidates, target, path, uniqueCombinations);
        return {uniqueCombinations.begin(), uniqueCombinations.end()};
    }
};
```

### Complexity

- Time: exponential, with heavy duplicate work
- Space: recursion plus the deduplication set

## How we derive the optimal solution

```text
Try candidates in every order
          |
          v
[2,2,3], [2,3,2], and [3,2,2] are the same combination
          |
          v
Force paths to use non-decreasing candidate indices
          |
          v
Each combination is generated exactly once
          |
          v
Sort candidates and prune values larger than remaining
```

## Optimized / CP approach

### Algorithm

1. Sort candidates so branches can be pruned.
2. Pass a `start` index and remaining target to DFS.
3. If remaining is `0`, copy the path into the answer.
4. Try candidates from `start` onward.
5. Stop when a candidate is larger than remaining.
6. Recurse with the same index because reuse is allowed.
7. Remove the chosen value when returning.

### Complexity

- Time: exponential and output-dependent
- Space: `O(target / minimum candidate)` recursion depth, excluding output

## Pattern to remember

```text
all combinations + choices can repeat
        => backtracking
recurse with same index   = reuse allowed
recurse with index + 1    = use once
```

## C++

```cpp
class Solution {
   public:
    vector<vector<int>> combinationSum(vector<int>& candidates, int target) {
        sort(candidates.begin(), candidates.end());
        vector<vector<int>> answer;
        vector<int> path;

        function<void(int, int)> search = [&](int start, int remaining) {
            if (remaining == 0) {
                answer.push_back(path);
                return;
            }
            for (int index = start; index < (int)candidates.size(); ++index) {
                int value = candidates[index];
                if (value > remaining) {
                    break;
                }
                path.push_back(value);
                search(index, remaining - value);
                path.pop_back();
            }
        };

        search(0, target);
        return answer;
    }
};
```

## Python

```python
class Solution:
    def combination_sum(
        self,
        candidates: list[int],
        target: int,
    ) -> list[list[int]]:
        candidates.sort()
        answer: list[list[int]] = []
        path: list[int] = []

        def search(start: int, remaining: int) -> None:
            if remaining == 0:
                answer.append(path.copy())
                return

            for index in range(start, len(candidates)):
                value = candidates[index]
                if value > remaining:
                    break
                path.append(value)
                search(index, remaining - value)
                path.pop()

        search(0, target)
        return answer
```

## Java

```java
class Solution {
    public List<List<Integer>> combinationSum(int[] candidates, int target) {
        Arrays.sort(candidates);
        List<List<Integer>> answer = new ArrayList<>();
        search(candidates, target, 0, new ArrayList<>(), answer);
        return answer;
    }

    private void search(int[] candidates, int remaining, int start, List<Integer> path,
        List<List<Integer>> answer) {
        if (remaining == 0) {
            answer.add(new ArrayList<>(path));
            return;
        }

        for (int index = start; index < candidates.length; index++) {
            int value = candidates[index];
            if (value > remaining) {
                break;
            }
            path.add(value);
            search(candidates, remaining - value, index, path, answer);
            path.remove(path.size() - 1);
        }
    }
}
```

## Go

```go
func combinationSum(candidates []int, target int) [][]int {
	sort.Ints(candidates)
	answer := [][]int{}
	path := []int{}

	var search func(int, int)
	search = func(start, remaining int) {
		if remaining == 0 {
			answer = append(answer, append([]int(nil), path...))
			return
		}

		for index := start; index < len(candidates); index++ {
			value := candidates[index]
			if value > remaining {
				break
			}
			path = append(path, value)
			search(index, remaining-value)
			path = path[:len(path)-1]
		}
	}

	search(0, target)
	return answer
}
```

## Common mistakes

- Recursing with `index + 1`, which incorrectly forbids reuse.
- Adding the mutable path without copying it.
- Restarting every recursive loop at `0`, which creates permutations.
