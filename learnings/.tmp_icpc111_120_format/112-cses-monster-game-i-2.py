def monster_game_i_li_chao(
    query_points: list[int], line_slopes: list[int], initial_slope: int
) -> int:
    if not query_points or len(query_points) != len(line_slopes):
        raise ValueError("query_points and line_slopes need equal nonzero length")

    coordinates = sorted(set(query_points))
    lines: list[tuple[int, int] | None] = [None] * (4 * len(coordinates))

    def value(line: tuple[int, int], point: int) -> int:
        return line[0] * point + line[1]

    def add_line(node: int, low: int, high: int, new_line: tuple[int, int]) -> None:
        current = lines[node]
        if current is None:
            lines[node] = new_line
            return

        middle = (low + high) // 2
        if value(new_line, coordinates[middle]) < value(current, coordinates[middle]):
            lines[node], new_line = new_line, current
            current = lines[node]
        if low == high:
            return
        if value(new_line, coordinates[low]) < value(current, coordinates[low]):
            add_line(2 * node, low, middle, new_line)
        elif value(new_line, coordinates[high]) < value(current, coordinates[high]):
            add_line(2 * node + 1, middle + 1, high, new_line)

    def query(node: int, low: int, high: int, index: int) -> int:
        line = lines[node]
        best = value(line, coordinates[index]) if line is not None else 10**40
        if low == high:
            return best
        middle = (low + high) // 2
        if index <= middle:
            return min(best, query(2 * node, low, middle, index))
        return min(best, query(2 * node + 1, middle + 1, high, index))

    coordinate_index = {point: index for index, point in enumerate(coordinates)}
    add_line(1, 0, len(coordinates) - 1, (initial_slope, 0))
    answer = 0
    for point, slope in zip(query_points, line_slopes, strict=True):
        answer = query(1, 0, len(coordinates) - 1, coordinate_index[point])
        add_line(1, 0, len(coordinates) - 1, (slope, answer))
    return answer
