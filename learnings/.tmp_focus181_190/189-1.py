def unique_paths_with_obstacles_brute(grid: list[list[int]]) -> int:
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

    def count(row: int, column: int) -> int:
        if row == len(grid) or column == len(grid[0]) or grid[row][column] == 1:
            return 0
        if (row, column) == (len(grid) - 1, len(grid[0]) - 1):
            return 1
        return count(row + 1, column) + count(row, column + 1)

    return count(0, 0)
