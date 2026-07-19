# 12 - React Accessibility, Security, and Error Boundaries

## Accessibility Is HTML First

React uses HTML semantics. Choose native controls, labels, landmarks, headings, focus order, names, states, and keyboard behavior before ARIA/custom widgets.

```tsx
function Toggle({ pressed, onChange }: { pressed: boolean; onChange(value: boolean): void }) {
  return <button type="button" aria-pressed={pressed} onClick={() => onChange(!pressed)}>{pressed ? "Enabled" : "Disabled"}</button>;
}
// Accessibility result: real button supports keyboard and exposes toggle state.
```

## Focus Management

Move focus for route changes, opened dialogs, errors, or removed focused items only when it improves logical interaction. Restore focus after modal closure. Use tested headless primitives for complex widgets.

## XSS

React escapes rendered strings:

```tsx
const untrusted = "<img src=x onerror=alert(1)>";
return <p>{untrusted}</p>;
// Browser result: literal text, not an executed image/script.
```

`dangerouslySetInnerHTML` bypasses this protection. Use only with content sanitized by a proven policy. Validate URLs and do not trust component props merely because TypeScript typed them.

## Authentication and Authorization

Client guards improve UX but do not secure data/actions. Server/API must authenticate and authorize every request and resource ownership.

## Error Boundaries

Error boundaries catch rendering/lifecycle failures below them and show fallback UI. They do not catch ordinary event-handler errors, most async callbacks, server errors, or errors inside themselves.

```tsx
<ErrorBoundary fallback={<p role="alert">This section could not load.</p>}>
  <CourseDetails />
</ErrorBoundary>
// Browser result after descendant render failure: localized accessible fallback instead of losing the whole page.
```

Use route/feature boundaries, report safe diagnostics, and provide retry/navigation where meaningful.

## Security Checklist

- runtime-validate APIs/storage/URL data
- protect secrets outside client bundle
- avoid unsafe HTML and dynamic script/code
- safe redirect/URL allow-lists
- CSRF protection for cookie-authenticated commands
- CSP and dependency governance
- no tokens/personal data in logs/analytics/errors
- third-party components/scripts reviewed as supply-chain code
