# 03 - Conditional Rendering, Lists, Keys, and Composition

## Conditions

```tsx
function Status({ loading, error }: { loading: boolean; error?: string }) {
  if (loading) return <p>Loading…</p>;
  if (error) return <p role="alert">{error}</p>;
  return <p>Ready</p>;
}
// Browser result: exactly one loading, error, or ready state is rendered.
```

Use early returns for major states and ternary/`&&` for small branches. Remember `0 && <Thing />` renders `0`; use an explicit boolean condition.

## Lists and Stable Keys

```tsx
type Course = { id: string; title: string };
function CourseList({ courses }: { courses: readonly Course[] }) {
  return <ul>{courses.map(course => <li key={course.id}>{course.title}</li>)}</ul>;
}
// Browser result: one list item per course; id preserves sibling identity across updates.
```

Keys must be stable and unique among siblings. Avoid array index when items can insert, delete, or reorder. Never generate random keys during render; they remount stateful children every time.

## Key Controls State Identity

Changing a component's key tells React it is a different instance, resetting its state.

```tsx
<CourseEditor key={selectedCourseId} courseId={selectedCourseId} />
// Behavior: selecting another ID remounts editor and resets its local state.
```

Use intentionally, not to hide state synchronization bugs.

## Composition

```tsx
type DialogLayoutProps = { heading: string; body: ReactNode; actions: ReactNode };
function DialogLayout({ heading, body, actions }: DialogLayoutProps) {
  return <div role="dialog" aria-labelledby="dialog-heading"><h2 id="dialog-heading">{heading}</h2>{body}<footer>{actions}</footer></div>;
}
// Browser result: caller composes body/actions into one accessible dialog layout.
```

Prefer slots/children and focused components over inheritance.

## Avoid Premature Component Extraction

Extract when a piece has a clear name/responsibility, is reused, owns state/effects, or makes testing/reading easier. A component that merely renames one `div` may add noise.
