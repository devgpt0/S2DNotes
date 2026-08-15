# Focus300 276: LeetCode 223 - Rectangle Area

**Source:** [LeetCode 223](https://leetcode.com/problems/rectangle-area/)  
**Difficulty:** Easy  
**Pattern:** overlap arithmetic

## Exact contract

Return the union area of two axis-aligned rectangles.

## First principles

The total area is the sum of the two rectangles minus any overlap counted twice. Detecting the overlap reduces the problem to a small piece of geometry.

## Cases that decide correctness

- Disjoint rectangles have zero overlap.
- Touching edges do not create overlap area.
- One rectangle can fully contain the other.
- Coordinates may be ordered so width and height are computed with `max` and `min`.

## Brute force

```python
def compute_area_brute(ax1, ay1, ax2, ay2, bx1, by1, bx2, by2):
    overlap = max(0, min(ax2, bx2) - max(ax1, bx1)) * max(0, min(ay2, by2) - max(ay1, by1))
    return (ax2 - ax1) * (ay2 - ay1) + (bx2 - bx1) * (by2 - by1) - overlap
```

Rasterize the plane and count covered cells.

## Better insight

Compute each rectangle's area and subtract the intersection area if one exists.

## Expert solution

```python
def compute_area(ax1, ay1, ax2, ay2, bx1, by1, bx2, by2):
    overlap = max(0, min(ax2, bx2) - max(ax1, bx1)) * max(0, min(ay2, by2) - max(ay1, by1))
    return (ax2 - ax1) * (ay2 - ay1) + (bx2 - bx1) * (by2 - by1) - overlap
```

Calculate the overlap width and height from coordinate intersections, then combine the inclusion-exclusion terms.

**Complexity:** O(1) time and O(1) space.
