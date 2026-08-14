# ICPC300 011: CSES - Giant Pizza

**Source:** [CSES - Giant Pizza](https://cses.fi/problemset/task/1684/)  
**Pattern:** 2-SAT with strongly connected components  
**Goal:** Choose `+` or `-` for every topping so that each customer's two-option
request contains at least one chosen literal, or report that this is impossible.

## 1. Problem in plain words

A literal `+ x` means topping `x` must be included for that option to be true.
A literal `- x` means it must be excluded. Each customer supplies two literals
joined by **or**.

For requests `(+1 or +2)`, `(-1 or +2)`, and `(-2 or +1)`, choosing `+1 +2`
satisfies everyone. The source accepts any valid assignment.

The code below represents a literal as `(topping_index, wanted_value)`, using
zero-based indices and `True` for `+`.

## 2. First principles

A clause `(a or b)` is false only when both literals are false. Therefore:

- if `a` is false, `b` must be true: `not a -> b`;
- if `b` is false, `a` must be true: `not b -> a`.

These implications form a directed graph. A literal and its negation cannot
belong to the same strongly connected component (SCC): each would force the
other, making both truth values mandatory.

If no variable has that contradiction, the SCC condensation is a DAG. Choosing
components in reverse implication order gives a satisfying assignment.

## 3. Cases that decide correctness

| Case | Required result |
| --- | --- |
| One clause `(+1 or +1)` | Topping `1` must be `+`. |
| `(+1 or +1)` and `(-1 or -1)` | Impossible. |
| A variable never mentioned | Either sign is valid. |
| Repeated or mirrored clauses | They do not change satisfiability. |
| More than one valid assignment | Return any one of them. |

## 4. Brute force: try every assignment

For a tiny number of toppings, enumerate all `2^n` sign choices and test every
clause directly. This is a useful correctness oracle.

```python
Literal = tuple[int, bool]
Clause = tuple[Literal, Literal]


def choose_toppings_brute_force(
    topping_count: int, clauses: list[Clause]
) -> list[str] | None:
    for mask in range(1 << topping_count):
        valid = True
        for (first, first_wanted), (second, second_wanted) in clauses:
            first_value = bool(mask & (1 << first)) == first_wanted
            second_value = bool(mask & (1 << second)) == second_wanted
            if not first_value and not second_value:
                valid = False
                break

        if valid:
            return [
                "+" if mask & (1 << topping) else "-"
                for topping in range(topping_count)
            ]

    return None
```

**Why it works:** every possible assignment appears once, and the direct test
is exactly the source's definition of a satisfied customer.

**Complexity:** `O(2^n (n + m))` time and `O(n)` output space.

## 5. Better for small instances: stop on a false clause

Backtracking can reject a partial assignment as soon as both literals of one
clause are known to be false. This often explores much less than `2^n`, but an
adversarial formula still makes it exponential, so it is not the contest
solution.

```python
Literal = tuple[int, bool]
Clause = tuple[Literal, Literal]


def choose_toppings_backtracking(
    topping_count: int, clauses: list[Clause]
) -> list[str] | None:
    assignment: list[bool | None] = [None] * topping_count

    def literal_value(literal: Literal) -> bool | None:
        topping, wanted = literal
        value = assignment[topping]
        if value is None:
            return None
        return value == wanted

    def has_false_clause() -> bool:
        for first, second in clauses:
            if literal_value(first) is False and literal_value(second) is False:
                return True
        return False

    def search(topping: int) -> bool:
        if has_false_clause():
            return False
        if topping == topping_count:
            return True

        for value in (False, True):
            assignment[topping] = value
            if search(topping + 1):
                return True
        assignment[topping] = None
        return False

    if not search(0):
        return None
    return ["+" if value else "-" for value in assignment]
```

**Complexity:** `O(2^n m)` worst-case time and `O(n)` recursion space.

## 6. Expert solution: implication graph plus Kosaraju

Give each topping two graph vertices. Vertex `2*x` means `+x`, vertex
`2*x + 1` means `-x`, and `literal ^ 1` is its negation.

Kosaraju's algorithm finds SCCs in linear time. With the component numbering
used below, a literal is chosen when its component appears later than the
component of its negation.

```python
Literal = tuple[int, bool]
Clause = tuple[Literal, Literal]


def choose_toppings_2sat(topping_count: int, clauses: list[Clause]) -> list[str] | None:
    vertex_count = 2 * topping_count
    graph: list[list[int]] = [[] for _ in range(vertex_count)]
    reverse_graph: list[list[int]] = [[] for _ in range(vertex_count)]

    def vertex(literal: Literal) -> int:
        topping, wanted = literal
        if not 0 <= topping < topping_count:
            raise ValueError("topping index is outside the assignment")
        return 2 * topping + (0 if wanted else 1)

    def add_implication(source: int, destination: int) -> None:
        graph[source].append(destination)
        reverse_graph[destination].append(source)

    for first, second in clauses:
        first_vertex = vertex(first)
        second_vertex = vertex(second)
        add_implication(first_vertex ^ 1, second_vertex)
        add_implication(second_vertex ^ 1, first_vertex)

    visited = [False] * vertex_count
    finish_order: list[int] = []

    for start in range(vertex_count):
        if visited[start]:
            continue
        visited[start] = True
        stack = [(start, 0)]
        while stack:
            node, edge_index = stack[-1]
            if edge_index == len(graph[node]):
                finish_order.append(node)
                stack.pop()
                continue

            neighbor = graph[node][edge_index]
            stack[-1] = (node, edge_index + 1)
            if not visited[neighbor]:
                visited[neighbor] = True
                stack.append((neighbor, 0))

    component = [-1] * vertex_count
    component_id = 0
    for start in reversed(finish_order):
        if component[start] != -1:
            continue
        component[start] = component_id
        stack = [start]
        while stack:
            node = stack.pop()
            for neighbor in reverse_graph[node]:
                if component[neighbor] == -1:
                    component[neighbor] = component_id
                    stack.append(neighbor)
        component_id += 1

    answer: list[str] = []
    for topping in range(topping_count):
        positive = 2 * topping
        negative = positive + 1
        if component[positive] == component[negative]:
            return None
        answer.append("+" if component[positive] > component[negative] else "-")

    return answer
```

### Why the expert code is correct

- Every clause contributes exactly its two logically equivalent implications.
- Vertices in one SCC force one another. A variable and its negation in one SCC
  are therefore an exact certificate of impossibility.
- Otherwise, SCCs form a DAG. The later component of each opposite pair can be
  made true without requiring an already-false later component.
- Thus every implication, and consequently every original clause, is true.

**Complexity:** `O(n + m)` time and `O(n + m)` memory.

## 7. What to remember

For every clause `(a or b)`, write `not a -> b` and `not b -> a`. Then test
whether any literal shares an SCC with its negation.
