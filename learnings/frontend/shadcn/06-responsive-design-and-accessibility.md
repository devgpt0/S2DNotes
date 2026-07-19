# 06 - shadcn/ui Responsive Design and Accessibility

## Responsive Composition

```tsx
function CourseFilters() {
  return <><div className="hidden lg:block"><Filters /></div>
    <Sheet><SheetTrigger asChild><Button className="lg:hidden">Filters</Button></SheetTrigger><SheetContent><SheetTitle>Filter courses</SheetTitle><Filters /></SheetContent></Sheet></>;
}
// Browser result: desktop sidebar trigger content or mobile filter sheet based on viewport.
```

If both versions mount, duplicated form IDs/state can cause issues. Consider one adaptive structure or shared state with unique IDs.

## Accessibility Preservation

Headless primitives supply much behavior, but composition can break it:

- missing DialogTitle/Description
- `asChild` child that drops props/ref
- icon button without name
- incorrect menu vs navigation role
- focus outline removed by classes
- state visually changes but ARIA/data state is stale
- portal content outside expected provider/style scope

## Icon Button

```tsx
<Button variant="ghost" size="icon" aria-label="Delete React course"><Trash2 aria-hidden="true" /></Button>
// Accessibility result: button name is explicit and decorative icon is ignored.
```

## Responsive Data UI

- cards for small summaries, table for real relationships
- horizontal table scroll for dense data
- keep row actions keyboard reachable
- preserve headers/selection state
- server-side pagination/filtering for large datasets
- test 200% zoom and long localization

## Testing Matrix

Keyboard, Escape, focus return, screen-reader names/descriptions, touch, small/large viewport, zoom, dark mode, reduced motion, high contrast, RTL, form errors, and portal stacking.

## Browser Performance

Complex primitives add portals/listeners/layout measurements. Render on demand, avoid hundreds of mounted tooltips/popovers, profile large tables/command lists, and keep client component boundaries intentional in server-rendered frameworks.
