def minimum_path_sum_brute(grid: list[list[int]]) -> int:
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

    def cost(row: int, column: int) -> int:
        if (row, column) == (len(grid) - 1, len(grid[0]) - 1):
            return grid[row][column]
        candidates: list[int] = []
        if row + 1 < len(grid):
            candidates.append(cost(row + 1, column))
        if column + 1 < len(grid[0]):
            candidates.append(cost(row, column + 1))
        return grid[row][column] + min(candidates)

    return cost(0, 0)
