def dynamic_connectivity_rebuild_dsu(
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

    active = {edge(first, second) for first, second in initial_edges}
    if len(active) != len(initial_edges):
        raise ValueError("initial edges must be unique")

    def component_count() -> int:
        parent = list(range(vertex_count))
        size = [1] * vertex_count

        def find(vertex: int) -> int:
            while parent[vertex] != vertex:
                parent[vertex] = parent[parent[vertex]]
                vertex = parent[vertex]
            return vertex

        components = vertex_count
        for first, second in active:
            first_root = find(first)
            second_root = find(second)
            if first_root == second_root:
                continue
            if size[first_root] < size[second_root]:
                first_root, second_root = second_root, first_root
            parent[second_root] = first_root
            size[first_root] += size[second_root]
            components -= 1
        return components

    answers = [component_count()]
    for operation_type, first, second in operations:
        normalized = edge(first, second)
        if operation_type == 1:
            if normalized in active:
                raise ValueError("cannot add an active edge")
            active.add(normalized)
        elif operation_type == 2:
            if normalized not in active:
                raise ValueError("cannot remove an inactive edge")
            active.remove(normalized)
        else:
            raise ValueError(f"unknown operation type: {operation_type}")
        answers.append(component_count())
    return answers
