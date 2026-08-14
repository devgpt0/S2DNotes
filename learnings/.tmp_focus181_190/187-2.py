class ListNode:
    def __init__(self, value: int, next_node: "ListNode | None" = None) -> None:
        self.value = value
        self.next = next_node


def rotate_list(head: ListNode | None, rotations: int) -> ListNode | None:
    if head is not None and type(head) is not ListNode:
        raise TypeError("head must be a ListNode or None")
    if type(rotations) is not int:
        raise TypeError("rotations must be an integer")
    if not 0 <= rotations <= 2_000_000_000:
        raise ValueError("rotations must be between 0 and 2000000000")
    if head is None:
        return None

    seen: set[int] = set()
    tail = head
    length = 0
    while True:
        if id(tail) in seen:
            raise ValueError("input list must not contain a cycle")
        if type(tail.value) is not int:
            raise TypeError("node values must be integers")
        seen.add(id(tail))
        length += 1
        if length > 500:
            raise ValueError("input list may contain at most 500 nodes")
        if tail.next is None:
            break
        tail = tail.next

    rotations %= length
    if rotations == 0:
        return head
    tail.next = head
    new_tail = head
    for _ in range(length - rotations - 1):
        if new_tail.next is None:
            raise RuntimeError("temporary cycle ended unexpectedly")
        new_tail = new_tail.next
    new_head = new_tail.next
    new_tail.next = None
    return new_head
