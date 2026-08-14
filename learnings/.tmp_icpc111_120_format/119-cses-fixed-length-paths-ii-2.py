import sys


def fixed_length_paths_tree_dp(
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

    sys.setrecursionlimit(max(1_000, 2 * vertex_count + 10))
    limit = min(maximum_distance, vertex_count - 1)
    visited = [False] * vertex_count
    answer = 0

    def visit(node: int, parent: int) -> list[int]:
        nonlocal answer
        if visited[node]:
            raise ValueError("edges must form an acyclic tree")
        visited[node] = True
        counts = [1]
        for neighbor in graph[node]:
            if neighbor == parent:
                continue
            child_counts = visit(neighbor, node)
            prefix = [0]
            for count in child_counts:
                prefix.append(prefix[-1] + count)
            for first_depth, first_count in enumerate(counts):
                low = max(0, minimum_distance - first_depth - 1)
                high = min(
                    len(child_counts) - 1,
                    limit - first_depth - 1,
                )
                if low <= high:
                    answer += first_count * (prefix[high + 1] - prefix[low])
            needed = min(limit + 1, len(child_counts) + 1)
            if len(counts) < needed:
                counts.extend([0] * (needed - len(counts)))
            for depth, count in enumerate(child_counts):
                if depth + 1 > limit:
                    break
                counts[depth + 1] += count
        return counts

    visit(0, -1)
    if not all(visited):
        raise ValueError("edges must form a connected tree")
    return answer
