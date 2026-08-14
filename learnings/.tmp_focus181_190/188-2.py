def unique_paths_dp(rows: int, columns: int) -> int:
    if type(rows) is not int or type(columns) is not int:
        raise TypeError("rows and columns must be integers")
    if not 1 <= rows <= 100 or not 1 <= columns <= 100:
        raise ValueError("rows and columns must be between 1 and 100")

    ways = [1] * columns
    for _ in range(1, rows):
        for column in range(1, columns):
            ways[column] += ways[column - 1]
    return ways[-1]
