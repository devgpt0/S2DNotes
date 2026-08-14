class ListNode:
    def __init__(self, value: int, next_node: "ListNode | None" = None) -> None:
        self.value = value
        self.next = next_node


def rotate_list_brute(head: ListNode | None, rotations: int) -> ListNode | None:
    if head is not None and type(head) is not ListNode:
        raise TypeError("head must be a ListNode or None")
    if type(rotations) is not int:
        raise TypeError("rotations must be an integer")
    if not 0 <= rotations <= 2_000_000_000:
        raise ValueError("rotations must be between 0 and 2000000000")
    seen: set[int] = set()
    node = head
    length = 0
    while node is not None:
        if id(node) in seen:
            raise ValueError("input list must not contain a cycle")
        if type(node.value) is not int:
            raise TypeError("node values must be integers")
        seen.add(id(node))
        length += 1
        if length > 500:
            raise ValueError("input list may contain at most 500 nodes")
        node = node.next

    for _ in range(rotations):
        if head is None or head.next is None:
            return head
        new_tail = head
        while new_tail.next is not None and new_tail.next.next is not None:
            new_tail = new_tail.next
        new_head = new_tail.next
        new_tail.next = None
        if new_head is None:
            raise RuntimeError("a multi-node list must have a tail")
        new_head.next = head
        head = new_head
    return head
