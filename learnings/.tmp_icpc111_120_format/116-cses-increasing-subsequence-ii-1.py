MODULO = 1_000_000_007


def increasing_subsequences_brute(values: list[int]) -> int:
    count = 0
    for mask in range(1, 1 << len(values)):
        chosen = [values[index] for index in range(len(values)) if mask & (1 << index)]
        if all(chosen[index - 1] < chosen[index] for index in range(1, len(chosen))):
            count += 1
    return count % MODULO
