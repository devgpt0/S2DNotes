def bit_problem_enumerate(values: list[int]) -> list[tuple[int, int, int]]:
    if any(value < 0 for value in values):
        raise ValueError("values must be nonnegative")
    bit_count = max(1, max(values, default=0).bit_length())
    full_mask = (1 << bit_count) - 1
    frequency = [0] * (full_mask + 1)
    for value in values:
        frequency[value] += 1

    def count_submasks(mask: int) -> int:
        total = 0
        submask = mask
        while True:
            total += frequency[submask]
            if submask == 0:
                return total
            submask = (submask - 1) & mask

    answers: list[tuple[int, int, int]] = []
    for value in values:
        submasks = count_submasks(value)
        missing = full_mask ^ value
        supermasks = 0
        addition = missing
        while True:
            supermasks += frequency[value | addition]
            if addition == 0:
                break
            addition = (addition - 1) & missing
        disjoint = count_submasks(missing)
        answers.append((submasks, supermasks, len(values) - disjoint))
    return answers
