# 07 - HTML Practical Activities and Interview Answers

## Activity 1: Accessible Article Page

Build a page with header, main navigation, article, two sections, figure/caption, related-links aside, and footer.

Success criteria:

- meaningful heading hierarchy
- keyboard-usable links
- descriptive image alternative text
- valid landmarks
- no `div` used where a semantic element fits

### Example Solution Skeleton

```html
<header><a href="/">Academy</a></header>
<nav aria-label="Main"><a href="/courses">Courses</a></nav>
<main>
  <article>
    <h1>Learning HTML</h1>
    <section><h2>Start with meaning</h2><p>Choose elements by purpose.</p></section>
    <figure><img src="html.svg" alt="HTML document tree"><figcaption>Document structure</figcaption></figure>
  </article>
</main>
<footer>Example Academy</footer>
<!-- Browser result: a structured, navigable article page. -->
```

## Activity 2: Registration Form

Build name, email, password, experience, terms checkbox, and submit controls. Add labels, autocomplete, required rules, useful errors, and a fieldset where needed. Test keyboard-only operation and invalid submission.

## Activity 3: Performance Inspection

Open a page in DevTools Network with cache disabled and mobile throttling. Record the largest file, first render-blocking request, LCP element, and one improvement.

## Interview Questions with Answers

### 1. What is semantic HTML?

Semantic HTML uses elements that describe content purpose, such as `nav`, `main`, `article`, and `button`. It improves accessibility, browser behavior, maintainability, and search understanding.

### 2. `div` vs `section`?

`div` has no semantic meaning and groups content for styling/scripting. `section` is a thematic section that normally has a heading. Do not replace every `div` with `section`.

### 3. Why include `lang`?

It helps screen readers choose pronunciation rules and helps translation/search tooling understand language.

### 4. Why are width and height important on images?

They let the browser reserve aspect-ratio space before the image arrives, reducing layout shift.

### 5. `defer` vs `async`?

Both download without blocking HTML parsing. Deferred scripts run after parsing in document order. Async scripts run as soon as ready and have no guaranteed relative order.

### 6. Client vs server validation?

Client validation improves user feedback but can be bypassed. Server validation is the security and data-integrity boundary.

### 7. Button vs link?

A link navigates. A button performs an action. Choosing correctly gives built-in keyboard and accessibility behavior.

### 8. What is the DOM?

The DOM is the browser's object tree created from parsed HTML. JavaScript can read and modify it.

### 9. What causes CLS?

Content moving unexpectedly, often from images without reserved dimensions, late ads/banners, or font/layout changes.

### 10. What does CORS do?

CORS lets a server tell browsers which other origins may read its responses. It does not authenticate callers and does not protect direct server-to-server requests.
