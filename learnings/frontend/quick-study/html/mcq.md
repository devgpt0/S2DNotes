# HTML interview MCQs with explanations

Answer each question before reading the explanation.

## 1. What does HTML primarily describe?

- A. Database queries
- B. Page structure and meaning
- C. Network routing
- D. Image editing

**Answer: B — Page structure and meaning.** HTML identifies content such as headings, paragraphs, navigation, forms, and articles. CSS controls presentation, while JavaScript adds behavior.

## 2. Why is `<!doctype html>` used?

- A. It imports CSS
- B. It enables modern standards mode
- C. It adds page metadata
- D. It opens the DOM

**Answer: B — It enables modern standards mode.** The doctype tells browsers to render the document using current HTML rules instead of legacy quirks mode.

## 3. Which element contains the page's unique main content?

- A. `section`
- B. `article`
- C. `main`
- D. `body`

**Answer: C — `main`.** `main` identifies the primary content of the page. `body` contains all visible page content, including repeated headers, navigation, and footers.

## 4. Which element should trigger an in-page action?

- A. `a`
- B. `button`
- C. `div`
- D. `span`

**Answer: B — `button`.** Buttons provide built-in keyboard, focus, and accessibility behavior for actions. Links are intended for navigation to a URL.

## 5. Which element should navigate to another URL?

- A. `a`
- B. `button`
- C. `label`
- D. `nav`

**Answer: A — `a`.** An anchor with an `href` represents navigation and supports expected browser behavior such as opening in a new tab or copying the destination.

## 6. What should `alt` contain for an informative image?

- A. The file name
- B. Its visual style
- C. A description of its purpose
- D. Empty text

**Answer: C — A description of its purpose.** Good alternative text communicates the information the image contributes in its current context, not every visual detail.

## 7. What should a purely decorative image use?

- A. No `img` element
- B. `alt=""`
- C. `alt="image"`
- D. `title="decorative"`

**Answer: B — `alt=""`.** An empty alternative tells screen readers to ignore decoration. Omitting `alt` may cause a screen reader to announce the file name instead.

## 8. How is a label explicitly connected to an input?

- A. They use the same class
- B. The label's `for` matches the input's `id`
- C. They use the same `name`
- D. They are styled by adjacent CSS

**Answer: B — Matching `for` and `id`.** This association gives the input an accessible name and makes clicking the label focus or activate the input.

## 9. Which input attribute becomes the submitted field key?

- A. `id`
- B. `class`
- C. `name`
- D. `for`

**Answer: C — `name`.** Form submission sends name/value pairs. An input without a `name` is generally not included in the submitted form data.

## 10. What is the default type of a `button` inside a form?

- A. `button`
- B. `reset`
- C. `submit`
- D. `menu`

**Answer: C — `submit`.** A form button submits by default. Set `type="button"` explicitly when the button performs a different action.

## 11. Which method suits a search form that does not change server state?

- A. GET
- B. POST
- C. PATCH
- D. DELETE

**Answer: A — GET.** GET represents a safe read and places search parameters in the URL, making results bookmarkable and shareable.

## 12. Which attribute is true simply when it is present?

- A. `class`
- B. `disabled`
- C. `value`
- D. `name`

**Answer: B — `disabled`.** It is a Boolean attribute. Even `disabled="false"` means disabled because presence, not the text value, determines the state.

## 13. Which heading normally identifies the page's main subject?

- A. `h6`
- B. `h3`
- C. `h1`
- D. Whichever heading has the desired size

**Answer: C — `h1`.** Heading levels describe document structure, not appearance. CSS should control size while heading order communicates hierarchy.

## 14. Which element represents standalone content such as a blog post?

- A. `article`
- B. `aside`
- C. `span`
- D. `footer`

**Answer: A — `article`.** An article is content that can make sense independently, such as a post, news story, review, or forum entry.

## 15. Which element groups the primary navigation links?

- A. `menu`
- B. `nav`
- C. `section`
- D. `header`

**Answer: B — `nav`.** `nav` identifies a significant group of navigation links. A `header` may contain it but does not itself mean navigation.

## 16. Which elements group form controls and name the group?

- A. `div` and `p`
- B. `form` and `label`
- C. `fieldset` and `legend`
- D. `section` and `h2`

**Answer: C — `fieldset` and `legend`.** `fieldset` groups related controls, while `legend` gives that group an accessible label, especially useful for radio buttons and checkboxes.

## 17. When do radio buttons belong to one group?

- A. When they share an `id`
- B. When they share a `name`
- C. When they share a `value`
- D. When they share a class

**Answer: B — When they share a `name`.** The browser then allows only one radio button in that named group to be selected. Each option should still have its own value and ID.

## 18. Which table cell represents a header?

- A. `td`
- B. `tr`
- C. `th`
- D. `thead`

**Answer: C — `th`.** A `th` identifies a row or column header. `scope="row"` or `scope="col"` makes its relationship to data cells explicit.

## 19. Which element gives a table its accessible title?

- A. `label`
- B. `title`
- C. `caption`
- D. `legend`

**Answer: C — `caption`.** A caption describes the table as a whole and is programmatically associated with it.

## 20. What does `defer` do on a classic external script?

- A. It runs the script before parsing
- B. It runs after parsing and preserves script order
- C. It prevents the download
- D. It runs only after a click

**Answer: B — It runs after parsing and preserves order.** Deferred scripts download in parallel with HTML parsing, then execute in document order before `DOMContentLoaded`.

## 21. What is true about `async` scripts?

- A. Their execution order is guaranteed
- B. They run only after `DOMContentLoaded`
- C. They run as soon as downloaded, so order is not guaranteed
- D. They block their own download

**Answer: C — They execute as soon as ready.** `async` is suitable for independent scripts. Dependent scripts should not rely on async execution order.

## 22. Which metadata is essential for a responsive mobile layout?

- A. Keywords
- B. Viewport
- C. Author
- D. Refresh

**Answer: B — Viewport.** `<meta name="viewport" content="width=device-width, initial-scale=1.0">` makes the CSS viewport match the device width.

## 23. What does `loading="lazy"` usually do on an image?

- A. Compresses it
- B. Delays loading until it is near the viewport
- C. Hides its alternative text
- D. Converts its format

**Answer: B — It delays off-screen loading.** This can reduce initial network work, but the main visible image should normally load eagerly.

## 24. Why specify an image's width and height?

- A. To add resolution
- B. To reserve layout space
- C. To enable alternative text
- D. To turn it into a link

**Answer: B — To reserve layout space.** The browser can calculate the aspect ratio before the image downloads, reducing unexpected layout shift.

## 25. Which attribute limits an iframe's capabilities?

- A. `sandbox`
- B. `target`
- C. `media`
- D. `scope`

**Answer: A — `sandbox`.** It restricts capabilities such as scripts, forms, and same-origin access. Add back only the permissions the embedded content requires.

## 26. What does ARIA add?

- A. CSS behavior
- B. Semantics for accessibility APIs
- C. Automatic keyboard logic
- D. Server validation

**Answer: B — Accessibility semantics.** ARIA communicates roles, states, and relationships, but developers must still implement keyboard behavior and focus management.

## 27. Which `tabindex` adds an element to normal keyboard focus order?

- A. `-1`
- B. `0`
- C. `1`
- D. `99`

**Answer: B — `0`.** It uses DOM order. `-1` permits programmatic focus but removes the element from Tab order; positive values create difficult custom focus ordering.

## 28. Which element preserves whitespace for a code block?

- A. `code` alone
- B. `pre`
- C. `samp`
- D. `blockquote`

**Answer: B — `pre`.** `pre` preserves spaces and line breaks. It is commonly combined with a nested `code` element to identify source code semantically.

## 29. Client-side form validation is best described as what?

- A. A replacement for server validation
- B. User assistance, not a security boundary
- C. Something performed only by CSS
- D. A complete defense against invalid requests

**Answer: B — User assistance, not security.** Attackers can bypass the browser and send requests directly, so the server must independently validate every field.

## 30. Which markup is invalid?

- A. Unique IDs
- B. A button containing text
- C. Multiple elements with the same ID
- D. A label wrapping its input

**Answer: C — Duplicate IDs.** IDs must be unique so labels, URL fragments, scripts, and accessibility relationships identify the intended element reliably.
