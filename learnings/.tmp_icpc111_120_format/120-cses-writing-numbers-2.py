from functools import cache


def maximum_written_digit_dp(copies_per_digit: int) -> int:
    if copies_per_digit < 0:
        raise ValueError("copies_per_digit must be nonnegative")

    def digit_counts(limit: int) -> tuple[int, ...]:
        digits = tuple(int(character) for character in str(limit))

        @cache
        def solve(
            position: int, tight: bool, started: bool
        ) -> tuple[int, tuple[int, ...]]:
            if position == len(digits):
                return 1, (0,) * 10
            upper = digits[position] if tight else 9
            total_ways = 0
            total_counts = [0] * 10
            for digit in range(upper + 1):
                next_started = started or digit != 0
                ways, counts = solve(
                    position + 1,
                    tight and digit == upper,
                    next_started,
                )
                total_ways += ways
                for value in range(10):
                    total_counts[value] += counts[value]
                if next_started:
                    total_counts[digit] += ways
            return total_ways, tuple(total_counts)

        return solve(0, True, False)[1]

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
