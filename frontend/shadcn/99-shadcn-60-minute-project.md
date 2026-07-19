# shadcn/ui 60-Minute Project - Course Management Dashboard

## Goal

Build a small dashboard using Card, Button, Input, Badge, Table, Dialog, Sheet, form validation, Sonner toast, theme tokens, responsive composition, and accessible testing.

## Time Box

- 0-8 min: initialize/add components
- 8-18 min: theme and dashboard shell
- 18-32 min: course cards/table
- 32-45 min: create-course dialog/form
- 45-52 min: responsive filter Sheet
- 52-57 min: pending/error/toast states
- 57-60 min: keyboard/test/build audit

## Step 1: Add Components

```powershell
npx shadcn@latest add button card input label badge table dialog sheet field sonner
# Result: project-owned source and dependencies for the dashboard are added.
```

Review generated diff.

## Step 2: Responsive Dashboard

```tsx
function Dashboard({ courses }: { courses: readonly Course[] }) {
  return <main className="mx-auto max-w-6xl space-y-6 p-4 sm:p-6"><header className="flex flex-wrap items-center gap-3"><div><h1 className="text-2xl font-bold">Courses</h1><p className="text-muted-foreground">Manage learning content.</p></div><CreateCourseDialog /></header>
    <section className="grid grid-cols-[repeat(auto-fit,minmax(min(100%,16rem),1fr))] gap-4">{courses.map(course => <CourseCard key={course.id} course={course} />)}</section></main>;
}
// Browser result: semantic responsive dashboard with stable course cards and create action.
```

## Step 3: Domain Card

```tsx
function CourseCard({ course }: { course: Course }) {
  return <Card><CardHeader><CardTitle>{course.title}</CardTitle><CardDescription>{course.description}</CardDescription></CardHeader>
    <CardContent><StatusBadge status={course.status}>{course.status}</StatusBadge></CardContent>
    <CardFooter><Button asChild variant="outline"><a href={`/courses/${course.id}`}>Open course</a></Button></CardFooter></Card>;
}
// Browser result: themed course card with typed status and semantically correct navigation link.
```

## Step 4: Create Dialog/Form

Use DialogTitle/Description, labelled fields, Zod schema, React Hook Form, pending button, server error mapping, and focus restoration.

```tsx
async function submit(values: CourseInput) {
  try { await api.createCourse(values); toast.success("Course created"); setOpen(false); }
  catch (error) { toast.error("Could not create course"); }
}
// Browser result: successful save closes dialog and announces toast; failure keeps form and shows safe error.
```

Do not use toast as the only field-error location.

## Step 5: Responsive Filters

Render one controlled filter state through a desktop panel and small-screen Sheet. Ensure unique IDs and do not mount duplicate active form controls unnecessarily.

## Step 6: Test

```tsx
test("creates course from dialog", async () => {
  const user = userEvent.setup();
  render(<Dashboard courses={[]} />);
  await user.click(screen.getByRole("button", { name: /create course/i }));
  await user.type(screen.getByLabelText(/title/i), "React Basics");
  await user.click(screen.getByRole("button", { name: /save/i }));
  expect(await screen.findByText(/course created/i)).toBeInTheDocument();
});
// Test output: passes when dialog form saves and announces success.
```

## Interview Review

Explain copied-source ownership, components.json, cn/twMerge, CVA variants, asChild/ref forwarding, token theming, primitive accessibility, form/server validation, responsive Dialog/Sheet, registry/upgrades, and testing through roles.

## Completion Definition

Generated source reviewed, domain components separate, keyboard/dialog focus works, form/server errors handled, small/large layouts usable, dark contrast tested, no unsafe variant strings, test/type/build pass, and upgrade ownership documented.
