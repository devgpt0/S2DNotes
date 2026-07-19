# 04 - React Forms and Validation

## Controlled Input

```tsx
function NameForm() {
  const [name, setName] = useState("");
  return <form onSubmit={event => { event.preventDefault(); console.log(name); }}>
    <label>Name <input name="name" value={name} onChange={event => setName(event.currentTarget.value)} required /></label>
    <button>Save</button>
  </form>;
}
// Browser/console result: React owns input value; valid submit prints current name.
```

Controlled fields help live validation/conditional UI but rerender on change.

## Uncontrolled/FormData

```tsx
function SearchForm() {
  function submit(formData: FormData) {
    const query = formData.get("query");
    if (typeof query !== "string" || query.length === 0) throw new TypeError("query required");
    console.log(query);
  }
  return <form action={submit}><label>Search <input name="query" required /></label><button>Search</button></form>;
}
// React 19 result: form action receives FormData; valid submission prints query.
```

Use controlled state only when UI needs it. Native form behavior plus FormData can be simpler.

## Validation Layers

- HTML constraints: immediate browser feedback
- client schema/business checks: richer interaction
- server validation: authoritative security/data boundary

Do not silently trim/coerce unless business rules explicitly define normalization.

## Error Accessibility

```tsx
<label htmlFor="email">Email</label>
<input id="email" name="email" type="email" aria-invalid={Boolean(error)} aria-describedby={error ? "email-error" : undefined} />
{error && <p id="email-error" role="alert">{error}</p>}
// Accessibility result: field exposes invalid state and associated announced error.
```

## Submission State

Prevent accidental duplicate commands through pending UI plus server idempotency where needed. Disabling a button alone is not a distributed correctness guarantee.

## Form Libraries

Use a form library when complex nested fields, schemas, touched/dirty state, and reusable controls justify it. Understand native labels/names/submission/validation first.
