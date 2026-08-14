def empty_string_brute(text: str, modulo: int = 1_000_000_007) -> int:
    if modulo <= 0:
        raise ValueError("modulo must be positive")
    if len(text) % 2 == 1:
        return 0
    if not text:
        return 1

    total = 0
    for index in range(len(text) - 1):
        if text[index] == text[index + 1]:
            total += empty_string_brute(text[:index] + text[index + 2 :], modulo)
    return total % modulo
