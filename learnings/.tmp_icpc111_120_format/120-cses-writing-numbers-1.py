def maximum_written_brute(copies_per_digit: int) -> int:
    if copies_per_digit < 0:
        raise ValueError("copies_per_digit must be nonnegative")
    used = [0] * 10
    number = 0
    while True:
        candidate = number + 1
        required = [0] * 10
        for character in str(candidate):
            required[int(character)] += 1
        if any(used[digit] + required[digit] > copies_per_digit for digit in range(10)):
            return number
        for digit in range(10):
            used[digit] += required[digit]
        number = candidate
