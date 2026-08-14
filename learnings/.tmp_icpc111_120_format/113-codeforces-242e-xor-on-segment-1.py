def xor_on_segment_brute(
    values: list[int], operations: list[tuple[int, ...]]
) -> list[int]:
    if not values or any(value < 0 for value in values):
        raise ValueError("values must be nonempty and nonnegative")

    current = values.copy()
    answers: list[int] = []
    for operation in operations:
        operation_type = operation[0]
        if operation_type == 1:
            _, left, right = operation
            answers.append(sum(current[left : right + 1]))
        elif operation_type == 2:
            _, left, right, mask = operation
            if mask < 0:
                raise ValueError("XOR masks must be nonnegative")
            for index in range(left, right + 1):
                current[index] ^= mask
        else:
            raise ValueError(f"unknown operation type: {operation_type}")
    return answers
