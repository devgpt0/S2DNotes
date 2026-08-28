# 65. Traverse a Grid with a Queue

**What you learn:** Java queue questions APIs and problem solving.

## Problem

Count cells reachable from (0,0) where 0 is open and 1 is blocked.

## Example

~~~text
Input: grid=[[0,0],[1,0]]
Output: 3
~~~

## Simple idea

Enqueue each cell once and explore four neighbors.

## Java solution

~~~java
static int reachable(int[][] grid) {
    if (grid.length == 0 || grid[0][0] == 1) return 0;
    Queue<int[]> queue = new ArrayDeque<>(); queue.offer(new int[]{0, 0}); grid[0][0] = 1;
    int count = 0; int[][] dirs = {{1,0},{-1,0},{0,1},{0,-1}};
    while (!queue.isEmpty()) {
        int[] cell = queue.poll(); count++;
        for (int[] d : dirs) {
            int r = cell[0] + d[0], c = cell[1] + d[1];
            if (r >= 0 && r < grid.length && c >= 0 && c < grid[0].length && grid[r][c] == 0) {
                grid[r][c] = 1; queue.offer(new int[]{r, c});
            }
        }
    }
    return count;
}
~~~

## Complexity

- Time: `O(rows * columns)`
- Extra space: `O(rows * columns)`

Try to write the solution yourself before reading the code.

