from collections import deque


def fixed_length_paths_brute(
    vertex_count: int,
    edges: list[tuple[int, int]],
    minimum_distance: int,
    maximum_distance: int,
) -> int:
    if vertex_count <= 0:
        raise ValueError("vertex_count must be positive")
    if not 0 <= minimum_distance <= maximum_distance:
        raise ValueError("invalid distance interval")
    if len(edges) != vertex_count - 1:
        raise ValueError("a tree must have vertex_count - 1 edges")
    graph = [[] for _ in range(vertex_count)]
    for first, second in edges:
        if not 0 <= first < vertex_count or not 0 <= second < vertex_count:
            raise ValueError("edge endpoint out of range")
        graph[first].append(second)
        graph[second].append(first)

    answer = 0
    for start in range(vertex_count):
        distance = [-1] * vertex_count
        distance[start] = 0
        queue = deque([start])
        while queue:
            node = queue.popleft()
            for neighbor in graph[node]:
                if distance[neighbor] == -1:
                    distance[neighbor] = distance[node] + 1
                    queue.append(neighbor)
        if any(value == -1 for value in distance):
            raise ValueError("edges must form a connected tree")
        answer += sum(
            minimum_distance <= distance[end] <= maximum_distance
            for end in range(start + 1, vertex_count)
        )
    return answer
