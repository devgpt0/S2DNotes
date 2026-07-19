# 10 - React Performance and Profiling

## Start with Measurement

React performance problems often come from large component trees, expensive calculations, unstable props, over-broad context, excessive effects, huge DOM, or slow browser/network work.

Use React DevTools Profiler and browser Performance panel before adding memoization.

## Memoize Expensive Calculation

```tsx
const visibleCourses = useMemo(
  () => expensiveFilter(courses, query),
  [courses, query],
);
// Result: recalculates only when courses or query identity/value changes; useful only when calculation cost justifies it.
```

## Stable Callback

```tsx
const handleSelect = useCallback((id: string) => setSelectedId(id), []);
// Result: stable function identity can help a memoized child avoid rerender; it does not make the callback execution faster.
```

Do not wrap everything. Memoization adds comparison, memory, dependencies, and readability cost. Modern React compiler/tooling may automate some memoization in supported setups; profile the actual build.

## `memo`

```tsx
const CourseRow = memo(function CourseRow({ course, onSelect }: Props) {
  return <button onClick={() => onSelect(course.id)}>{course.title}</button>;
});
// Result: React may skip rerender when props are shallowly equal.
```

One new object/function prop defeats shallow equality. Fix data ownership before custom deep comparisons.

## List Performance

- stable keys
- paginate/virtualize genuinely large lists
- avoid mounting hidden heavy subtrees
- keep row state local when possible
- do not perform O(n²) lookups during each render
- normalize/index data when repeated keyed access matters

## Context Performance

Split context by update frequency/responsibility. Memoize provider values when identity stability is needed, but avoid premature global context.

## Code Loading

Use route/feature-level lazy loading for meaningful boundaries. Too many tiny chunks increase request/coordination overhead.

## Browser Work Still Matters

React optimization cannot fix oversized images, slow fonts, layout thrashing, expensive CSS paint, massive JavaScript, or slow APIs. Measure end-to-end Core Web Vitals and interactions.
