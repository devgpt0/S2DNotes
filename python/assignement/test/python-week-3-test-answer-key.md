# PYTHON WEEK 3 TEST - ANSWER KEY

Format: Qn -> Output/Option | Reason

## Q1
Output: `[3, 8, -8, 9, -12]` then `[9, 8, 3, -8, -12]`
Reason: `sorted(..., key=abs)` returns a new list; `sort(reverse=True)` mutates `nums`.

## Q2
Output: `{4, 16, 36, 64}` (set order may vary)
Reason: Squares of even numbers from `1..8`.

## Q3
Output: `['red', 'cyan', 'black', 'green']` then `['red', 'cyan', 'black', 'green']`
Reason: `reversed(tokens)` gives reverse order; `tokens.reverse()` mutates list to the same order.

## Q4
Output: `[12, 17, 1]`
Reason: Slice `1:4` includes indices `1,2,3`.

## Q5
Output: `keyerror` then `{10, 20, 30}` (set order may vary)
Reason: `remove(109)` raises `KeyError`; `discard(109)` is safe if missing.

## Q6
Output: `20` then `{'p': 10, 'r': 30}`
Reason: `pop('q')` returns removed value and deletes key.

## Q7
Output: `[21, 6, 28]`
Reason: Slice from index `1` to `3`.

## Q8
Output: `88` then `NA`
Reason: Existing key returns value; missing key uses default.

## Q9
Output: `[6, 10, 11, 13]`
Reason: Slice `2:6` includes indices `2..5`.

## Q10
Output: `(8, 3, 3)` then `(2, 3, 3, 8, 8)`
Reason: Tuple slicing and reverse slicing.

## Q11
Output: `[20, 7]`
Reason: Slice `2:4` includes indices `2,3`.

## Q12
Output: `2` then `[2, 75, 2, 1, 9]`
Reason: After insert, `pop(2)` removes third element.

## Q13
Output: `1` then `50` then `{'a': 1, 'b': 50}`
Reason: `setdefault` returns current value if key exists, else inserts default.

## Q14
Output: `{'scores': [10, 20, 30]}` then `{'scores': [10, 20, 30]}`
Reason: `copy()` is shallow; nested list is shared.

## Q15
Output: `3` then `[1, 9, 6, 69, 7]`
Reason: Insert at index 3, then pop index 4.

## Q16
Output: `1` then `[2, 3, 4]` then `5`
Reason: Starred unpacking captures middle values into a list.

## Q17
Answer: `B`
Reason: `pop()` without index removes and returns the last item.

## Q18
Answer: `B`
Reason: `get` avoids `KeyError` and supports fallback.

## Q19
Answer: `C`
Reason: One-element tuple needs trailing comma.

## Q20
Answer: `B`
Reason: Set elements must be hashable.

## Q21
Answer: `B`
Reason: `dict.copy()` performs shallow copy.

## Q22
Answer: `C`
Reason: Same list object is reused for all keys.

## Q23
Answer: `B`
Reason: `sorted` returns a new list.

## Q24
Answer: `B`
Reason: `extend` adds each element from iterable.

## Q25
Answer: `B`
Reason: Tuples fit fixed-shape records.

## Q26
Answer: `C`
Reason: Same start and end gives empty slice.

## Q27
Answer: `B`
Reason: `discard` does nothing if element is absent.

## Q28
Answer: `B`
Reason: Assignment aliases same list object.

## Q29
Answer: `C`
Reason: `in` on dict checks keys.

## Q30
Answer: `C`
Reason: Sets provide fast membership checks.

## Q31
Output: `{'a': 2, 'b': 2, 'c': 1}`
Reason: `defaultdict(int)` starts counts at 0 and increments per character.

## Q32
Output: `[4, 8, 4, 8, 6]` then `30`
Reason: Flatten even values, then sum.

## Q33
Output: `12 4`
Reason: Dispatch table calls `add` and `sub`.

## Q34
Output: `Counter({3: 3, 2: 2, 4: 1})` then `[(3, 3)]`
Reason: Counter stores frequencies; `most_common(1)` returns top pair.

## Q35
Output: `[('q', 52), ('p', 58), ('r', 87)]`
Reason: Sorted by second tuple value, then key.

## Q36
Output: `6` then `[11, 14]` then `8`
Reason: Starred unpacking for function return tuple.

## Q37
Output: `[(14, 'x'), (24, 'y')]` then `[(14, 'x'), (24, 'y'), (34, 'NA')]`
Reason: `zip` truncates to shortest; `zip_longest` pads with fill value.

## Q38
Output: `[('x', 6), ('z', 5), ('y', 4)]`
Reason: Sort dict items by value descending.

## Q39
Output: `13 7`
Reason: `10+3` and `10-3`.

## Q40
Output: `14`
Reason: `MappingProxyType` is a live read-only view of the base dict.

## Q41
Output: `(6, 4, 8)` then `[4, 6, 8]` then `True`
Reason: `reversed` gives iterator, `sorted` returns list, full tuple slice is same tuple object.

## Q42
Output: `9`
Reason: Proxy reflects base dict update.

## Q43
Output: `True True` then `True True`
Reason: Proper subset/superset relations hold.

## Q44
Output: `{3, 4, 5, 6}` (set order may vary)
Reason: Set comprehension deduplicates flattened values.

## Q45
Output: `{4, 5, 6, 7}` then `{6, 7}`
Reason: `&` precedence is higher than `|`.

## Q46
Output: `[8, 4, 8, 6]` then `26`
Reason: Keep evens while flattening, then sum.

## Q47
Output: `[(4, 81), (5, 81)]`
Reason: Odd squares with indices; last two selected.

## Q48
Output: `15 11`
Reason: `13+2` and `13-2`.

## Q49
Output: `[[0, 9, 0], [0, 9, 0]]`
Reason: Repeated inner list references same object.

## Q50
Output: `[(1, 1), (5, 49)]`
Reason: Odd values at indices `0,1,5`; last two entries shown.

## Q51
Output: `True True` then `True True`
Reason: `a` is proper subset of `b`.

## Q52
Output: `4`
Reason: First value encountered twice is 4.

## Q53
Output: `True True` then `True True`
Reason: Same subset/superset relation pattern.

## Q54
Output: `{2, 3, 4, 5}` then `{4, 5}`
Reason: Intersection first in `a | b & c`; explicit parentheses change grouping.

## Q55
Output: `[('q', 62), ('r', 77), ('p', 82)]`
Reason: Ascending by score.

## Q56
Output: `[8, 4, 8]` then `20`
Reason: Even flatten and sum.

## Q57
Output: `{'c': 2, 'a': 2, 'b': 1}`
Reason: Character counting with insertion order by first appearance.

## Q58
Output: `[[1], [2]]` then `[[1, 7], [2]]`
Reason: `deepcopy` creates independent nested lists.

## Q59
Output: `13` then `[12, 6, 1]` then `15`
Reason: Starred unpacking on list.

## Q60
Output: `Counter({4: 3, 3: 2, 5: 1})` then `[(4, 3)]`
Reason: Frequency counts and top-most item.

## Q61
Output: `[(3, 1), (4, 81)]`
Reason: Only odd values are at indices 3 and 4.

## Q62
Output: `{6: 'float-like'}` then `1`
Reason: `6` and `6.0` are equal keys with same hash, so second assignment overwrites.

## Q63
Output: `3`
Reason: First duplicate encountered is 3.

## Q64
Output: `7` then `[11, 14]` then `9`
Reason: Unpacking returned tuple with star target.

## Q65
Output: `[('r', 58), ('q', 72), ('p', 75)]`
Reason: Sort by numeric value ascending.

## Q66
Output: `5` then `[10, 13]` then `7`
Reason: Same unpacking pattern.

## Q67
Output: `[2, 6, 8]` then `16`
Reason: Even flatten then sum.

## Q68
Output: `[(3, 121), (4, 49)]`
Reason: Odd values transformed to `(index, square)`; last two kept.

## Q69
Output: `{3, 4, 5, 6}` then `{5, 6}`
Reason: `&` before `|`; grouped version intersects with `c` after union.

## Q70
Output: `None` then `{1, 3}`
Reason: `difference_update` mutates set in place and returns `None`.

## Q71
Output: `solarized en`
Reason: `ChainMap` searches left-to-right maps.

## Q72
Output: `[('x', 4), ('z', 3), ('y', 2)]`
Reason: Sorted descending by value.

## Q73
Output: `{1, 2, 3, 4}` then `{3, 4}`
Reason: Operator precedence and grouping effect.

## Q74
Output: `[(10, 'x'), (20, 'y')]` then `[(10, 'x'), (20, 'y'), (30, 'NA')]`
Reason: `zip` truncates; `zip_longest` pads.

## Q75
Output: `{1, 2, 3, 4}` (set order may vary)
Reason: Unique flattened values.

## Q76
Output: `13 9`
Reason: `11+2` and `11-2`.

## Q77
Output: `NEO` then `NORA` then `NA`
Reason: Generator yields matching names in order; third `next` uses fallback.

## Q78
Output: `13`
Reason: Mapping proxy reflects updated base dict value.

## Q79
Output: `[2, 6, 6, 8]` then `22`
Reason: Even flatten and sum.

## Q80
Output: `6`
Reason: First repeated number in traversal is 6.

## Q81
Output: `[('x', 5), ('z', 4), ('y', 3)]`
Reason: Sort dict items by value descending.

## Q82
Output: `(5, 3, 7)` then `[3, 5, 7]` then `True`
Reason: Reverse tuple, sorted list, and full tuple slice identity.

## Q83
Output: `{1: 'float-like'}` then `1`
Reason: `1` and `1.0` collide as same dict key.

## Q84
Output: `7` then `[7, 10]` then `9`
Reason: Star-unpacking between first and last.

## Q85
Output: `{2: 'float-like'}` then `1`
Reason: `2` and `2.0` are same dict key.

## Q86
Output: `light en`
Reason: First map supplies `theme`, second supplies `lang`.

## Q87
Output: `True True` then `True True`
Reason: `a` is proper subset of `b`.

## Q88
Output: `(1, [7, 8, 13])` then `(1, [7, 8])`
Reason: Shallow copy shares inner list; deep copy duplicates it.

## Q89
Output: `[('p', 54), ('r', 66), ('q', 80)]`
Reason: Sorted by second value ascending.

## Q90
Output: `(1, [3, 4, 9])` then `(1, [3, 4])`
Reason: Inner list mutation appears in shallow copy, not deep copy.

## Q91
Output: `(1, [2, 3, 8])` then `(1, [2, 3])`
Reason: Same shallow vs deep behavior with nested mutable data.

## Q92
Output: `{4: 'float-like'}` then `1`
Reason: `4` and `4.0` hash and compare equal.

## Q93
Output: `[4, 8]` then `12`
Reason: Only even values are 4 and 8.

## Q94
Output: `Y 11`
Reason: Pattern `(0, y)` matches first.

## Q95
Answer: `B`
Reason: Dict views are dynamic/live.

## Q96
Answer: `B`
Reason: Intersection `&` has higher precedence than union `|`.

## Q97
Answer: `B`
Reason: Dict keys must be hashable; all tuple elements must be hashable.

## Q98
Answer: `B`
Reason: `collections.Counter` is purpose-built for frequencies.

## Q99
Answer: `B`
Reason: `zip` stops at shortest iterable.

## Q100
Answer: `B`
Reason: `sorted` returns a new list and keeps original unchanged.
