# 05 - Dialogs, Sheets, Menus, Tables, Command, and Toast

## Dialog

```tsx
<Dialog><DialogTrigger asChild><Button>Delete</Button></DialogTrigger>
  <DialogContent><DialogHeader><DialogTitle>Delete course?</DialogTitle><DialogDescription>This cannot be undone.</DialogDescription></DialogHeader>
    <DialogFooter><DialogClose asChild><Button variant="outline">Cancel</Button></DialogClose><Button variant="destructive">Delete</Button></DialogFooter>
  </DialogContent>
</Dialog>
// Browser result: labelled modal interaction with trigger, description, actions, and primitive-managed focus behavior.
```

Keep destructive confirmation explicit; do not put a complete page workflow in a modal.

## Sheet for Responsive Secondary UI

Use a Sheet for navigation/filters on small screens while rendering the same semantic controls in a sidebar on wide screens. Do not render duplicate active controls with conflicting IDs/state.

## Dropdown/Menu

Menus represent action choices, not site navigation or arbitrary form content. Ensure actions have names, destructive separation, keyboard behavior, and disabled semantics.

## Data Table

shadcn provides table presentation, not a complete data-grid engine. Add sorting/filtering/pagination/selection through explicit state or a table library when justified.

```tsx
<Table><TableHeader><TableRow><TableHead scope="col">Course</TableHead><TableHead scope="col">Status</TableHead></TableRow></TableHeader>
  <TableBody>{courses.map(course => <TableRow key={course.id}><TableCell>{course.title}</TableCell><TableCell>{course.status}</TableCell></TableRow>)}</TableBody></Table>
// Browser result: semantic table with stable keyed rows.
```

## Command Palette

Command components support searchable actions. Provide meaningful groups, empty state, keyboard shortcut discoverability, and authorization before executing actions.

## Toast/Sonner

Toasts are for brief noncritical confirmation. Errors requiring action belong near the failed task/form. Do not use toast as the only announcement for critical state.

## Popover/Tooltip

Tooltip provides supplementary text, not essential content or interactive controls. Popover owns richer interaction and must handle focus/dismissal.
