# Tree Dynamic Programming

## Idea

Tree DP computes a state from child subtrees. Root the tree so every edge has
a parent-to-child direction.

## Visual model

For maximum-weight independent set:

```text
take vertex    -> cannot take children
skip vertex    -> independently take or skip each child
```

## Classroom board: take or skip a parent

```text
parent weight 5, child weight 4
take parent -> child must be skipped: total 5
skip parent -> child may be taken: total 4

with many children, add each child's compatible best state
```

## Steps

1. Choose any root and pass the parent in DFS.
2. Define `skip[v]` and `take[v]` for the subtree of `v`.
3. Combine every child once.
4. Return `max(skip[root], take[root])`.

## First-principles derivation

Root the tree so every problem splits into independent child subtrees. Define
what the answer means for one subtree and combine already solved children.

The parent-child state carries exactly the information needed across the cut
between a subtree and the rest of the tree.

## Classroom board: maximum-weight independent set

No adjacent selected vertices; weights are shown inside nodes.

```text
       0(4)
      /    \
   1(2)   2(3)
           |
          3(5)

dp[v][1] = choose v
dp[v][0] = skip v

leaf 1: choose=2, skip=0
leaf 3: choose=5, skip=0
node 2: choose=3+skip(3)=3
        skip=max(5,0)=5
root 0: choose=4+skip(1)+skip(2)=9
        skip=max(2,0)+max(3,5)=7
answer = 9
```

Choosing vertex `0` forces both children to be skipped but still permits
grandchild `3`.

## Pattern recognition

Use tree DP when choices in one subtree interact with the rest only through
the connecting parent edge.

## Implementation: maximum-weight independent set

### C++

```cpp
std::pair<long long, long long> independentSetDfs(
    const std::vector<std::vector<int>>& tree,
    const std::vector<int>& weight,
    int vertex,
    int parent) {
    long long skip = 0;
    long long take = weight[vertex];
    for (int child : tree[vertex]) {
        if (child == parent) continue;
        auto [childSkip, childTake] = independentSetDfs(tree, weight, child, vertex);
        skip += std::max(childSkip, childTake);
        take += childSkip;
    }
    return {skip, take};
}
```

### Python

```python
def independent_set_dfs(
    tree: list[list[int]], weight: list[int], vertex: int, parent: int
) -> tuple[int, int]:
    skip = 0
    take = weight[vertex]
    for child in tree[vertex]:
        if child == parent:
            continue
        child_skip, child_take = independent_set_dfs(tree, weight, child, vertex)
        skip += max(child_skip, child_take)
        take += child_skip
    return skip, take
```

### Java

```java
static long[] independentSetDfs(List<List<Integer>> tree, int[] weight, int vertex, int parent) {
    long skip = 0;
    long take = weight[vertex];
    for (int child : tree.get(vertex)) {
        if (child == parent) continue;
        long[] childState = independentSetDfs(tree, weight, child, vertex);
        skip += Math.max(childState[0], childState[1]);
        take += childState[0];
    }
    return new long[] {skip, take};
}
```

## Why it works

Once the choice at `v` is fixed, child subtrees are independent. The two states
enumerate both legal choices at every vertex and keep only the best total.

## Complexity

Time is `O(V)` and recursion space is `O(height)`.

## Common mistakes

- Walking back to the parent forever.
- Using one state when the parent needs to know whether the child was chosen.
- Combining children before their states are complete.
