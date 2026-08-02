# Simple DSA Glossary

| Word | Simple meaning |
| --- | --- |
| algorithm | exact steps that turn input into the required output |
| data structure | a way to store data so chosen operations are fast |
| index | a position; arrays normally start at index `0` |
| contiguous | next to each other with no gaps |
| subsequence | keeps order but may skip values |
| prefix | a beginning part |
| suffix | an ending part |
| state | the minimum remembered information needed to continue |
| invariant | a fact that remains true throughout an algorithm |
| brute force | direct method that tries every valid possibility |
| optimize | remove repeated/unnecessary work without changing the answer |
| stable sort | equal keys keep their earlier relative order |
| monotone | moves in only one direction, such as false then true |
| vertex/node | one object in a graph |
| edge | a connection between two graph vertices |
| path | a sequence of connected vertices/edges |
| component | a maximal group connected to one another |
| relax an edge | improve a known path using that edge |
| tree | connected graph with no cycle |
| root | chosen starting/top vertex of a tree |
| ancestor | a vertex above another vertex in a rooted tree |
| leaf | tree vertex with no children |
| memoization | save recursive state answers so they are computed once |
| tabulation | compute DP states in an order that has dependencies ready |
| modulo | remainder after division |
| amortized | average cost across a whole sequence of operations |
| auxiliary space | extra memory excluding input and usually output |

## Complexity in simple words

```text
O(1)       same amount of work
O(log n)   repeatedly cut the remaining work in half
O(n)       visit input once
O(n log n) efficient general sorting / divide and conquer
O(n^2)     inspect most pairs
O(2^n)     inspect most subsets
O(n!)      inspect most orders
```

When a note uses a word not listed here, read its board example first. The
example should give the word a concrete meaning before the formal definition.
