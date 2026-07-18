# 11 - CSS Practical Activities and Interview Answers

## Activity 1: Responsive Course Cards

Build cards with image, title, description, price, and button.

Requirements:

- one column at narrow widths
- automatic extra columns when each card can remain at least 16rem
- images preserve 16:9 ratio
- equal spacing through `gap`
- visible keyboard focus
- no horizontal page scrolling at 320px

### Example Layout Solution

```css
.cards { display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 16rem), 1fr)); gap: 1rem; }
.card img { inline-size: 100%; aspect-ratio: 16 / 9; object-fit: cover; }
.card a:focus-visible { outline: .2rem solid royalblue; outline-offset: .2rem; }
/* Browser result: responsive accessible card grid without device-specific breakpoints. */
```

## Activity 2: Dashboard

Create header, sidebar, main cards, and wide table. Use Grid for page layout, Flexbox for toolbar controls, sticky header, scrollable table wrapper, and a mobile single-column layout.

## Activity 3: Browser Performance Lab

Record a page in DevTools Performance. Enable paint flashing. Change an animation from `left` to `transform`, retest, and explain the rendering-stage difference.

## Interview Questions with Answers

### 1. What is the cascade?

The browser's conflict-resolution system using origin/importance, layers, specificity, scoping proximity, and source order.

### 2. `display: none` vs `visibility: hidden`?

`display: none` removes layout and accessibility-tree presence. `visibility: hidden` keeps layout space but hides the element and normally removes interaction/accessibility exposure.

### 3. Flexbox vs Grid?

Flexbox is primarily one-dimensional and content-driven. Grid controls rows and columns together. They can be combined.

### 4. Why use `box-sizing: border-box`?

Declared width includes content, padding, and border, making component sizing easier to reason about.

### 5. What creates a stacking context?

Examples include positioned elements with non-auto z-index, transforms, opacity below one, isolation, filters, and some containment. Z-index only compares within relevant contexts.

### 6. Mobile-first meaning?

Write the base small-screen experience first and enhance with `min-width` queries. It encourages simple defaults and avoids undoing desktop assumptions.

### 7. Media vs container query?

Media query responds to viewport/device/user environment. Container query responds to a component container's size/style.

### 8. Reflow/layout vs repaint?

Layout recalculates geometry; paint redraws pixels. A change may trigger both. Transform/opacity can often be composited more cheaply, but measure.

### 9. How do you prevent responsive overflow?

Use flexible tracks, `minmax(0, 1fr)`, `min-width: 0` for flex/grid children, wrapping, responsive media, overflow wrappers for genuinely wide data, and long-content tests.

### 10. How do you support multiple browsers?

Define a support policy, check compatibility data, use progressive enhancement/fallbacks, run automated cross-browser tests, and test real interaction on representative devices.
