def minimum_path_sum(grid: list[list[int]]) -> int:
    if (
        type(grid) is not list
        or not grid
        or any(
            type(row) is not list or not row or len(row) != len(grid[0]) for row in grid
        )
    ):
        raise TypeError("grid must be a nonempty rectangular list")
    if any(type(value) is not int or value < 0 for row in grid for value in row):
        raise ValueError("grid values must be non-negative integers")

    costs = [0] * len(grid[0])
    for row_index, row in enumerate(grid):
        for column, value in enumerate(row):
            if row_index == 0 and column == 0:
                costs[column] = value
            elif row_index == 0:
                costs[column] = costs[column - 1] + value
            elif column == 0:
                costs[column] += value
            else:
                costs[column] = min(costs[column], costs[column - 1]) + value
    return costs[-1]
