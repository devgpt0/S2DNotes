# HTML Expert Tips and Production Checklist

## Semantics Experts Use

- Start with the content outline before adding containers.
- Use one page-level `main`; do not put repeated site navigation inside it.
- A `section` normally deserves a heading. A styling wrapper usually remains `div`.
- Use `article` only for content that can stand independently.
- Use `address` for contact information related to its nearest article/body, not every postal address.
- Use `time datetime` for machine-readable dates.
- Keep DOM order equal to reading and keyboard order; never depend on CSS visual reordering.
- Prefer `details/summary`, `dialog`, `button`, and native form controls before recreating widgets.

## Accessibility Tricks

- Inspect the accessibility tree, not only the visual DOM.
- Every control needs an accessible name; visible text is usually best.
- Use `aria-describedby` for help/error text and `aria-invalid` after validation.
- Dynamic status that does not move focus may need a restrained live region.
- Put the error summary before a failed form and link each error to its field.
- Avoid `aria-label` when visible text already supplies a name; it can replace that text in the accessibility name.
- `title` is not a dependable label or mobile interaction.
- Test keyboard, screen reader, 200% zoom, text-only zoom, high contrast, and reduced motion.
- Use a skip link for pages with repeated navigation.
- Ensure source order remains logical when CSS Grid rearranges regions.

## Forms Experts Build

- Match `autocomplete` tokens to the real data purpose.
- Use `inputmode` to improve keyboards without changing validation semantics.
- Keep a stable `name`; it defines the submitted key.
- Group related radios/checkboxes with `fieldset` and `legend`.
- Never clear valid input after a failed submission.
- Explain format before input rather than only after failure.
- Treat browser validation as convenience and server validation as authority.
- For uploads, validate size, extension, MIME signature/content, name, storage path, and authorization server-side.

## Image and Media Performance

- Always include intrinsic width and height or an equivalent aspect ratio.
- Do not lazy-load the likely LCP image.
- Use `srcset` and accurate `sizes`; an inaccurate `sizes="100vw"` can waste bandwidth.
- Prefer responsive image services/build pipelines over manually maintaining many assets.
- Use SVG for appropriate vector art, not complex photographs.
- Provide captions/transcripts and avoid autoplay audio.
- Use `fetchpriority="high"` only for a measured critical image.

## Loading and Browser Tips

- Put critical metadata early: charset should appear within the first 1024 bytes.
- Use modules or `defer` for application scripts.
- Use `async` only for independent scripts whose execution order does not matter.
- Preload only resources discovered too late but definitely required.
- Preconnect only a few critical cross-origins.
- Version static asset URLs and send deliberate cache headers.
- Keep HTML streamable; meaningful early content improves perceived speed.
- Avoid enormous DOM trees and unnecessary wrappers.

## Security Tips

- Use CSP as defense in depth, not as a substitute for output encoding.
- Apply `rel="noopener"` to untrusted/new-tab navigation where required by target behavior.
- Sandbox untrusted iframes with the minimum tokens.
- Validate redirect targets and URL schemes.
- Never place secrets in HTML, comments, data attributes, source maps, or client bundles.
- Treat third-party scripts as code with the same page privileges.

## SEO and Sharing

- Give every indexable page a specific title, description, canonical URL, language, and useful heading.
- Make links crawlable through real `href` values.
- Structured data must match visible content.
- Return correct HTTP status codes; a pretty “not found” page with 200 harms indexing.
- Test social previews and ensure absolute share-image URLs.

## Final Expert Review

Validate markup, inspect landmarks/names, tab through controls, submit invalid forms, test without CSS/JavaScript, throttle network/CPU, inspect resource priority and Core Web Vitals, then test representative real browsers/devices.

## Expert Code Snippets Used in Production

### Accessible Native Dialog

```html
<button type="button" commandfor="confirm-dialog" command="show-modal">Delete course</button>
<dialog id="confirm-dialog" aria-labelledby="dialog-title">
  <h2 id="dialog-title">Delete course?</h2>
  <p>This action cannot be undone.</p>
  <form method="dialog"><button value="cancel">Cancel</button><button value="confirm">Delete</button></form>
</dialog>
<!-- Browser result in supporting browsers: modal dialog with native focus/escape/backdrop behavior. Provide tested fallback for support policy. -->
```

### Error Summary Linked to Fields

```html
<div role="alert" tabindex="-1" id="error-summary">
  <h2>Fix these problems</h2><a href="#email">Enter a valid email address</a>
</div>
<label for="email">Email</label>
<input id="email" name="email" type="email" aria-invalid="true" aria-describedby="email-error">
<p id="email-error">Use a format such as name@example.com.</p>
<!-- Accessibility result: summary can receive focus; link moves to field; field exposes invalid state and help. -->
```

### Responsive Preloaded Hero

```html
<link rel="preload" as="image" href="hero-1280.avif" imagesrcset="hero-640.avif 640w, hero-1280.avif 1280w" imagesizes="100vw" fetchpriority="high">
<img src="hero-1280.avif" srcset="hero-640.avif 640w, hero-1280.avif 1280w" sizes="100vw" width="1280" height="640" fetchpriority="high" alt="Students learning frontend development">
<!-- Browser result: browser can prioritize and select the correct hero candidate without layout shift. -->
```

### Secure External Link Helper Pattern

```html
<a href="https://external.example/resource" target="_blank" rel="noopener noreferrer">Open external resource <span class="sr-only">(opens in a new tab)</span></a>
<!-- Browser/accessibility result: isolated new tab with an announced behavior cue. -->
```

## High-Use Responsive and Extendable Snippet

```html
<article>
  <picture>
    <source media="(min-width: 60rem)" srcset="course-wide-1200.webp 1200w, course-wide-1800.webp 1800w" sizes="80vw">
    <img src="course-640.webp" srcset="course-640.webp 640w, course-960.webp 960w" sizes="(min-width: 40rem) 50vw, 100vw" width="960" height="640" loading="lazy" decoding="async" alt="Learner building a course project">
  </picture>
  <h2>Java Foundations</h2>
  <p>Learn one concept at a time with runnable output.</p>
  <a href="/courses/java">View course <span class="sr-only">Java Foundations</span></a>
</article>
<!-- Result: responsive image selection, stable layout dimensions, lazy below-fold loading, and reusable semantic card content. -->
```

Use CSS for layout and visual variants. Keep the HTML contract stable: meaningful heading, content, and action still work without styling or JavaScript.
