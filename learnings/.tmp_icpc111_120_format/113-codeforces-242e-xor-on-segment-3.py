def xor_on_segment_lazy(
    values: list[int], operations: list[tuple[int, ...]]
) -> list[int]:
    if not values or any(value < 0 for value in values):
        raise ValueError("values must be nonempty and nonnegative")

    maximum = max(values)
    for operation in operations:
        if operation[0] == 2:
            maximum = max(maximum, operation[3])
    bit_count = max(1, maximum.bit_length())
    size = len(values)
    ones = [[0] * (4 * size) for _ in range(bit_count)]
    pending_xor = [0] * (4 * size)

    def build(node: int, low: int, high: int) -> None:
        if low == high:
            for bit in range(bit_count):
                ones[bit][node] = (values[low] >> bit) & 1
            return
        middle = (low + high) // 2
        build(2 * node, low, middle)
        build(2 * node + 1, middle + 1, high)
        for bit in range(bit_count):
            ones[bit][node] = ones[bit][2 * node] + ones[bit][2 * node + 1]

    def apply(node: int, low: int, high: int, mask: int) -> None:
        for bit in range(bit_count):
            if mask & (1 << bit):
                ones[bit][node] = high - low + 1 - ones[bit][node]
        pending_xor[node] ^= mask

    def push(node: int, low: int, high: int) -> None:
        mask = pending_xor[node]
        if mask == 0 or low == high:
            return
        middle = (low + high) // 2
        apply(2 * node, low, middle, mask)
        apply(2 * node + 1, middle + 1, high, mask)
        pending_xor[node] = 0

    def update(
        node: int, low: int, high: int, left: int, right: int, mask: int
    ) -> None:
        if left <= low and high <= right:
            apply(node, low, high, mask)
            return
        push(node, low, high)
        middle = (low + high) // 2
        if left <= middle:
            update(2 * node, low, middle, left, right, mask)
        if right > middle:
            update(2 * node + 1, middle + 1, high, left, right, mask)
        for bit in range(bit_count):
            ones[bit][node] = ones[bit][2 * node] + ones[bit][2 * node + 1]

    def query(node: int, low: int, high: int, left: int, right: int) -> int:
        if left <= low and high <= right:
            return sum(ones[bit][node] << bit for bit in range(bit_count))
        push(node, low, high)
        middle = (low + high) // 2
        total = 0
        if left <= middle:
            total += query(2 * node, low, middle, left, right)
        if right > middle:
            total += query(2 * node + 1, middle + 1, high, left, right)
        return total

    build(1, 0, size - 1)
    answers: list[int] = []
    for operation in operations:
        if operation[0] == 1:
            _, left, right = operation
            answers.append(query(1, 0, size - 1, left, right))
        elif operation[0] == 2:
            _, left, right, mask = operation
            if mask < 0:
                raise ValueError("XOR masks must be nonnegative")
            update(1, 0, size - 1, left, right, mask)
        else:
            raise ValueError(f"unknown operation type: {operation[0]}")
    return answers
