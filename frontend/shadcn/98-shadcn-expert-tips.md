# shadcn/ui Expert Tips and Production Code Snippets

## Expert Principles

- Treat generated components as maintained product source.
- Separate primitives from domain components.
- Customize token -> variant -> composition -> primitive, in that order.
- Preserve primitive accessibility/ref/prop contracts.
- Keep class override policy explicit.
- Diff and test upgrades.
- Remove unused generated source and dependencies.

## Expert Code Snippet: Polymorphic Domain Link

```tsx
type CourseLinkProps = ComponentProps<typeof Button> & { href: string };
function CourseLink({ href, children, ...props }: CourseLinkProps) {
  return <Button asChild {...props}><a href={href}>{children}</a></Button>;
}
// Browser result: styled native link with Button variants, avoiding invalid button-inside-link markup.
```

## Expert Code Snippet: Typed Variants

```tsx
const statusVariants = cva("inline-flex rounded-full px-2 py-1 text-xs font-medium", {
  variants: { status: { draft: "bg-slate-100 text-slate-900", published: "bg-green-100 text-green-900", archived: "bg-amber-100 text-amber-950" } },
});
type StatusBadgeProps = VariantProps<typeof statusVariants> & { children: ReactNode };
function StatusBadge({ status, children }: StatusBadgeProps) { return <span className={statusVariants({ status })}>{children}</span>; }
// Result: only supported status variants type-check and map to complete static utility strings.
```

## Expert Code Snippet: Ref-Safe Wrapper

```tsx
const SearchInput = forwardRef<HTMLInputElement, ComponentProps<typeof Input>>(
  ({ className, ...props }, ref) => <Input ref={ref} type="search" className={cn("ps-9", className)} {...props} />,
);
SearchInput.displayName = "SearchInput";
// Result: wrapper preserves native Input props/ref and allows intentional consumer class merging.
```

## Expert Code Snippet: Responsive Dialog/Drawer Decision

```tsx
function EditCourse({ open, onOpenChange }: Props) {
  const desktop = useMediaQuery("(min-width: 48rem)");
  const Root = desktop ? Dialog : Drawer;
  const Content = desktop ? DialogContent : DrawerContent;
  return <Root open={open} onOpenChange={onOpenChange}><Content><EditCourseForm /></Content></Root>;
}
// Browser result: one controlled form instance uses dialog on desktop and drawer on small screens.
```

Ensure both primitive APIs/semantics align; do not switch while open without handling focus/state.

## Expert Code Snippet: Server Error Mapping

```tsx
function applyServerErrors(errors: readonly ApiFieldError[], form: UseFormReturn<CourseInput>) {
  for (const error of errors) {
    if (error.field === "title" || error.field === "price") form.setError(error.field, { message: error.message });
    else form.setError("root", { message: "Could not save the course." });
  }
}
// Result: allow-listed server fields map safely; unknown fields become a non-field error.
```

## Production Review Checklist

Owned source reviewed, variants finite, theme contrast tested, refs/props preserved, dialogs labelled, icon controls named, forms server-validated, responsive/zoom/RTL tested, portal stacking checked, component interaction tests present, registry/dependencies governed, and upgrade diff documented.

## Source Ownership Tips

- Review generated source and dependency diffs before commit.
- Record upstream/CLI version when component provenance matters.
- Keep `components/ui` free of business API calls and feature state.
- Remove unused generated components and their dependencies.
- Make local divergences intentional and documented so upgrades can be merged rather than guessed.
- Do not wrap every primitive; add a wrapper only when it defines a stable app/design-system contract.

## Token and Variant Tips

- Customize semantic CSS tokens before changing every component class.
- Verify foreground/background contrast in light, dark, hover, focus, selected, disabled, and destructive states.
- Add variants for stable semantics, not one page's spacing preference.
- Keep CVA variant values finite and complete static Tailwind strings.
- Define a class override policy; HTML class order alone does not guarantee which Tailwind conflict wins.
- Use `asChild` only when the child element has correct semantics and can accept props/ref.

## Form Tips

- Separate HTML form coercion schema from strict API response/domain schemas.
- Set stable default values and avoid controlled/uncontrolled switching.
- Keep client validation for UX and server validation for authority.
- Allow-list server field error names before calling `setError`.
- Preserve input on server failure; close/reset dialog only after confirmed success.
- Focus/announce the first error and keep non-field errors visible.
- Prevent duplicate effects with server idempotency, not only disabled buttons.

## Overlay Tips

- Choose Dialog, AlertDialog, Sheet/Drawer, Popover, DropdownMenu, Tooltip, or route from the interaction purpose.
- Test initial focus, focus trap, Escape, outside action, scroll lock, nested overlay, and focus return.
- Do not switch Dialog/Drawer implementation while open without preserving state/focus.
- Verify portals against transformed ancestors, z-index layers, and mobile soft keyboards.
- A toast is not the correct home for critical persistent errors.

## Table and Async Tips

- Start with semantic Table; add TanStack/headless table only for required behavior.
- Server-paginate large datasets and allow-list sort/filter fields.
- Distinguish initial loading, refreshing, empty, error, stale, and success.
- Name row action buttons/menus with the entity for assistive technology.
- Keep shareable table state in URL.
- Test virtualization, sticky headers, column hiding, zoom, and screen-reader navigation before release.

## Registry and Upgrade Tips

- Treat external registry items as executable supply-chain inputs.
- Generate upgrade candidates in a scratch branch/project, then diff.
- Port upstream accessibility fixes without overwriting intentional local design behavior.
- Run type, lint, interaction, accessibility, visual, E2E, CSS-size, and bundle checks.
- Pin/verify dependencies under repository policy and audit newly introduced transitive packages.

## Browser and Testing Tips

- Test Chromium, Firefox, and WebKit/Safari focus/portal/scroll-lock behavior.
- Test touch, soft keyboard, 200% zoom, RTL, forced colors, reduced motion, autofill, and password managers.
- Query tests by role/name/label rather than generated classes or primitive implementation details.
- Use a component showcase to review every state/variant/theme when team scale justifies it.

## High-Use Responsive Domain Component

```tsx
function CourseGrid({ courses }: { courses: readonly Course[] }) {
  if (courses.length === 0) return <p>No courses found.</p>;
  return <section aria-label="Courses" className="grid grid-cols-[repeat(auto-fit,minmax(min(100%,18rem),1fr))] gap-4">
    {courses.map(course => <Card key={course.id} className="flex h-full flex-col">
      <CardHeader><CardTitle>{course.title}</CardTitle><CardDescription>{course.description}</CardDescription></CardHeader>
      <CardFooter className="mt-auto"><Button asChild variant="outline"><a href={`/courses/${encodeURIComponent(course.id)}`}>Open course</a></Button></CardFooter>
    </Card>)}
  </section>;
}
```

This composes owned primitives into a reusable domain component, uses CSS for responsiveness, preserves link semantics through `asChild`, and keeps identity stable with domain IDs.
