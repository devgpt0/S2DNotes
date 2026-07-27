# CSS: beginner-to-expert essential notes

CSS controls presentation: layout, spacing, color, typography, and responsive behavior. Read a rule as: **select elements, then apply declarations**.

```css
.card {
  padding: 1rem;
  border: 1px solid #d1d5db;
}
```

## 1. Selectors and states

```css
button { }                  /* element */
.button { }                 /* class */
#save { }                   /* id */
[aria-current="page"] { }  /* attribute */
.card > h2 { }              /* direct child */
.card h2 { }                /* any descendant */
```

Pseudo-classes describe state (`:hover`, `:focus-visible`, `:checked`, `:disabled`, `:first-child`, `:nth-child(2n)`). Pseudo-elements style a generated part (`::before`, `::after`, `::placeholder`). Generated content must not contain essential information.

## 2. Cascade, specificity, and inheritance

When rules conflict, CSS chooses by: `!important` (avoid it), origin/layer, specificity, then later source order.

Specificity: inline style > `#id` > `.class`, `[attribute]`, `:hover` > `element`.

```css
p { color: black; }          /* element */
.notice { color: blue; }     /* class wins */
#message { color: red; }     /* id wins */
```

Some text properties, such as `color` and `font-family`, inherit from a parent. Layout properties, such as `margin`, do not. Prefer low-specificity classes; do not fight CSS with `!important`.

Cascade layers give rule groups an explicit priority:

```css
@layer reset, base, components, utilities;
```

Within the same origin, unlayered author styles beat layered styles. `:where(...)` always has zero specificity; it is useful for easy-to-override defaults.

## 3. Box model, sizing, and units

Every element has **content → padding → border → margin**. `margin` is outside; `padding` is inside.

```text
┌────────────── margin ──────────────┐
│  ┌────────── border ────────────┐  │
│  │  ┌──────── padding ───────┐  │  │
│  │  │        content         │  │  │
│  │  └────────────────────────┘  │  │
│  └──────────────────────────────┘  │
└────────────────────────────────────┘
```

```css
* { box-sizing: border-box; }
```

With `border-box`, declared width includes padding and border, which makes sizing predictable.

- `px`: fixed CSS pixels; useful for borders and small limits.
- `rem`: relative to root font size; good default for spacing and type.
- `%`: relative to parent.
- `vw`/`vh`: relative to viewport.
- `fr`: remaining space in a grid.
- `min()`, `max()`, `clamp()`: responsive limits, e.g. `font-size: clamp(1rem, 2vw, 2rem)`.

Vertical margins of normal block elements can collapse. Flex and Grid margins do not. `min-width: 0` often fixes a flex/grid child that refuses to shrink because of long content.

## 4. Display, positioning, overflow, and stacking

- `block`: starts a new line, normally fills available width.
- `inline`: stays in text flow; width/height generally do not apply.
- `inline-block`: flows inline but can have dimensions.
- `none`: removes the element from layout.
- `position: relative`: remains in flow and can anchor absolute children.
- `absolute`: removed from normal flow; positioned against nearest positioned ancestor.
- `fixed`: positioned against viewport.
- `sticky`: normal flow until its scroll threshold, then sticks within its container.

`z-index` only compares elements in the same stacking context. It works on positioned elements and flex/grid items; a giant value cannot escape a different stacking context.

`overflow: auto` adds scrolling only when needed; `hidden` clips content. A positioned element, `opacity < 1`, `transform`, and several other properties create a new stacking context.

## 5. Flexbox and Grid

Use **Flexbox for one direction** (row or column). Use **Grid for rows and columns**.

```css
.toolbar {
  display: flex;
  align-items: center;       /* cross axis */
  justify-content: space-between; /* main axis */
  gap: 1rem;
}

.cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(16rem, 1fr));
  gap: 1rem;
}
```

For flex: `flex-direction` sets the main axis; `justify-content` works on it; `align-items` works across it. `flex: 1` means an item can grow to share remaining space. `gap` adds space without outer-edge margins.

For grid: define tracks with `grid-template-columns`; place items with `grid-column`/`grid-row` only when needed. The pattern above creates as many columns as fit, then one column on narrow screens.

## 6. Typography, colors, and custom properties

Set a readable `line-height` (often `1.5`) and keep line length reasonable. Use a font stack with fallbacks. Do not set body text in viewport units alone because users must be able to zoom.

```css
:root {
  --color-brand: #1d4ed8;
  --space-md: 1rem;
}

.button {
  color: white;
  background: var(--color-brand);
  padding: 0.75rem var(--space-md);
}
```

Custom properties participate in the cascade and can change by theme or component. Ensure text/background color contrast remains accessible.

## 7. Responsive and container-aware design

Start mobile-first; add a rule when the content needs it, not for a device name.

```css
.sidebar { display: none; }

@media (min-width: 48rem) {
  .sidebar { display: block; }
}
```

- Use `:hover` plus keyboard-friendly `:focus-visible`; touch devices may not hover.
- Prefer `transition: opacity 150ms ease` rather than `transition: all`.
- Respect motion preferences:

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation-duration: 0.01ms; transition-duration: 0.01ms; }
}
```

Media queries respond to the viewport or user preference. Container queries respond to the space available to a component:

```css
.card-list { container-type: inline-size; }
@container (min-width: 32rem) {
  .card { grid-template-columns: 10rem 1fr; }
}
```

Use `max-width: 100%; height: auto` for images that must shrink. Prefer logical properties such as `margin-inline` and `padding-block` when supporting different writing directions.

## 8. Transforms, transitions, and animations

`transform` changes visual position/size without changing normal layout. `translate`, `scale`, and `rotate` are usually smoother than animating `top`, `width`, or `height`.

```css
.button { transition: transform 150ms ease; }
.button:hover { transform: translateY(-2px); }

@keyframes pulse { 50% { opacity: 0.5; } }
```

Animate `transform` and `opacity` when possible. Motion should be short, purposeful, and optional via `prefers-reduced-motion`.

## 9. Architecture, debugging, and performance

- Keep selectors shallow and component-focused. Use consistent class naming.
- Prefer normal flow, Flexbox, and Grid before absolute positioning.
- Use browser DevTools to inspect computed styles, the box model, grid/flex overlays, and crossed-out rules.
- Remove unused CSS, compress assets, and avoid enormous selector chains.
- Avoid layout-triggering animation and repeated style recalculation.
- Test responsive layouts by content breakpoints, text zoom, keyboard focus, and long/translated content.

## 10. Common mistakes

- Fixed heights that clip growing text.
- `100vw` causing horizontal overflow because it can include the scrollbar.
- Removing focus outlines.
- Using `!important` to patch unclear ownership.
- Assuming `z-index: 999999` escapes every stacking context.
- Using only color or hover to communicate state.

## Interview checklist

Explain the box model, `border-box`, cascade and specificity, normal flow, `relative`/`absolute`/`fixed`/`sticky`, Flexbox axes, Grid vs Flexbox, responsive design, and stacking contexts.
