MODULO = 1_000_000_007


def increasing_subsequences_fenwick(values: list[int]) -> int:
    ranks = {value: index + 1 for index, value in enumerate(sorted(set(values)))}
    tree = [0] * (len(ranks) + 1)

    def prefix_sum(index: int) -> int:
        total = 0
        while index > 0:
            total += tree[index]
            index -= index & -index
        return total % MODULO

    def add(index: int, amount: int) -> None:
        while index < len(tree):
            tree[index] = (tree[index] + amount) % MODULO
            index += index & -index

    answer = 0
    for value in values:
        rank = ranks[value]
        ways = (1 + prefix_sum(rank - 1)) % MODULO
        add(rank, ways)
        answer = (answer + ways) % MODULO
    return answer
