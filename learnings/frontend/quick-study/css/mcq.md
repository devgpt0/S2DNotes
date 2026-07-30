# CSS MCQs: predict the computed style

There are 50 questions: 30 code-snippet questions and 20 theory questions. Assume no other CSS applies unless the question says otherwise.

## Part A: code-snippet MCQs (1-30)

### 1. What color is the paragraph?

```html
<p class="notice">Read this.</p>
```

```css
p { color: black; }
.notice { color: blue; }
```

- A. Black
- B. Blue
- C. Browser default
- D. Transparent

**Answer: B.** A class selector is more specific than an element selector.

### 2. What color wins?

```html
<p id="message" class="notice">Read this.</p>
```

```css
p { color: black; }
.notice { color: blue; }
#message { color: red; }
```

- A. Black
- B. Blue
- C. Red
- D. All three colors

**Answer: C.** An ID selector has higher specificity than a class selector.

### 3. Which rule wins on a specificity tie?

```html
<p class="notice">Read this.</p>
```

```css
.notice { color: blue; }
.notice { color: green; }
```

- A. Blue
- B. Green
- C. Both colors blend
- D. The browser default

**Answer: B.** Later source order breaks an otherwise equal cascade tie.

### 4. What is the total rendered width with this base rule?

```css
* { box-sizing: border-box; }
.card { width: 200px; padding: 20px; border: 5px solid; }
```

- A. 200px
- B. 240px
- C. 250px
- D. 210px

**Answer: A.** `border-box` includes padding and border in the declared width.

### 5. What changes when the base rule is absent?

```css
.card { width: 200px; padding: 20px; border: 5px solid; }
```

- A. Total width is 200px
- B. Total width is 240px
- C. Total width is 250px
- D. The box is invisible

**Answer: C.** Content-box width plus 40px padding and 10px border equals 250px.

### 6. Which `h2` matches this selector?

```css
.card > h2 { color: navy; }
```

- A. Any `h2` anywhere in the document
- B. An `h2` that is a direct child of `.card`
- C. An `h2` before `.card`
- D. Only an `h2` with `id="card"`

**Answer: B.** `>` is the direct-child combinator.

### 7. What state makes this outline appear?

```css
.button:focus-visible { outline: 3px solid blue; }
```

- A. When the button is disabled
- B. When keyboard-style focus should be visibly indicated
- C. When the button is hidden
- D. When the page loads

**Answer: B.** `:focus-visible` is designed for a clear focus indication when appropriate.

### 8. What does this layout create by default?

```css
.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
```

- A. A vertical main axis with horizontal cross-axis alignment
- B. A horizontal main axis with vertically centered items
- C. A two-dimensional grid
- D. A hidden container

**Answer: B.** Flex defaults to `row`; `justify-content` uses the main axis and `align-items` uses the cross axis.

### 9. Which property changes the Flexbox main axis to vertical?

```css
.stack {
  display: flex;
  flex-direction: column;
}
```

- A. `display: flex`
- B. `flex-direction: column`
- C. `column`
- D. `stack`

**Answer: B.** The column direction makes vertical the main axis.

### 10. What does `gap` add here?

```css
.actions {
  display: flex;
  gap: 1rem;
}
```

- A. Space only outside the container
- B. Space between flex items
- C. A border around items
- D. Extra font size

**Answer: B.** `gap` is interior spacing between layout items.

### 11. How does this card grid react to less space?

```css
.cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(16rem, 1fr));
}
```

- A. Every card remains on one line at any width
- B. It uses as many 16rem-minimum columns as fit, then reduces columns
- C. It creates exactly sixteen columns
- D. It switches to Flexbox

**Answer: B.** `auto-fit` and `minmax` make a content-responsive grid.

### 12. Which element anchors this absolutely positioned close button?

```css
.card { position: relative; }
.close { position: absolute; top: 0; right: 0; }
```

- A. The viewport
- B. The closest positioned ancestor, `.card`
- C. The document title
- D. The previous sibling

**Answer: B.** A positioned ancestor establishes the containing block.

### 13. What happens to this element in normal layout?

```css
.notice { display: none; }
```

- A. It still takes space but is transparent
- B. It is removed from layout
- C. It becomes fixed
- D. It becomes a screen-reader-only element

**Answer: B.** `display: none` removes the element from rendering and the accessibility tree.

### 14. What does this overflow rule do when needed?

```css
.code-panel { overflow: auto; }
```

- A. Always shows both scrollbars
- B. Adds scrolling only if content overflows
- C. Hides overflowing content
- D. Wraps every word

**Answer: B.** `auto` lets the browser supply scrolling when required.

### 15. What does this size respond to?

```css
h1 { font-size: clamp(2rem, 5vw, 4rem); }
```

- A. It is always 5vw
- B. It grows with viewport width but stays from 2rem to 4rem
- C. It is always 2rem
- D. It is always 4rem

**Answer: B.** `clamp(minimum, preferred, maximum)` limits a fluid value.

### 16. What value does this button receive?

```css
:root { --brand: #1d4ed8; }
.button { background: var(--brand); }
```

- A. `var(--brand)` remains literal text
- B. `#1d4ed8`
- C. The browser default background
- D. An inherited font color

**Answer: B.** `var()` reads the custom property value.

### 17. Which viewport matches this rule?

```css
@media (min-width: 48rem) {
  .sidebar { display: block; }
}
```

- A. Any viewport narrower than 48rem
- B. A viewport at least 48rem wide
- C. Only a 48px viewport
- D. A container 48rem wide

**Answer: B.** This is a viewport media query with an inclusive minimum.

### 18. What must exist for this query to work?

```css
@container (min-width: 32rem) {
  .card { grid-template-columns: 10rem 1fr; }
}
```

- A. A nearby element with a container type, such as `container-type: inline-size`
- B. A media query
- C. An ID selector
- D. A JavaScript event listener

**Answer: A.** Container queries need a query container.

### 19. What does this transform change first?

```css
.button:hover { transform: translateY(-2px); }
```

- A. The normal-flow position of following elements
- B. The painted visual position of the button
- C. The button's text content
- D. The viewport height

**Answer: B.** Transforms move the visual result without reflowing normal layout.

### 20. Which properties are transitioned?

```css
.button { transition: transform 150ms ease, opacity 150ms ease; }
```

- A. Every property
- B. Only `transform` and `opacity`
- C. Only background color
- D. No property until an animation is defined

**Answer: B.** Listing exact properties is clearer than `transition: all`.

### 21. What does this query respect?

```css
@media (prefers-reduced-motion: reduce) {
  .spinner { animation: none; }
}
```

- A. A user preference for less motion
- B. A smaller device width
- C. A lower color contrast
- D. An offline connection

**Answer: A.** It removes nonessential animation for users who request reduced motion.

### 22. Which value inherits to a child by default?

```css
.article { color: #111827; margin: 2rem; }
```

- A. `color` only
- B. `margin` only
- C. Both values
- D. Neither value

**Answer: A.** Text color normally inherits; margins do not.

### 23. What does this selector match?

```css
[aria-current="page"] { font-weight: 700; }
```

- A. Only buttons
- B. Any element with that exact attribute/value pair
- C. Every link
- D. The root element only

**Answer: B.** Attribute selectors match an attribute condition, regardless of element type.

### 24. Why can this be necessary on a flex child?

```css
.article-body { min-width: 0; }
```

- A. It makes every word bold
- B. It allows a long-content child to shrink instead of forcing overflow
- C. It positions the child absolutely
- D. It removes padding

**Answer: B.** Flex and grid items can otherwise keep a large intrinsic minimum width.

### 25. What does this logical property change?

```css
.content { padding-inline: 1rem; }
```

- A. Top and bottom padding
- B. Start and end padding in the inline direction
- C. Border radius
- D. Only left padding in every writing direction

**Answer: B.** Logical properties adapt to writing direction.

### 26. What does this preserve?

```css
img {
  max-width: 100%;
  height: auto;
}
```

- A. The original file size
- B. The image aspect ratio while allowing it to shrink
- C. A fixed 100px width
- D. The image's CSS background

**Answer: B.** Automatic height follows the scaled width.

### 27. What creates the extra text after the label?

```css
.required::after { content: " *"; }
```

- A. A pseudo-element
- B. A DOM text node written in HTML
- C. An inherited attribute
- D. A media query

**Answer: A.** `::after` generates a styled visual part; essential information should not live only there.

### 28. What is the usual behavior of this position?

```css
.header {
  position: sticky;
  top: 0;
}
```

- A. It is always removed from flow
- B. It behaves in normal flow until the scroll threshold, then sticks within its container
- C. It stays fixed to the viewport regardless of its container
- D. It disables scrolling

**Answer: B.** Sticky combines normal-flow placement with threshold-based sticking.

### 29. What does this layer order declare?

```css
@layer reset, base, components, utilities;
```

- A. The number of grid columns
- B. An explicit cascade priority order for layers
- C. An animation sequence
- D. Four custom properties

**Answer: B.** Layer ordering helps control which groups of rules win.

### 30. What likely happens here?

```css
.parent { opacity: 0.9; }
.child { position: relative; z-index: 9999; }
```

- A. The child can always appear above every element on the page
- B. Opacity can create a stacking context that confines the child
- C. `z-index` changes text color
- D. The child becomes invisible

**Answer: B.** A large z-index cannot escape its parent's stacking context.

## Part B: theory MCQs (31-50)

### 31. What does the CSS cascade decide?

- A. Which HTML file loads
- B. Which competing declaration wins
- C. Which database query runs
- D. Which image is accessible

**Answer: B.** The cascade resolves matching style declarations.

### 32. Why prefer class selectors for most component styling?

- A. They are impossible to override
- B. They are reusable and have manageable specificity
- C. They replace HTML semantics
- D. They make CSS asynchronous

**Answer: B.** Classes offer clear, low-conflict styling hooks.

### 33. What is outside an element's border in the box model?

- A. Content
- B. Padding
- C. Margin
- D. Background

**Answer: C.** Margin separates the element from its neighbors.

### 34. When should Flexbox usually be chosen over Grid?

- A. For a one-dimensional row or column arrangement
- B. For every page layout
- C. For server-side data
- D. For image compression

**Answer: A.** Flexbox focuses on one main axis.

### 35. When is Grid especially useful?

- A. When rows and columns must be controlled together
- B. When only text color changes
- C. When JavaScript is disabled
- D. When a link opens another page

**Answer: A.** Grid is two-dimensional.

### 36. Why avoid `!important` as a normal repair tool?

- A. It never works
- B. It makes cascade ownership and later overrides harder to maintain
- C. It removes all CSS
- D. It changes HTML validity

**Answer: B.** Solve the selector, source order, or component boundary instead.

### 37. What is a content-driven breakpoint?

- A. A breakpoint chosen when layout content no longer fits well
- B. A breakpoint named after a phone
- C. A JavaScript error
- D. A CSS syntax error

**Answer: A.** Layout needs should determine breakpoints.

### 38. Why keep keyboard focus visible?

- A. It saves bandwidth
- B. It tells keyboard users which control is active
- C. It makes hover work on touch devices
- D. It prevents inheritance

**Answer: B.** Focus is required to navigate confidently without a pointer.

### 39. What should color contrast support?

- A. Decoration only
- B. Readable text and distinguishable controls
- C. Smaller HTML files
- D. More selector specificity

**Answer: B.** Contrast is an accessibility and usability requirement.

### 40. Why test layouts with enlarged text?

- A. It makes fonts load sooner
- B. It reveals clipping and fixed-height failures
- C. It resets custom properties
- D. It changes media queries to JavaScript

**Answer: B.** Interfaces must survive zoom and user font preferences.

### 41. What is a stacking context?

- A. A block formatting context only
- B. A local z-ordering world for an element and descendants
- C. A Flexbox container
- D. A type of font

**Answer: B.** Descendants cannot out-rank elements outside that context just by increasing z-index.

### 42. Which browser tool best shows a crossed-out losing declaration?

- A. The computed styles/rules inspector
- B. The address bar
- C. The page title
- D. View source only

**Answer: A.** Developer tools explain the applied and overridden rules.

### 43. Why use `rem` frequently for spacing and typography?

- A. It depends on the root text size and scales predictably
- B. It always equals one pixel
- C. It disables zoom
- D. It is a grid-only unit

**Answer: A.** Root-relative sizing supports coherent scaling.

### 44. What is a custom property's main benefit?

- A. It turns CSS into JavaScript
- B. It gives repeated design values a reusable, cascade-aware name
- C. It removes the need for selectors
- D. It encrypts colors

**Answer: B.** Variables help keep colors, spacing, and theme values consistent.

### 45. Why prefer `transform`/`opacity` for simple motion when possible?

- A. They are always accessible without testing
- B. They often avoid costly layout work compared with size/position changes
- C. They remove the need for CSS
- D. They create semantic HTML

**Answer: B.** Still keep motion brief and respect reduced-motion preferences.

### 46. What does mobile-first CSS mean?

- A. Hide desktop content permanently
- B. Start with the small-layout base and add enhancements as space becomes available
- C. Use only pixels
- D. Ignore large screens

**Answer: B.** It produces a simple base and intentional larger-layout rules.

### 47. Why can `100vw` cause horizontal scrolling?

- A. It may include the scrollbar width
- B. It always equals zero
- C. It disables overflow
- D. It removes padding

**Answer: A.** `width: 100%` is often safer for normal layout containers.

### 48. What is the safest default layout strategy?

- A. Absolute-position every element
- B. Use normal flow, then Flexbox or Grid for real layout relationships
- C. Use tables for all columns
- D. Add `z-index: 9999` everywhere

**Answer: B.** Native flow is resilient to changing content.

### 49. Why should essential information not be only in `::before` or `::after` content?

- A. Pseudo-elements cannot have color
- B. Generated visual content is not a reliable semantic content source
- C. It prevents CSS loading
- D. It makes the DOM invalid

**Answer: B.** Put required information in the HTML itself.

### 50. What should you do first when a CSS rule seems ignored?

- A. Add `!important`
- B. Inspect whether the selector matches and which rule wins
- C. Rewrite the HTML completely
- D. Add random margins

**Answer: B.** Developer tools provide the evidence needed for a correct fix.
