def dynamic_connectivity_rollback(
    vertex_count: int,
    initial_edges: list[tuple[int, int]],
    operations: list[tuple[int, int, int]],
) -> list[int]:
    if vertex_count <= 0:
        raise ValueError("vertex_count must be positive")

    def edge(first: int, second: int) -> tuple[int, int]:
        if first == second:
            raise ValueError("self-loops are not supported")
        return (first, second) if first < second else (second, first)

    active_since = {edge(first, second): 0 for first, second in initial_edges}
    if len(active_since) != len(initial_edges):
        raise ValueError("initial edges must be unique")

    state_count = len(operations) + 1
    intervals: list[tuple[int, int, tuple[int, int]]] = []
    for time, (operation_type, first, second) in enumerate(operations, start=1):
        normalized = edge(first, second)
        if operation_type == 1:
            if normalized in active_since:
                raise ValueError("cannot add an active edge")
            active_since[normalized] = time
        elif operation_type == 2:
            start = active_since.pop(normalized, None)
            if start is None:
                raise ValueError("cannot remove an inactive edge")
            intervals.append((start, time - 1, normalized))
        else:
            raise ValueError(f"unknown operation type: {operation_type}")
    for normalized, start in active_since.items():
        intervals.append((start, state_count - 1, normalized))

    timeline: list[list[tuple[int, int]]] = [[] for _ in range(4 * state_count)]

    def add_interval(
        node: int,
        low: int,
        high: int,
        left: int,
        right: int,
        normalized: tuple[int, int],
    ) -> None:
        if left <= low and high <= right:
            timeline[node].append(normalized)
            return
        middle = (low + high) // 2
        if left <= middle:
            add_interval(2 * node, low, middle, left, right, normalized)
        if right > middle:
            add_interval(2 * node + 1, middle + 1, high, left, right, normalized)

    for left, right, normalized in intervals:
        if left <= right:
            add_interval(1, 0, state_count - 1, left, right, normalized)

    parent = list(range(vertex_count))
    size = [1] * vertex_count
    history: list[tuple[int, int]] = []
    components = vertex_count

    def find(vertex: int) -> int:
        while parent[vertex] != vertex:
            vertex = parent[vertex]
        return vertex

    def unite(first: int, second: int) -> None:
        nonlocal components
        first_root = find(first)
        second_root = find(second)
        if first_root == second_root:
            return
        if size[first_root] < size[second_root]:
            first_root, second_root = second_root, first_root
        history.append((second_root, size[first_root]))
        parent[second_root] = first_root
        size[first_root] += size[second_root]
        components -= 1

    def rollback(snapshot: int) -> None:
        nonlocal components
        while len(history) > snapshot:
            child, old_parent_size = history.pop()
            root = parent[child]
            size[root] = old_parent_size
            parent[child] = child
            components += 1

    answers = [0] * state_count

    def solve(node: int, low: int, high: int) -> None:
        snapshot = len(history)
        for first, second in timeline[node]:
            unite(first, second)
        if low == high:
            answers[low] = components
        else:
            middle = (low + high) // 2
            solve(2 * node, low, middle)
            solve(2 * node + 1, middle + 1, high)
        rollback(snapshot)

    solve(1, 0, state_count - 1)
    return answers
