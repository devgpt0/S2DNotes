from collections import deque


def monster_game_i_monotone_hull(
    query_points: list[int], line_slopes: list[int], initial_slope: int
) -> int:
    if not query_points or len(query_points) != len(line_slopes):
        raise ValueError("query_points and line_slopes need equal nonzero length")
    if any(
        query_points[index] > query_points[index + 1]
        for index in range(len(query_points) - 1)
    ):
        raise ValueError("query points must be nondecreasing")
    inserted_slopes = [initial_slope, *line_slopes]
    if any(
        inserted_slopes[index] < inserted_slopes[index + 1]
        for index in range(len(inserted_slopes) - 1)
    ):
        raise ValueError("inserted slopes must be nonincreasing")

    lines: deque[tuple[int, int]] = deque()

    def evaluate(line: tuple[int, int], point: int) -> int:
        return line[0] * point + line[1]

    def redundant(
        first: tuple[int, int],
        second: tuple[int, int],
        third: tuple[int, int],
    ) -> bool:
        return (second[1] - first[1]) * (second[0] - third[0]) >= (
            third[1] - second[1]
        ) * (first[0] - second[0])

    def add_line(slope: int, intercept: int) -> None:
        while lines and lines[-1][0] == slope:
            if lines[-1][1] <= intercept:
                return
            lines.pop()
        new_line = (slope, intercept)
        while len(lines) >= 2 and redundant(lines[-2], lines[-1], new_line):
            lines.pop()
        lines.append(new_line)

    add_line(initial_slope, 0)
    answer = 0
    for point, slope in zip(query_points, line_slopes, strict=True):
        while len(lines) >= 2 and evaluate(lines[0], point) >= evaluate(
            lines[1], point
        ):
            lines.popleft()
        answer = evaluate(lines[0], point)
        add_line(slope, answer)
    return answer
