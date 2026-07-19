# 02 - Composition, Variants, Class Merging, and Source Ownership

## Compose, Do Not Wrap Blindly

Create domain components that use UI primitives while keeping semantic APIs.

```tsx
type EnrollButtonProps = { courseId: string; onEnroll(id: string): void };
function EnrollButton({ courseId, onEnroll }: EnrollButtonProps) {
  return <Button onClick={() => onEnroll(courseId)}>Enroll</Button>;
}
// Browser result: domain-named action built from the shared Button primitive.
```

## Variants

Generated components commonly use a variant utility such as class-variance-authority.

```tsx
const badgeVariants = cva("inline-flex rounded-full px-2 py-1 text-xs font-medium", {
  variants: {
    tone: { success: "bg-green-100 text-green-900", warning: "bg-amber-100 text-amber-950" },
  },
  defaultVariants: { tone: "success" },
});
console.log(badgeVariants({ tone: "warning" }));
// Console output includes base badge classes and warning tone classes.
```

Variants should represent supported design-system choices, not expose every CSS property as a prop.

## Preserve Native Props

```tsx
type IconButtonProps = ComponentProps<typeof Button> & { label: string };
function IconButton({ label, children, ...props }: IconButtonProps) {
  return <Button size="icon" aria-label={label} {...props}>{children}</Button>;
}
// Accessibility result: icon-only button has an accessible name and preserves Button props/ref behavior.
```

## `asChild` / Slot Composition

Some primitives let a child element receive behavior/styles without adding another DOM element.

```tsx
<Button asChild><a href="/courses">Browse courses</a></Button>
// Browser result: styled link remains a link; no nested button/link invalid markup.
```

The child must accept passed props/ref and remain semantically correct.

## Source Ownership Rules

- record why local generated source changed
- keep accessibility behavior intact
- avoid editing every primitive for one feature
- place product styling in domain components when appropriate
- test consumer overrides and variants
- upgrade by reviewing diffs, never blindly overwrite
- remove unused generated components/dependencies

## Class Merge Contract

Consumer `className` commonly comes last through `cn`, but conflict resolution follows Tailwind merge knowledge and CSS generation. Document whether consumers may override layout, color, or only placement.
