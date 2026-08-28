# 64. Process Tasks by Priority

**What you learn:** Java queue questions APIs and problem solving.

## Problem

Process tasks from highest priority to lowest, preserving tie order.

## Example

~~~text
Input: tasks=[build:2,test:3,docs:1]
Output: [test, build, docs]
~~~

## Simple idea

Compose a reversed priority comparator with an input-order tie breaker.

## Java solution

~~~java
record Task(String name, int priority, int order) {}
static ArrayList<String> process(List<Task> tasks) {
    Queue<Task> queue = new PriorityQueue<>(
        Comparator.comparingInt(Task::priority).reversed().thenComparingInt(Task::order));
    queue.addAll(tasks); ArrayList<String> result = new ArrayList<>();
    while (!queue.isEmpty()) result.add(queue.poll().name());
    return result;
}
~~~

## Complexity

- Time: `O(n log n)`
- Extra space: `O(n)`

Try to write the solution yourself before reading the code.

