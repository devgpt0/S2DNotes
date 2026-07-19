# 03 - shadcn/ui Forms, Validation, and Server Errors

## Layers

- semantic HTML names/labels/constraints
- client schema and interaction state
- server validation as authority
- domain component using shadcn controls

## Schema

```tsx
const courseSchema = z.object({
  title: z.string().min(2).max(120),
  price: z.coerce.number().positive(),
  level: z.enum(["beginner", "intermediate", "advanced"]),
});
type CourseInput = z.infer<typeof courseSchema>;
console.log(courseSchema.safeParse({ title: "React", price: "999", level: "beginner" }).success);
// Console output: true; note that z.coerce intentionally converts the price string.
```

Use coercion only when the boundary contract intentionally accepts string form values.

## React Hook Form Integration

```tsx
const form = useForm<CourseInput>({ resolver: zodResolver(courseSchema), defaultValues: { title: "", price: 0, level: "beginner" } });
function submit(values: CourseInput) { console.log(values); }
return <form onSubmit={form.handleSubmit(submit)} noValidate>
  <Field><FieldLabel htmlFor="title">Title</FieldLabel><Input id="title" {...form.register("title")} />
    {form.formState.errors.title && <FieldError>{form.formState.errors.title.message}</FieldError>}</Field>
  <Button type="submit" disabled={form.formState.isSubmitting}>Save</Button>
</form>;
// Browser result: labelled validated title control; valid submit prints typed CourseInput.
```

Exact form component APIs vary with the generated shadcn version. Read owned source.

## Server Errors

Map server field errors to controls and put non-field failures in an alert/error summary. Client validation can become stale and must not replace server checks.

```tsx
try { await saveCourse(values); }
catch (error) {
  if (error instanceof DuplicateTitleError) form.setError("title", { message: "A course with this title already exists." }, { shouldFocus: true });
  else form.setError("root", { message: "Could not save. Try again." });
}
// Browser result: known duplicate focuses title; unknown safe message appears at form level.
```

## Form Expert Checklist

Stable IDs/names, visible labels, help/error associations, focus on summary/first invalid control, pending state, duplicate prevention/idempotency, preserved values, server errors, keyboard/autofill/password-manager behavior, and tests with real user events.
