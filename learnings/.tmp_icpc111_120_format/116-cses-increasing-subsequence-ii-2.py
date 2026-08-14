MODULO = 1_000_000_007


def increasing_subsequences_quadratic(values: list[int]) -> int:
    ways = [1] * len(values)
    for end, value in enumerate(values):
        for previous in range(end):
            if values[previous] < value:
                ways[end] = (ways[end] + ways[previous]) % MODULO
    return sum(ways) % MODULO
