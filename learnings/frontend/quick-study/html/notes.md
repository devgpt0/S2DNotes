# HTML: beginner-to-expert essential notes

HTML gives a web page its **meaning and structure**. CSS makes it look good; JavaScript makes it react.

## 1. Mental model and page shell

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Page title</title>
    <meta name="description" content="A short page summary." />
  </head>
  <body>
    <main><h1>One main page heading</h1></main>
  </body>
</html>
```

- `<!doctype html>` tells the browser to use modern HTML.
- `lang` helps screen readers and search engines.
- `viewport` makes the layout use the device width on phones.
- `title` appears in the browser tab and search results.
- Use one clear `h1`; follow it with `h2`, then `h3`—do not choose headings only for their size.

## 2. Elements, attributes, and the DOM

An element normally has an opening tag, content, and a closing tag. Void elements such as `img`, `input`, `br`, `hr`, `meta`, and `link` have no closing tag. Attributes configure an element:

```html
<input id="email" class="field" type="email" disabled />
```

- `id` must be unique on the page; it links labels, fragments, and JavaScript to one element.
- `class` can be shared and is the usual CSS hook.
- Boolean attributes are true when present: `disabled="false"` still disables the control. Remove the attribute to make it false.
- `data-*` stores small application-specific values, readable through `element.dataset`.

The browser parses HTML into the DOM tree:

```text
document
└── html
    ├── head
    └── body
        └── main
            └── h1
```

Invalid nesting can make the browser repair the tree differently from the source. Validate markup and close elements correctly.

## 3. Use semantic elements

Semantic means the tag explains what its content is.

| Use | For |
|---|---|
| `header`, `footer` | page or section introduction/end |
| `nav` | main navigation links |
| `main` | the unique main page content |
| `section` | a themed group with a heading |
| `article` | content that can stand alone, such as a post |
| `aside` | related but secondary content |
| `button` | an action |
| `a` | navigation to a URL |

Do not use `div` or `span` when a semantic element fits. `div` is a neutral block; `span` is a neutral inline wrapper.

## 4. Everyday content

```html
<p>A paragraph with <strong>important</strong> text.</p>
<a href="/about">About us</a>
<img src="team.jpg" alt="Three support engineers in an office" />
<ul><li>Fast</li><li>Accessible</li></ul>
<ol><li>Choose a plan</li><li>Pay</li></ol>
```

- `strong` means importance; `em` means stress. Use CSS for visual bold/italic only.
- `alt` describes an image’s purpose. Use `alt=""` only for a decorative image.
- Use `a` for a destination and `button` for an action. A clickable `div` is not a good substitute.
- Give external links opened in a new tab `target="_blank" rel="noopener noreferrer"`.

Paths may be relative (`images/logo.svg`, `/about`) or absolute (`https://example.com/about`). A URL fragment such as `#pricing` moves to an element with `id="pricing"`.

Use `<figure>` with `<figcaption>` when an image, diagram, or code sample needs a caption. Use `<blockquote cite="...">` for a long quotation and `<code>` inside `<pre>` for preserved code formatting.

## 5. Forms and validation

```html
<form action="/signup" method="post">
  <label for="email">Email</label>
  <input id="email" name="email" type="email" autocomplete="email" required />
  <button type="submit">Create account</button>
</form>
```

- A `label` tells every input what it is and is connected with matching `for`/`id`.
- `name` is the key submitted with the form. `id` is for the document and label connection.
- Set `type`: `email`, `password`, `number`, `date`, `checkbox`, `radio`, etc. The browser can then give useful keyboards and basic validation.
- `required`, `minlength`, `min`, `max`, `pattern` provide browser-side help, but the server must validate again.
- `button` inside a form submits by default. Set `type="button"` for a non-submit action.
- Group related choices with `fieldset` and `legend`. Radio buttons in one group share the same `name`.

`GET` puts form data in the URL and is suitable for safe, repeatable reads such as search. `POST` sends data in the request body and is suitable for state changes. HTTPS is still required; POST is not encryption.

Useful controls:

```html
<textarea name="bio" rows="4"></textarea>
<select name="country">
  <option value="">Choose a country</option>
  <option value="in">India</option>
</select>
```

Placeholder text is a hint, not a label. Show validation errors near the field, explain how to fix them, and connect custom error text with `aria-describedby`.

## 6. Tables, media, and responsive images

Use tables only for tabular data, not layout:

```html
<table>
  <caption>Monthly sales</caption>
  <thead><tr><th scope="col">Month</th><th scope="col">Sales</th></tr></thead>
  <tbody><tr><th scope="row">June</th><td>120</td></tr></tbody>
</table>
```

`caption`, header cells, and `scope` let users understand relationships.

Use `audio` and `video` with `controls`; provide captions with `<track kind="captions">` for video. Use responsive images to avoid downloading an unnecessarily large file:

```html
<img
  src="photo-800.jpg"
  srcset="photo-400.jpg 400w, photo-800.jpg 800w"
  sizes="(max-width: 600px) 100vw, 800px"
  alt="A developer reviewing a pull request"
  width="800"
  height="450"
  loading="lazy"
/>
```

Width and height reserve space and reduce layout shift. Do not lazy-load the main above-the-fold image.

## 7. Accessibility essentials

- Start with native HTML. It already has keyboard behavior and screen-reader meaning.
- Ensure every interactive control can be reached with Tab and used with Enter/Space as appropriate.
- Keep visible focus; never remove `outline` without a clear replacement.
- Do not communicate information with color alone.
- Use labels, meaningful link text (`Read pricing`, not `Click here`), heading order, and descriptive image alt text.
- Use ARIA only when HTML cannot express the meaning. ARIA adds semantics; it does not add behavior. Prefer `<button>` to `<div role="button">`.

Landmarks (`header`, `nav`, `main`, `aside`, `footer`) provide navigation. Add a “Skip to main content” link for keyboard users. Use `aria-live` sparingly for important dynamic messages. Never add a positive `tabindex`; preserve logical DOM order.

## 8. Metadata, loading, performance, and security

```html
<link rel="stylesheet" href="styles.css" />
<script src="app.js" defer></script>
```

- Normal scripts block parsing. `defer` downloads in parallel and runs in document order after parsing.
- `async` downloads in parallel and runs as soon as ready; order is not guaranteed. Use it for independent scripts.
- Module scripts (`type="module"`) are deferred by default.
- Put canonical, social-sharing, and favicon metadata in `head` when the product needs them.
- Never inject untrusted content as HTML. Prefer text output and a strict Content Security Policy.
- `iframe` embeds another page; give it a descriptive `title` and use `sandbox` with the minimum permissions.
- Validate HTML with the Nu HTML Checker and test keyboard navigation, zoom, and a screen reader—not only visual appearance.

## 9. Common mistakes

- Multiple or skipped headings used only for visual size.
- Inputs without labels or submitted inputs without `name`.
- Duplicate IDs.
- Buttons built from `div` elements.
- Empty links, vague link text, or missing image alternatives.
- Client-side validation treated as security.
- Tables used for page layout.
- Invalid nesting such as a `div` inside a `p`.

## Interview checklist

Explain semantic HTML, `div` vs `span`, `id` vs `class`, `a` vs `button`, `alt`, form labels, `name`, `GET` vs `POST`, and why native controls are more accessible.
