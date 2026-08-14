def bit_problem_sos(values: list[int]) -> list[tuple[int, int, int]]:
    if any(value < 0 for value in values):
        raise ValueError("values must be nonnegative")
    bit_count = max(1, max(values, default=0).bit_length())
    universe_size = 1 << bit_count
    full_mask = universe_size - 1

    frequency = [0] * universe_size
    for value in values:
        frequency[value] += 1
    submask_count = frequency.copy()
    supermask_count = frequency.copy()

    for index in range(bit_count):
        bit = 1 << index
        for mask in range(universe_size):
            if mask & bit:
                submask_count[mask] += submask_count[mask ^ bit]
            else:
                supermask_count[mask] += supermask_count[mask | bit]

    return [
        (
            submask_count[value],
            supermask_count[value],
            len(values) - submask_count[full_mask ^ value],
        )
        for value in values
    ]
