def empty_string_interval_dp(text: str, modulo: int = 1_000_000_007) -> int:
    if modulo <= 0:
        raise ValueError("modulo must be positive")
    if len(text) % 2 == 1:
        return 0

    pair_count = len(text) // 2
    choose = [[0] * (pair_count + 1) for _ in range(pair_count + 1)]
    for total in range(pair_count + 1):
        choose[total][0] = choose[total][total] = 1
        for selected in range(1, total):
            choose[total][selected] = (
                choose[total - 1][selected - 1] + choose[total - 1][selected]
            ) % modulo

    length = len(text)
    dynamic = [[0] * (length + 1) for _ in range(length + 1)]
    for index in range(length + 1):
        dynamic[index][index] = 1

    for interval_length in range(2, length + 1, 2):
        total_pairs = interval_length // 2
        for left in range(length - interval_length + 1):
            right = left + interval_length
            total = 0
            for partner in range(left + 1, right, 2):
                if text[left] != text[partner]:
                    continue
                left_block_pairs = (partner - left + 1) // 2
                total += (
                    dynamic[left + 1][partner]
                    * dynamic[partner + 1][right]
                    * choose[total_pairs][left_block_pairs]
                )
            dynamic[left][right] = total % modulo
    return dynamic[0][length]
