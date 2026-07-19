# 07 - shadcn/ui Customization, Registry, Upgrades, and Testing

## Customize at the Right Level

1. Theme tokens for global design decisions.
2. Variant for supported component choice.
3. Domain composition for product behavior.
4. Primitive source edit only for a shared low-level contract.

## Registry

A custom registry distributes owned components/configuration across projects. Treat it as source distribution with versioning, documentation, dependency metadata, and security review.

```powershell
npx shadcn@latest add https://registry.example.com/r/course-card.json
# Result: CLI fetches registry definition and adds its source/dependencies; review remote source before use.
```

## Upgrades

Generated files do not magically update. For an upgrade:

1. Read release/migration notes.
2. Generate the new component in a temporary branch/path.
3. Diff against local source.
4. Preserve intentional custom API/accessibility.
5. Run type, unit, interaction, visual, accessibility, and build tests.
6. Remove obsolete dependencies/classes.

Never overwrite customized primitives blindly.

## Testing Components

```tsx
test("opens and closes delete dialog", async () => {
  const user = userEvent.setup();
  render(<DeleteCourseDialog />);
  await user.click(screen.getByRole("button", { name: /delete course/i }));
  expect(screen.getByRole("dialog", { name: /delete course/i })).toBeInTheDocument();
  await user.keyboard("{Escape}");
  expect(screen.queryByRole("dialog")).not.toBeInTheDocument();
});
// Test output: passes when labelled dialog opens and Escape closes it.
```

Test behavior/roles, variant contracts, consumer class merge, pending/disabled/error, focus restoration, and actual target browsers.

## Supply Chain

Review CLI/registry source, pin/lock dependencies, verify package integrity, scan dependencies, and understand primitive/icon/form/table packages added by each component.
