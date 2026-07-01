# 10 - Performance and Memory (List Deep Dive)

## 1) Performance Starts with Correct Data Structure

No list type is universally fastest.

Pick by workload:

- heavy random reads: `ArrayList`
- head/tail deque operations: `LinkedList` or often `ArrayDeque` for pure deque
- concurrent read-heavy snapshots: `CopyOnWriteArrayList`

## 2) Complexity Comparison

| Operation | ArrayList | LinkedList | CopyOnWriteArrayList |
|---|---|---|---|
| `get(i)` | `O(1)` | `O(n)` | `O(1)` |
| append `add(e)` | amortized `O(1)` | `O(1)` | `O(n)` |
| `add(0, e)` | `O(n)` | `O(1)` | `O(n)` |
| `remove(i)` | `O(n)` shift | `O(n)` traversal | `O(n)` |
| iteration | cache-friendly | pointer chasing | snapshot-friendly |

## 3) CPU Cache Locality

`ArrayList` stores elements in contiguous memory references.

Benefits:

- better cache locality
- faster sequential iteration in many real workloads

`LinkedList` jumps through node objects, which can hurt cache performance.

## 4) Memory Overhead

### `ArrayList`

- one backing object array
- usually lower overhead per element

### `LinkedList`

- each element wrapped in node object (`prev`, `next`, value)
- significantly higher overhead for large lists

### `CopyOnWriteArrayList`

- frequent new array allocations on each write
- can create GC pressure under write-heavy workloads

## 5) Resize Behavior in `ArrayList`

Concept taught: Demonstrates 5) Resize Behavior in `ArrayList` in practice.

```java
ArrayList<Integer> list = new ArrayList<>(2);
for (int i = 1; i <= 5; i++) list.add(i);
System.out.println(list);
```

Output:

```text
[1, 2, 3, 4, 5]
```

Behind the scenes, internal array resized multiple times.

Optimization for large bulk load:

Concept taught: Demonstrates 5) Resize Behavior in `ArrayList` in practice.

```java
ArrayList<Integer> big = new ArrayList<>(1_000_000);
```

## 6) Bulk Operations Are Often Better

Concept taught: Demonstrates 6) Bulk Operations Are Often Better in practice.

```java
List<Integer> nums = new ArrayList<>(List.of(1, -2, 3, -4, 5));
nums.removeIf(n -> n < 0);
nums.addAll(List.of(6, 7, 8));
System.out.println(nums);
```

Expected output:

```text
[1, 3, 5, 6, 7, 8]
```

Benefits:

- cleaner code
- library-level optimizations

## 7) Boxing/Unboxing Cost

`List<Integer>` stores objects, not primitives.

Effects in tight numeric loops:

- autoboxing allocation/overhead
- more memory than primitive arrays

For very numeric-heavy performance paths, primitive arrays or specialized libs can be faster.

## 8) `contains` in Hot Paths

Concept taught: Demonstrates 8) `contains` in Hot Paths in practice.

```java
List<Integer> list = new ArrayList<>();
for (int i = 0; i < 1_000_000; i++) list.add(i);
System.out.println(list.contains(999_999));
```

Output:

```text
true
```

But `contains` is linear scan.

If frequent membership checks dominate, use `HashSet`.

## 9) `subList` and Memory/Structure Considerations

`subList` is a view:

- lightweight creation
- tied to parent structural modifications

If long-lived independent list needed, copy it:

Concept taught: Demonstrates 9) `subList` and Memory/Structure Considerations in practice.

```java
List<Integer> copy = new ArrayList<>(bigList.subList(100, 200));
```

## 10) Concurrency Performance Notes

- `Vector`: synchronization overhead on each call
- `Collections.synchronizedList`: wrapper-level locking, still needs external lock for iteration consistency
- `CopyOnWriteArrayList`: great read scalability, expensive writes

## 11) Measure, Do Not Guess

Avoid naive `System.nanoTime` loops for serious benchmarking.

Use JMH for reliable microbenchmarks:

- warmup
- JIT stabilization
- dead-code elimination protection

## 12) Quick Selection Checklist

- Need random access + general purpose -> `ArrayList`
- Need frequent two-end deque ops -> `ArrayDeque` or `LinkedList`
- Need safe concurrent iteration with rare writes -> `CopyOnWriteArrayList`
- Need fastest contains lookups -> maybe not a list; choose `Set`

## 13) Summary

Performance is workload-driven. For most applications, a pre-sized `ArrayList` plus good API usage gives excellent real-world results.
