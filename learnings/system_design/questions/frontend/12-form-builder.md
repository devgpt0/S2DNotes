# Design a Dynamic Form Builder Frontend

> **Difficulty:** Hard  
> **Main focus:** schema, validation, versioning

## Interview prompt

Design a no-code form builder and renderer with conditional logic, drafts, and safe publication.

## 1. Clarify the experience

**What I would say first:** The form definition is versioned data interpreted by a restricted renderer. I will avoid executable user code and define deterministic validation and conditional rules.

### Functional requirements

- Drag fields into sections and configure labels, validation, and choices.
- Add conditional visibility and branching.
- Preview, publish immutable versions, collect responses, and edit drafts.
- Support localization, accessibility, and large forms.

### Browser and product constraints

- Published responses must remain interpretable after the draft changes.
- Conditional rules can form cycles or reference deleted fields.
- Arbitrary HTML or JavaScript is unsafe.

## 2. State and API contracts

- FormSchema {formId, version, fields, layout, rules, locales}
- POST /v1/forms/{id}/versions validates and publishes one immutable schema
- POST /v1/forms/{id}/responses {schemaVersion, answers, submissionId}

## 3. Frontend architecture

```text
builder UI -> normalized draft store -> command/undo stack
     |                 |
     |                 +-> rule graph validator
     +-> component palette / property panel / preview renderer
                              |
                     schema validation API -> version store

runtime form -> schema interpreter -> field registry -> response API
```

## 4. Critical user flow

1. Builder commands modify a normalized field map and ordered layout IDs.
2. Rule graph validates references, types, and cycles after each structural change.
3. Preview uses the same renderer and validation engine as production.
4. Publish sends canonical schema; the server validates and creates an immutable version.
5. Responses include schema version and idempotent submission ID.

## 5. Deep dive

- Use a declarative expression language with an allowlisted operator set, not eval.
- Field IDs remain stable across label changes; deleting referenced fields requires rule repair.
- Compute conditional dependencies so only affected fields re-evaluate.
- Large forms render sections progressively but preserve validation summaries and focus.

## 6. Performance, resilience, and observability

- Normalize schema state so editing one field does not rerender every field.
- Lazy-load uncommon field types and virtualize very large builder canvases.
- Autosave debounces versioned patches and clearly displays unsaved state.
- Track publish validation failures, draft recovery, render time, rule evaluation, and response completion.

## 7. Security and accessibility

- Escape labels and help text, sanitize restricted rich text, and isolate file uploads.
- Authorize builder and response access separately; minimize sensitive answers in browser logs.
- Generated forms require labels, descriptions, error association, logical focus order, and keyboard operation.

## 8. Trade-offs

| Choice | Consequence |
|---|---|
| Arbitrary custom code | Maximum flexibility with severe security and support risk. |
| Declarative schema | Safe and portable with bounded expressiveness. |
| Mutable published form | Easy edits but ambiguous old responses. |
| Immutable versions | Clear history and migration work. |

## 9. 60-second interview summary

A normalized builder emits a declarative versioned schema, with graph validation for conditional rules and one shared preview/runtime interpreter. Published versions are immutable, responses record the schema version, and no user-supplied executable code enters the renderer.

## Likely follow-up questions

- What state belongs in the URL, local UI, server cache, or durable local storage?
- What happens on a slow device with a flaky network?
- How do loading, empty, stale, partial-error, and retry states appear?
- Which Core Web Vital or product metric would reveal a bad release?

