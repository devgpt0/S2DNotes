# 73. Build an Adjacency Map

**What you learn:** Java maps and sets APIs and problem solving.

## Problem

Add an undirected edge to Map<Integer,List<Integer>>.

## Example

~~~text
Input: edges=(1,2),(2,3)
Output: {1=[2],2=[1,3],3=[2]}
~~~

## Simple idea

Initialize each neighbor list lazily and add both directions.

## Java solution

~~~java
static void addEdge(Map<Integer, List<Integer>> graph, int first, int second) {
    graph.computeIfAbsent(first, ignored -> new ArrayList<>()).add(second);
    graph.computeIfAbsent(second, ignored -> new ArrayList<>()).add(first);
}
~~~

## Complexity

- Time: `O(n)`
- Extra space: `O(1)`

Try to write the solution yourself before reading the code.

