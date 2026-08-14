# ICPC300 236: Codeforces 1290C - Prefix Enlightenment

**Source:** [Codeforces 1290C - Prefix Enlightenment](https://codeforces.com/problemset/problem/1290/C)  
**Difficulty:** 2400  
**Pattern:** weighted parity DSU under prefix constraints

## Exact contract

Each switch toggles a listed set of bulbs; every bulb belongs to one or two
switches. Process bulbs from left to right. After each prefix, return the
minimum number of switches that must be on so every bulb in that prefix ends in
state `1`, or `-1` if the constraints conflict.

## First principles

Switch states are binary variables. Bulb `i` requires the XOR of its controlling
switches to equal `1 ^ initial[i]`. A parity DSU stores equations
`x[u] ^ x[v] = required`.

For each component, maintain the number of on switches when its root is assigned
zero or one. An equation may merge components; a one-switch bulb fixes one root
assignment. The global answer is the sum of each component's cheaper allowed
cost.

## Cases that decide correctness

- One-controller bulbs anchor a component to one assignment.
- Two anchors can make a later prefix impossible.
- DSU parity is variable XOR component root.
- Merging with reversed union-by-size orientation keeps the same XOR relation.
- Components not touched by constraints optimally choose all switches off.

## Brute force: enumerate switch masks for every prefix

```python
def prefix_enlightenment_brute(
    initial: str, switch_positions: list[list[int]]
) -> list[int]:
    if not initial or any(character not in "01" for character in initial):
        raise ValueError("initial must be a nonempty binary string")
    controllers = [[] for _ in initial]
    for switch, positions in enumerate(switch_positions):
        if len(set(positions)) != len(positions):
            raise ValueError("a switch cannot list one bulb twice")
        for position in positions:
            if type(position) is not int or not 0 <= position < len(initial):
                raise ValueError("invalid bulb position")
            controllers[position].append(switch)
    if any(not 1 <= len(items) <= 2 for items in controllers):
        raise ValueError("every bulb needs one or two controllers")

    answers: list[int] = []
    for prefix in range(1, len(initial) + 1):
        best: int | None = None
        for mask in range(1 << len(switch_positions)):
            valid = True
            for position in range(prefix):
                state = int(initial[position])
                for switch in controllers[position]:
                    state ^= mask >> switch & 1
                if state != 1:
                    valid = False
                    break
            if valid:
                cost = mask.bit_count()
                best = cost if best is None else min(best, cost)
        answers.append(-1 if best is None else best)
    return answers
```

This takes `O(nk2^k)` time.

## Better approach: rebuild parity components per prefix

Solving all XOR equations from scratch after every new bulb is polynomial but
repeats the unchanged prefix. The weighted DSU incorporates one equation at a
time.

## Expert solution: online weighted parity DSU

```python
def prefix_enlightenment(initial: str, switch_positions: list[list[int]]) -> list[int]:
    if not initial or any(character not in "01" for character in initial):
        raise ValueError("initial must be a nonempty binary string")
    controllers = [[] for _ in initial]
    for switch, positions in enumerate(switch_positions):
        if len(set(positions)) != len(positions):
            raise ValueError("a switch cannot list one bulb twice")
        for position in positions:
            if type(position) is not int or not 0 <= position < len(initial):
                raise ValueError("invalid bulb position")
            controllers[position].append(switch)
    if any(not 1 <= len(items) <= 2 for items in controllers):
        raise ValueError("every bulb needs one or two controllers")

    switch_count = len(switch_positions)
    parent = list(range(switch_count))
    component_size = [1] * switch_count
    parity = [0] * switch_count
    cost_zero = [0] * switch_count
    cost_one = [1] * switch_count
    fixed = [-1] * switch_count

    def find(vertex: int) -> tuple[int, int]:
        if parent[vertex] == vertex:
            return vertex, 0
        root, above = find(parent[vertex])
        parity[vertex] ^= above
        parent[vertex] = root
        return root, parity[vertex]

    def component_cost(root: int) -> int:
        if fixed[root] == 0:
            return cost_zero[root]
        if fixed[root] == 1:
            return cost_one[root]
        return min(cost_zero[root], cost_one[root])

    total = 0
    possible = True

    def fix_variable(vertex: int, value: int) -> None:
        nonlocal total, possible
        root, vertex_parity = find(vertex)
        root_value = value ^ vertex_parity
        if fixed[root] != -1 and fixed[root] != root_value:
            possible = False
            return
        total -= component_cost(root)
        fixed[root] = root_value
        total += component_cost(root)

    def join(first: int, second: int, required: int) -> None:
        nonlocal total, possible
        first_root, first_parity = find(first)
        second_root, second_parity = find(second)
        if first_root == second_root:
            if first_parity ^ second_parity != required:
                possible = False
            return

        relation = required ^ first_parity ^ second_parity
        if component_size[first_root] < component_size[second_root]:
            first_root, second_root = second_root, first_root
        total -= component_cost(first_root) + component_cost(second_root)
        parent[second_root] = first_root
        parity[second_root] = relation
        component_size[first_root] += component_size[second_root]

        second_zero = cost_zero[second_root]
        second_one = cost_one[second_root]
        if relation:
            second_zero, second_one = second_one, second_zero
        cost_zero[first_root] += second_zero
        cost_one[first_root] += second_one

        second_fixed = fixed[second_root]
        if second_fixed != -1:
            translated = second_fixed ^ relation
            if fixed[first_root] != -1 and fixed[first_root] != translated:
                possible = False
            else:
                fixed[first_root] = translated
        total += component_cost(first_root)

    answers: list[int] = []
    for position, character in enumerate(initial):
        required = 1 ^ int(character)
        if possible:
            if len(controllers[position]) == 1:
                fix_variable(controllers[position][0], required)
            else:
                join(controllers[position][0], controllers[position][1], required)
        answers.append(total if possible else -1)
    return answers
```

Parity links preserve every processed XOR equation. The two component costs
enumerate its only possible root assignments, while anchors remove one choice;
summing independent component minima is globally optimal.

**Complexity:** `O((n+k) alpha(k))` time and `O(k+n)` space.
