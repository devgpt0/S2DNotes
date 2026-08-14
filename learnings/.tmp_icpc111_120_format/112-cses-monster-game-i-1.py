def monster_game_i_brute(
    query_points: list[int], line_slopes: list[int], initial_slope: int
) -> int:
    if not query_points or len(query_points) != len(line_slopes):
        raise ValueError("query_points and line_slopes need equal nonzero length")

    dynamic = [0] * len(query_points)
    for index, point in enumerate(query_points):
        best = initial_slope * point
        for previous in range(index):
            best = min(
                best,
                dynamic[previous] + line_slopes[previous] * point,
            )
        dynamic[index] = best
    return dynamic[-1]
