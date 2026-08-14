def reachable_nodes_brute(vertex_count: int, edges: list[tuple[int, int]]) -> list[int]:
    if vertex_count <= 0:
        raise ValueError("vertex_count must be positive")

    graph = [[] for _ in range(vertex_count)]
    for first, second in edges:
        graph[first].append(second)

    answers: list[int] = []
    for start in range(vertex_count):
        seen = {start}
        stack = [start]
        while stack:
            node = stack.pop()
            for neighbor in graph[node]:
                if neighbor not in seen:
                    seen.add(neighbor)
                    stack.append(neighbor)
        answers.append(len(seen))
    return answers
