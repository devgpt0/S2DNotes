def unique_paths_with_obstacles(grid: list[list[int]]) -> int:
    if (
        type(grid) is not list
        or not grid
        or len(grid) > 100
        or any(
            type(row) is not list
            or not row
            or len(row) != len(grid[0])
            or len(row) > 100
            for row in grid
        )
    ):
        raise TypeError("grid must be a nonempty rectangle of side at most 100")
    if any(
        type(value) is not int or value not in (0, 1) for row in grid for value in row
    ):
        raise ValueError("grid values must be integer zeroes and ones")

    ways = [0] * len(grid[0])
    ways[0] = 1
    for row in grid:
        for column, blocked in enumerate(row):
            if blocked:
                ways[column] = 0
            elif column > 0:
                ways[column] += ways[column - 1]
    return ways[-1]
