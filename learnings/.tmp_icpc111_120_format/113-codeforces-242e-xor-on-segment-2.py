from math import isqrt


def xor_on_segment_sqrt(
    values: list[int], operations: list[tuple[int, ...]]
) -> list[int]:
    if not values or any(value < 0 for value in values):
        raise ValueError("values must be nonempty and nonnegative")

    maximum = max(values)
    for operation in operations:
        if operation[0] == 2:
            maximum = max(maximum, operation[3])
    bit_count = max(1, maximum.bit_length())
    current = values.copy()
    block_size = isqrt(len(values)) + 1
    block_count = (len(values) + block_size - 1) // block_size
    ones = [[0] * bit_count for _ in range(block_count)]
    pending_xor = [0] * block_count

    def bounds(block: int) -> tuple[int, int]:
        start = block * block_size
        return start, min(start + block_size, len(current))

    def rebuild(block: int) -> None:
        ones[block] = [0] * bit_count
        start, end = bounds(block)
        for index in range(start, end):
            for bit in range(bit_count):
                ones[block][bit] += (current[index] >> bit) & 1

    def push(block: int) -> None:
        mask = pending_xor[block]
        if mask == 0:
            return
        start, end = bounds(block)
        for index in range(start, end):
            current[index] ^= mask
        pending_xor[block] = 0
        rebuild(block)

    def apply_full(block: int, mask: int) -> None:
        start, end = bounds(block)
        for bit in range(bit_count):
            if mask & (1 << bit):
                ones[block][bit] = end - start - ones[block][bit]
        pending_xor[block] ^= mask

    def block_sum(block: int) -> int:
        return sum(count << bit for bit, count in enumerate(ones[block]))

    for block in range(block_count):
        rebuild(block)

    answers: list[int] = []
    for operation in operations:
        operation_type = operation[0]
        left = operation[1]
        right = operation[2]
        first_block = left // block_size
        last_block = right // block_size
        if operation_type == 1:
            if first_block == last_block:
                push(first_block)
                answers.append(sum(current[left : right + 1]))
                continue
            push(first_block)
            _, first_end = bounds(first_block)
            total = sum(current[left:first_end])
            total += sum(
                block_sum(block) for block in range(first_block + 1, last_block)
            )
            push(last_block)
            last_start, _ = bounds(last_block)
            answers.append(total + sum(current[last_start : right + 1]))
        elif operation_type == 2:
            mask = operation[3]
            if mask < 0:
                raise ValueError("XOR masks must be nonnegative")
            if first_block == last_block:
                push(first_block)
                for index in range(left, right + 1):
                    current[index] ^= mask
                rebuild(first_block)
                continue
            push(first_block)
            _, first_end = bounds(first_block)
            for index in range(left, first_end):
                current[index] ^= mask
            rebuild(first_block)
            for block in range(first_block + 1, last_block):
                apply_full(block, mask)
            push(last_block)
            last_start, _ = bounds(last_block)
            for index in range(last_start, right + 1):
                current[index] ^= mask
            rebuild(last_block)
        else:
            raise ValueError(f"unknown operation type: {operation_type}")
    return answers
