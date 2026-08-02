# 2-SAT

## Idea

2-SAT asks whether boolean variables can satisfy clauses with two literals,
such as `(x is true OR y is false)`.

A clause `(a OR b)` is equivalent to two implications:

```text
NOT a -> b
NOT b -> a
```

## Classroom board: turn OR into consequences

```text
clause (x OR y)
if x is false, y must be true: NOT x -> y
if y is false, x must be true: NOT y -> x

if x and NOT x end in one SCC, each forces the other -> impossible
```

## Steps

1. Create two graph nodes per variable: false and true.
2. Add both implications for every clause.
3. Find strongly connected components (SCCs).
4. If a variable and its negation share an SCC, no assignment exists.
5. Otherwise assign values using reverse SCC order.

## First-principles derivation

A clause `(a OR b)` fails only when both literals are false. Therefore if
`a` is false, `b` must be true, and if `b` is false, `a` must be true.

```text
(a OR b) -> (NOT a -> b) and (NOT b -> a)
```

A formula is impossible exactly when a variable and its negation imply each
other and therefore belong to the same SCC.

## Classroom board: turn clauses into implications

Formula: `(x OR y) AND (NOT x OR y) AND (x OR NOT y)`.

```text
x OR y:       NOT x -> y, NOT y -> x
NOT x OR y:   x -> y,     NOT y -> NOT x
x OR NOT y:   NOT x -> NOT y, y -> x

x and y imply each other, so choose both true.
check clauses:
(T OR T) AND (F OR T) AND (T OR F) = true
```

If `x` and `NOT x` were in one SCC, choosing either truth value would force
its opposite.

## Pattern recognition

Use 2-SAT when every constraint can be written as a two-literal OR, including
“at least one,” “not both,” implication, and equality/inequality constraints.

## Implementation

The code uses `stronglyConnectedComponents` from the
[SCC note](12-strongly-connected-components.md). Node `2*v` means false and
`2*v+1` means true.

### C++

```cpp
class TwoSat {
   public:
    explicit TwoSat(int variables) : graph_(2 * variables) {}

    void addClause(int firstVariable, bool firstValue, int secondVariable, bool secondValue) {
        int first = 2 * firstVariable + firstValue;
        int second = 2 * secondVariable + secondValue;
        graph_[first ^ 1].push_back(second);
        graph_[second ^ 1].push_back(first);
    }

    std::optional<std::vector<bool>> solve() const {
        std::vector<int> component = stronglyConnectedComponents(graph_);
        std::vector<bool> answer(graph_.size() / 2);
        for (int variable = 0; variable < static_cast<int>(answer.size()); ++variable) {
            if (component[2 * variable] == component[2 * variable + 1]) return std::nullopt;
            answer[variable] = component[2 * variable] < component[2 * variable + 1];
        }
        return answer;
    }

   private:
    std::vector<std::vector<int>> graph_;
};
```

### Python

```python
class TwoSat:
    def __init__(self, variables: int) -> None:
        self.graph = [[] for _ in range(2 * variables)]

    def add_clause(
        self,
        first_variable: int,
        first_value: bool,
        second_variable: int,
        second_value: bool,
    ) -> None:
        first = 2 * first_variable + first_value
        second = 2 * second_variable + second_value
        self.graph[first ^ 1].append(second)
        self.graph[second ^ 1].append(first)

    def solve(self) -> list[bool] | None:
        component = strongly_connected_components(self.graph)
        answer = [False] * (len(self.graph) // 2)
        for variable in range(len(answer)):
            false_node = 2 * variable
            true_node = false_node + 1
            if component[false_node] == component[true_node]:
                return None
            answer[variable] = component[false_node] < component[true_node]
        return answer
```

### Java

```java
final class TwoSat {
    private final List<List<Integer>> graph;

    TwoSat(int variables) {
        graph = new ArrayList<>();
        for (int node = 0; node < 2 * variables; node++) graph.add(new ArrayList<>());
    }

    void addClause(int firstVariable, boolean firstValue, int secondVariable, boolean secondValue) {
        int first = 2 * firstVariable + (firstValue ? 1 : 0);
        int second = 2 * secondVariable + (secondValue ? 1 : 0);
        graph.get(first ^ 1).add(second);
        graph.get(second ^ 1).add(first);
    }

    boolean[] solve() {
        int[] component = stronglyConnectedComponents(graph);
        boolean[] answer = new boolean[graph.size() / 2];
        for (int variable = 0; variable < answer.length; variable++) {
            int falseNode = 2 * variable;
            int trueNode = falseNode + 1;
            if (component[falseNode] == component[trueNode]) return null;
            answer[variable] = component[falseNode] < component[trueNode];
        }
        return answer;
    }
}
```

## Why it works

If a literal reaches its negation and the negation reaches it, choosing either
forces a contradiction. Otherwise the acyclic SCC order gives a consistent
truth choice.

## Complexity

Time and space are `O(variables + clauses)`.

## Common mistakes

- Adding only one implication per clause.
- Confusing “not both” with “at least one.”
- Using an assignment comparison that does not match the SCC numbering order.
