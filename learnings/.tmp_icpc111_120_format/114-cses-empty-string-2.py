from functools import cache


def empty_string_memoized(text: str, modulo: int = 1_000_000_007) -> int:
    if modulo <= 0:
        raise ValueError("modulo must be positive")

    @cache
    def count(remaining: str) -> int:
        if not remaining:
            return 1
        if len(remaining) % 2 == 1:
            return 0
        total = 0
        for index in range(len(remaining) - 1):
            if remaining[index] == remaining[index + 1]:
                total += count(remaining[:index] + remaining[index + 2 :])
        return total % modulo

    return count(text)
