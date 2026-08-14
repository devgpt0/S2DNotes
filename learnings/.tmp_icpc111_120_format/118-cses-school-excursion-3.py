def excursion_sizes_bitset(
    child_count: int, friendships: list[tuple[int, int]]
) -> list[bool]:
    if child_count <= 0:
        raise ValueError("child_count must be positive")
    parent = list(range(child_count))
    sizes = [1] * child_count

    def find(node: int) -> int:
        while parent[node] != node:
            parent[node] = parent[parent[node]]
            node = parent[node]
        return node

    for first, second in friendships:
        if not 0 <= first < child_count or not 0 <= second < child_count:
            raise ValueError("friendship endpoint out of range")
        first_root = find(first)
        second_root = find(second)
        if first_root == second_root:
            continue
        if sizes[first_root] < sizes[second_root]:
            first_root, second_root = second_root, first_root
        parent[second_root] = first_root
        sizes[first_root] += sizes[second_root]

    possible = 1
    for node in range(child_count):
        if find(node) == node:
            possible |= possible << sizes[node]
    return [bool(possible & (1 << size)) for size in range(1, child_count + 1)]
