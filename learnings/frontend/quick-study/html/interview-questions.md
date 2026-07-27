# HTML: 10 most-asked interview questions

## 1. What is semantic HTML, and why does it matter?

Semantic tags describe purpose: `nav`, `main`, `article`, `button`, and `table`. They make code easier to maintain and give browsers, search engines, keyboards, and assistive technology useful built-in meaning and behavior.

## 2. What is the difference between `div` and `span`?

Both are neutral containers. A `div` is block-level by default; a `span` is inline by default. Use them only when no meaningful element fits, commonly as styling or scripting hooks.

## 3. What is the difference between `id` and `class`?

An `id` uniquely identifies one document element and supports labels, fragments, and DOM lookup. A class may be reused across elements and is the normal CSS styling hook. Duplicate IDs are invalid and harm accessibility.

## 4. When should you use a link versus a button?

Use a link to navigate to a URL. Use a button to perform an action such as submitting, opening, or deleting. Native elements provide correct keyboard and accessibility behavior.

## 5. How do you make an image accessible?

Write `alt` text that communicates the image’s purpose in context. Use `alt=""` for decoration so assistive technology ignores it. Provide a nearby explanation for complex charts and avoid repeating an adjacent caption.

## 6. How do you make a form accessible?

Give every control a visible label, use the correct input type, group related controls with `fieldset`/`legend`, preserve keyboard focus, and connect clear errors to their fields. Placeholder text does not replace a label.

## 7. What is the difference between GET and POST forms?

GET encodes data in the URL and is appropriate for safe, repeatable reads such as search. POST sends data in the body and is appropriate for state changes or larger/sensitive payloads. Both require HTTPS and server validation.

## 8. What are `async` and `defer` on scripts?

Both download without blocking HTML parsing. `defer` executes after parsing in document order. `async` executes as soon as each script downloads, so order is not guaranteed; it suits independent scripts.

## 9. What is ARIA, and when should it be used?

ARIA supplies accessibility semantics when native HTML cannot. It does not add keyboard behavior, focus management, or styling. Prefer a native element first; incorrect ARIA can make an interface worse.

## 10. How do you improve HTML performance and security?

Use responsive images, dimensions, appropriate lazy loading, deferred scripts, and a small DOM. Treat external data as untrusted, avoid unsafe HTML injection, sandbox iframes, use HTTPS and Content Security Policy, and validate all server input.
