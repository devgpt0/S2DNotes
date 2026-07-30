# CSS: turn clear HTML into a usable interface

CSS controls the presentation of HTML: spacing, color, type, layout, responsive behavior, and motion. The browser first builds the HTML DOM, then matches CSS rules to elements, resolves conflicts, calculates sizes and positions, and paints the result.

Read every rule as: **select these elements, then apply these declarations.**

```css
.card {
  padding: 1rem;
  border: 1px solid #d1d5db;
}
```

This selects every element with `class="card"`, adds inside spacing, and draws a border around it.

## 1. Start with a predictable base

### The idea

Browsers have useful default styles, but predictable sizing removes a common beginner surprise: a declared width normally describes the content box, not its padding and border.

### See it in code

```css
* {
  box-sizing: border-box;
}

body {
  margin: 0;
  font-family: system-ui, sans-serif;
  line-height: 1.5;
}
```

With `border-box`, `width: 20rem` includes the content, padding, and border. Margin remains outside. Setting it on every element makes component widths easier to reason about.

## 2. Select the element you actually mean

### The idea

A selector says which elements receive a rule. Prefer small, reusable class selectors because they are easy to understand and override.

### See it in code

```css
button { color: #111827; }                 /* element */
.button { background: #dbeafe; }           /* class */
#save { border-color: #2563eb; }           /* unique ID */
[aria-current="page"] { font-weight: 700; } /* attribute */
.card > h2 { margin-top: 0; }               /* direct child */
.card h2 { color: #1e3a8a; }                /* any descendant */
```

The `>` in `.card > h2` matters: it matches an `h2` immediately inside `.card`, not one nested further down.

### States and generated parts

```css
.button:hover { background: #bfdbfe; }
.button:focus-visible { outline: 3px solid #1d4ed8; }
.field:disabled { opacity: 0.6; }
.required::after { content: " *"; }
```

Pseudo-classes such as `:hover`, `:focus-visible`, and `:disabled` match a state. Pseudo-elements such as `::after` style a generated part. Do not place essential information only in generated CSS content; it may not be available to every user.

## 3. Understand the cascade before reaching for `!important`

### The idea

Several rules can match one element. The **cascade** decides the winning declaration. For ordinary author styles, compare importance, layer, specificity, then source order.

### See it in code

```css
p { color: #111827; }
.notice { color: #1d4ed8; }
#message { color: #b91c1c; }
```

For `<p id="message" class="notice">`, the text is red because an ID selector is more specific than a class or element selector.

### Specificity in plain language

- An ID selector beats a class, attribute selector, or pseudo-class.
- A class, attribute selector, or pseudo-class beats an element selector.
- If specificity ties, the later rule wins.
- Inline styles are very strong. `!important` changes the cascade and makes normal maintenance harder; avoid it.

Some properties inherit from a parent, such as `color` and `font-family`. Spacing and layout properties such as `margin` and `display` do not. Use the browser's computed-styles panel to see the real winner.

## 4. The box model explains spacing and size

### The idea

Every rendered box has content in the middle, then padding, border, and margin moving outward.

```text
margin
  border
    padding
      content
```

### See it in code

```css
.notice {
  width: 20rem;
  padding: 1rem;
  border: 2px solid #93c5fd;
  margin: 1.5rem auto;
}
```

With the base rule `box-sizing: border-box`, this box is 20rem wide including its 2rem of horizontal padding and 4px of horizontal border. Its vertical margin separates it from neighbors; `auto` horizontal margins center it when a width is available.

### Choose units by what they respond to

- `rem`: root font size; a strong default for text and spacing.
- `em`: current element's font size; useful for component-relative values.
- `%`: a related container size.
- `vw` and `vh`: viewport dimensions; use carefully on mobile browsers.
- `fr`: remaining space in a grid.
- `min()`, `max()`, and `clamp()`: safe responsive limits.

```css
h1 {
  font-size: clamp(2rem, 5vw, 4rem);
}
```

This heading grows with the viewport but never becomes smaller than 2rem or larger than 4rem.

## 5. Normal flow, display, and positioning

### The idea

Normal document flow is the browser's default layout algorithm: block elements stack and inline content flows through text. Use it first. Use other layout modes when they solve a real relationship.

### See it in code

```css
.badge { display: inline-block; }
.hidden { display: none; }

.dialog {
  position: fixed;
  inset: 1rem;
}

.card { position: relative; }
.card__close {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
}
```

- `block` normally starts on a new line and fills available inline width.
- `inline` flows with text and ignores most width and height settings.
- `inline-block` flows with text but accepts dimensions.
- `none` removes the element from layout and the accessibility tree.
- `relative` stays in flow but creates a positioning reference.
- `absolute` leaves normal flow and looks for the nearest positioned ancestor.
- `fixed` positions against the viewport.
- `sticky` stays in flow until its scroll boundary, then sticks inside its scroll container.

Use `overflow: auto` when a container should scroll only if content needs it. Avoid fixed heights for text containers because translated or zoomed text can overflow.

## 6. Use Flexbox for one direction

### The idea

Flexbox lays out items along one main axis: a row or a column. It excels at toolbars, button groups, and simple alignment.

### See it in code

```css
.toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
}

.toolbar__actions {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}
```

The default `flex-direction` is `row`, so the main axis is horizontal. `justify-content` positions items along that main axis. `align-items` positions them across it, normally vertically. If you change to `flex-direction: column`, the axes change too.

Use `gap` for space *between* layout items. It does not add unwanted space around the outside edge.

```css
.content { min-width: 0; }
```

This small rule is sometimes needed on a flex child with long text: it permits the child to shrink rather than forcing overflow.

## 7. Use Grid for rows and columns together

### The idea

Grid describes two-dimensional layout. It is a natural choice for card collections, page regions, and repeated rows and columns.

### See it in code

```css
.cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(16rem, 1fr));
  gap: 1rem;
}
```

Read the column rule as: create as many columns as fit; each is at least 16rem wide; share remaining space equally. When the container becomes narrow, cards wrap naturally into fewer columns without a device-specific breakpoint.

```css
.page {
  display: grid;
  grid-template-columns: 16rem minmax(0, 1fr);
  gap: 2rem;
}
```

`minmax(0, 1fr)` permits the second column to shrink below its content's preferred width, which helps long content avoid horizontal overflow.

## 8. Create readable typography and reusable design values

### The idea

Good typography helps users scan and understand content. Custom properties let repeated values have one meaningful name.

### See it in code

```css
:root {
  --color-text: #111827;
  --color-surface: #ffffff;
  --color-action: #1d4ed8;
  --space-md: 1rem;
  --radius-md: 0.5rem;
}

body {
  color: var(--color-text);
  background: var(--color-surface);
}

.button {
  padding: 0.75rem var(--space-md);
  border-radius: var(--radius-md);
  background: var(--color-action);
  color: white;
}
```

Custom properties participate in the cascade, so a component or dark theme can redefine them. Ensure foreground and background combinations have enough contrast. Keep line height comfortable and do not prevent users from zooming text.

Prefer logical properties when direction should not matter:

```css
.content {
  margin-inline: auto;
  padding-block: 2rem;
  padding-inline: 1rem;
}
```

## 9. Make layouts responsive to available space

### The idea

Start with the smallest useful layout, then change it when the content needs more room. A breakpoint belongs to a layout problem, not a device brand.

### See it in code

```css
.sidebar { display: none; }

@media (min-width: 48rem) {
  .sidebar { display: block; }
}

img {
  max-width: 100%;
  height: auto;
}
```

The sidebar is absent until 48rem of viewport width is available. Images can shrink with their container while retaining their aspect ratio.

For reusable components, container queries respond to the component's own space:

```css
.card-list { container-type: inline-size; }

@container (min-width: 32rem) {
  .card { grid-template-columns: 10rem 1fr; }
}
```

## 10. Add interaction and motion without excluding people

### The idea

States should work for mouse, keyboard, and touch users. Motion should explain a change, not distract from it.

### See it in code

```css
.button {
  transition: transform 150ms ease, background-color 150ms ease;
}

.button:hover,
.button:focus-visible {
  background-color: #1e40af;
  transform: translateY(-2px);
}

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms;
    transition-duration: 0.01ms;
  }
}
```

`transform` moves the painted result without changing normal layout. Animating `transform` and `opacity` is usually smoother than repeatedly changing `top`, `width`, or `height`. `:focus-visible` preserves a clear keyboard focus signal without showing it unnecessarily after a pointer click.

## 11. Debug the browser's computed result

When CSS surprises you, do not guess. Inspect the element in browser developer tools.

1. Confirm the selector actually matches.
2. Check which declaration is crossed out and why it lost the cascade.
3. Inspect the computed value, box model, and inherited values.
4. Turn on Flexbox or Grid overlays to see tracks and alignment.
5. Test narrow width, text zoom, long words, keyboard focus, and reduced motion.

Avoid `!important` as a repair. It hides the ownership problem and makes the next change harder. A small class, predictable source order, and a clear component boundary are usually enough.

## Learning path: beginner to expert

1. Practise selectors, the cascade, inheritance, and the box model.
2. Build layouts in normal flow, then add Flexbox and Grid deliberately.
3. Use `rem`, responsive limits, and content-driven breakpoints.
4. Create reusable values with custom properties and test contrast.
5. Test keyboard focus, zoom, reduced motion, and long translated content.
6. Learn to debug computed styles instead of adding random overrides.
