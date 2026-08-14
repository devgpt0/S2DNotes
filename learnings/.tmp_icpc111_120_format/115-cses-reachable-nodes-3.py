from collections import deque


def reachable_nodes_bitsets(
    vertex_count: int, edges: list[tuple[int, int]]
) -> list[int]:
    if vertex_count <= 0:
        raise ValueError("vertex_count must be positive")

    graph = [[] for _ in range(vertex_count)]
    indegree = [0] * vertex_count
    for first, second in edges:
        graph[first].append(second)
        indegree[second] += 1

    queue = deque(vertex for vertex in range(vertex_count) if indegree[vertex] == 0)
    order: list[int] = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor in graph[node]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)
    if len(order) != vertex_count:
        raise ValueError("graph must be acyclic")

    reachable = [1 << vertex for vertex in range(vertex_count)]
    for node in reversed(order):
        for neighbor in graph[node]:
            reachable[node] |= reachable[neighbor]
    return [vertices.bit_count() for vertices in reachable]
