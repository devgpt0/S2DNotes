def excursion_sizes_brute(
    child_count: int, friendships: list[tuple[int, int]]
) -> list[bool]:
    if child_count <= 0:
        raise ValueError("child_count must be positive")
    graph = [[] for _ in range(child_count)]
    for first, second in friendships:
        if not 0 <= first < child_count or not 0 <= second < child_count:
            raise ValueError("friendship endpoint out of range")
        graph[first].append(second)
        graph[second].append(first)

    seen = [False] * child_count
    component_sizes: list[int] = []
    for start in range(child_count):
        if seen[start]:
            continue
        seen[start] = True
        stack = [start]
        size = 0
        while stack:
            node = stack.pop()
            size += 1
            for neighbor in graph[node]:
                if not seen[neighbor]:
                    seen[neighbor] = True
                    stack.append(neighbor)
        component_sizes.append(size)

    possible = [False] * (child_count + 1)
    for mask in range(1 << len(component_sizes)):
        total = sum(
            size for index, size in enumerate(component_sizes) if mask & (1 << index)
        )
        possible[total] = True
    return possible[1:]
