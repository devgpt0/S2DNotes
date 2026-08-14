def dynamic_connectivity_brute(
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
        graph = [[] for _ in range(vertex_count)]
        for first, second in active:
            graph[first].append(second)
            graph[second].append(first)
        seen = [False] * vertex_count
        components = 0
        for start in range(vertex_count):
            if seen[start]:
                continue
            components += 1
            seen[start] = True
            stack = [start]
            while stack:
                node = stack.pop()
                for neighbor in graph[node]:
                    if not seen[neighbor]:
                        seen[neighbor] = True
                        stack.append(neighbor)
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
