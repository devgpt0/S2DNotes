def generate_spiral_matrix(size: int) -> list[list[int]]:
    if type(size) is not int:
        raise TypeError("size must be an integer")
    if not 1 <= size <= 20:
        raise ValueError("size must be between 1 and 20")

    matrix = [[0] * size for _ in range(size)]
    top = 0
    bottom = size - 1
    left = 0
    right = size - 1
    value = 1
    while top <= bottom and left <= right:
        for column in range(left, right + 1):
            matrix[top][column] = value
            value += 1
        top += 1
        for row in range(top, bottom + 1):
            matrix[row][right] = value
            value += 1
        right -= 1
        if top <= bottom:
            for column in range(right, left - 1, -1):
                matrix[bottom][column] = value
                value += 1
            bottom -= 1
        if left <= right:
            for row in range(bottom, top - 1, -1):
                matrix[row][left] = value
                value += 1
            left += 1
    return matrix
