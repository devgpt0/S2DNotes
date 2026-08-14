def unique_paths_brute(rows: int, columns: int) -> int:
    if type(rows) is not int or type(columns) is not int:
        raise TypeError("rows and columns must be integers")
    if not 1 <= rows <= 100 or not 1 <= columns <= 100:
        raise ValueError("rows and columns must be between 1 and 100")

    def count(row: int, column: int) -> int:
        if row == rows - 1 or column == columns - 1:
            return 1
        return count(row + 1, column) + count(row, column + 1)

    return count(0, 0)
