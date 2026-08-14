def maximum_written_positional(copies_per_digit: int) -> int:
    if copies_per_digit < 0:
        raise ValueError("copies_per_digit must be nonnegative")

    def digit_counts(limit: int) -> list[int]:
        counts = [0] * 10
        factor = 1
        while factor <= limit:
            lower = limit % factor
            current = (limit // factor) % 10
            higher = limit // (factor * 10)

            for digit in range(1, 10):
                counts[digit] += higher * factor
                if current > digit:
                    counts[digit] += factor
                elif current == digit:
                    counts[digit] += lower + 1

            if higher > 0:
                counts[0] += (higher - 1) * factor
                if current == 0:
                    counts[0] += lower + 1
                else:
                    counts[0] += factor
            factor *= 10
        return counts

    def fits(limit: int) -> bool:
        return max(digit_counts(limit)) <= copies_per_digit

    low = 0
    high = 1
    while fits(high):
        low = high
        high *= 2
    while low + 1 < high:
        middle = (low + high) // 2
        if fits(middle):
            low = middle
        else:
            high = middle
    return low
