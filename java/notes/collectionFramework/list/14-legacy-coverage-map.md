# 14 - Legacy Coverage Map

This file maps old notes to unified notes so legacy files can be deleted safely.

## 1) `ArrayListNotes.md` Coverage

- core idea + complexity -> `02-arraylist-core.md`
- iteration patterns -> `06-list-iteration-patterns.md`
- method behaviors (`in-place`, `read`, `view/new`) -> `02-arraylist-core.md`
- sorting examples -> `07-sorting-searching-and-binarysearch.md`
- immutable/mutable conversion -> `02-arraylist-core.md`, `09-immutability-and-defensive-copy.md`
- `Arrays.asList` behavior -> `02-arraylist-core.md`, `09-immutability-and-defensive-copy.md`
- declarations/raw type warning -> `02-arraylist-core.md`, `11-common-bugs-and-best-practices.md`
- size vs capacity, `ensureCapacity`, `trimToSize` -> `02-arraylist-core.md`
- Java 21 first/last methods complexity -> `02-arraylist-core.md`

## 2) `LinkedListNotes.md` Coverage

- doubly linked node concept -> `03-linkedlist-core.md`
- complexity and usage guidance -> `03-linkedlist-core.md`
- all common methods + occurrences -> `03-linkedlist-core.md`
- quick construction with `Arrays.asList` -> `03-linkedlist-core.md`
- `removeAll` example -> `03-linkedlist-core.md`
- in-place vs new object -> `03-linkedlist-core.md`

## 3) `VectorListNotes.md` Coverage

- vector properties, complexity, methods -> `04-vector-and-stack-core.md`
- Java 21 list additions -> `04-vector-and-stack-core.md`
- `reversed()` view behavior -> `04-vector-and-stack-core.md`
- capacity behavior and constructors -> `04-vector-and-stack-core.md`
- thread-safety caveats + concurrent example -> `04-vector-and-stack-core.md`

## 4) `StackNotes.md` Coverage

- LIFO concept + Stack APIs (`push/pop/peek/search`) -> `04-vector-and-stack-core.md`
- method behavior and complexity -> `04-vector-and-stack-core.md`
- LinkedList/ArrayList as stack patterns -> `04-vector-and-stack-core.md`
- modern `ArrayDeque` recommendation -> `04-vector-and-stack-core.md`
- common mistakes and import correction -> `04-vector-and-stack-core.md`

## 5) `CopyOnWriteArrayListNotes.md` Coverage

- why it exists vs ArrayList/LinkedList/Vector -> `05-copyonwritearraylist-core.md`
- copy-on-write internals and costs -> `05-copyonwritearraylist-core.md`
- iterator snapshot behavior and caveats -> `05-copyonwritearraylist-core.md`
- in-place vs copy/view methods -> `05-copyonwritearraylist-core.md`
- Java 21 method support + complexities -> `05-copyonwritearraylist-core.md`
- concurrent demo + common mistakes -> `05-copyonwritearraylist-core.md`

## 6) `ComparatorsAndComparablesNotes.md` Coverage

- difference table + when to use -> `13-comparable-vs-comparator.md`
- corrected beginner snippet -> `13-comparable-vs-comparator.md`
- complete comparable/comparator examples -> `13-comparable-vs-comparator.md`
- compare contract, comparator utilities, chaining/reversal -> `13-comparable-vs-comparator.md`
- sorting APIs, comparator contract, mistakes, practice tasks -> `13-comparable-vs-comparator.md`
