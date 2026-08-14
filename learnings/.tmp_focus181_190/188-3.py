from math import comb


def unique_paths(rows: int, columns: int) -> int:
    if type(rows) is not int or type(columns) is not int:
        raise TypeError("rows and columns must be integers")
    if not 1 <= rows <= 100 or not 1 <= columns <= 100:
        raise ValueError("rows and columns must be between 1 and 100")
    return comb(rows + columns - 2, rows - 1)
