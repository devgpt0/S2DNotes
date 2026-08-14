def generate_spiral_matrix_brute(size: int) -> list[list[int]]:
    if type(size) is not int:
        raise TypeError("size must be an integer")
    if not 1 <= size <= 20:
        raise ValueError("size must be between 1 and 20")

    matrix = [[0] * size for _ in range(size)]
    directions = ((0, 1), (1, 0), (0, -1), (-1, 0))
    direction = 0
    row = 0
    column = 0
    for value in range(1, size * size + 1):
        matrix[row][column] = value
        row_step, column_step = directions[direction]
        next_row = row + row_step
        next_column = column + column_step
        if not (
            0 <= next_row < size
            and 0 <= next_column < size
            and matrix[next_row][next_column] == 0
        ):
            direction = (direction + 1) % 4
            row_step, column_step = directions[direction]
            next_row = row + row_step
            next_column = column + column_step
        row, column = next_row, next_column
    return matrix
