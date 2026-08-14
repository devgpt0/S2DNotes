import sys


def fixed_length_paths_centroid(
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

    seen = {0}
    stack = [0]
    while stack:
        node = stack.pop()
        for neighbor in graph[node]:
            if neighbor not in seen:
                seen.add(neighbor)
                stack.append(neighbor)
    if len(seen) != vertex_count:
        raise ValueError("edges must form a connected tree")

    sys.setrecursionlimit(max(1_000, 2 * vertex_count + 10))
    removed = [False] * vertex_count
    subtree_size = [0] * vertex_count
    answer = 0

    def calculate_sizes(node: int, parent: int) -> int:
        subtree_size[node] = 1
        for neighbor in graph[node]:
            if neighbor != parent and not removed[neighbor]:
                subtree_size[node] += calculate_sizes(neighbor, node)
        return subtree_size[node]

    def find_centroid(node: int, parent: int, total: int) -> int:
        for neighbor in graph[node]:
            if (
                neighbor != parent
                and not removed[neighbor]
                and subtree_size[neighbor] > total // 2
            ):
                return find_centroid(neighbor, node, total)
        return node

    def collect_depths(node: int, parent: int, depth: int, counts: list[int]) -> None:
        if depth > maximum_distance:
            return
        if len(counts) <= depth:
            counts.extend([0] * (depth + 1 - len(counts)))
        counts[depth] += 1
        for neighbor in graph[node]:
            if neighbor != parent and not removed[neighbor]:
                collect_depths(neighbor, node, depth + 1, counts)

    def count_at_most(counts: list[int], limit: int) -> int:
        if limit < 0:
            return 0
        prefix: list[int] = []
        running = 0
        for count in counts:
            running += count
            prefix.append(running)
        ordered_pairs = 0
        self_pairs = 0
        for depth, count in enumerate(counts):
            maximum_other = min(len(counts) - 1, limit - depth)
            if maximum_other >= 0:
                ordered_pairs += count * prefix[maximum_other]
            if 2 * depth <= limit:
                self_pairs += count
        return (ordered_pairs - self_pairs) // 2

    def count_in_range(counts: list[int]) -> int:
        return count_at_most(counts, maximum_distance) - count_at_most(
            counts, minimum_distance - 1
        )

    def decompose(entry: int) -> None:
        nonlocal answer
        total = calculate_sizes(entry, -1)
        centroid = find_centroid(entry, -1, total)
        all_counts = [1]
        for neighbor in graph[centroid]:
            if removed[neighbor]:
                continue
            child_counts: list[int] = []
            collect_depths(neighbor, centroid, 1, child_counts)
            answer -= count_in_range(child_counts)
            if len(all_counts) < len(child_counts):
                all_counts.extend([0] * (len(child_counts) - len(all_counts)))
            for depth, count in enumerate(child_counts):
                all_counts[depth] += count
        answer += count_in_range(all_counts)
        removed[centroid] = True
        for neighbor in graph[centroid]:
            if not removed[neighbor]:
                decompose(neighbor)

    decompose(0)
    return answer
