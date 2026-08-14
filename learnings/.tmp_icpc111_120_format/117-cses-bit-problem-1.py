def bit_problem_brute(values: list[int]) -> list[tuple[int, int, int]]:
    if any(value < 0 for value in values):
        raise ValueError("values must be nonnegative")

    answers: list[tuple[int, int, int]] = []
    for value in values:
        submasks = sum(1 for other in values if value | other == value)
        supermasks = sum(1 for other in values if value & other == value)
        intersecting = sum(1 for other in values if value & other != 0)
        answers.append((submasks, supermasks, intersecting))
    return answers
