# 09 - Modern CSS and Architecture

## Custom Properties

```css
:root {
  --color-brand: oklch(45% .18 260);
  --space-3: .75rem;
}
.button { background: var(--color-brand); padding: var(--space-3); }
/* Browser result: button uses shared brand and spacing design tokens. */
```

Custom properties participate in cascade and can change at runtime. Sass variables are resolved during compilation.

## Logical Properties

```css
.card { margin-inline: auto; padding-block: 1rem; border-inline-start: .25rem solid; }
/* Browser result: spacing/border adapt to left-to-right, right-to-left, and writing mode. */
```

## CSS Functions

```css
.panel {
  inline-size: min(100%, 60rem);
  padding: clamp(1rem, 2vw, 2rem);
  color: color-mix(in oklch, navy 80%, white);
}
/* Browser result: bounded width, fluid padding, and mixed color in supporting browsers. */
```

Useful functions include `min`, `max`, `clamp`, `calc`, `var`, and modern color functions.

## Feature Queries

```css
.gallery { display: flex; flex-wrap: wrap; }
@supports (display: grid) {
  .gallery { display: grid; grid-template-columns: repeat(3, 1fr); }
}
/* Browser result: flex fallback; Grid enhancement when supported. */
```

## Architecture

A practical order:

1. reset/normalization
2. tokens/custom properties
3. base elements
4. layout objects
5. components
6. utilities
7. carefully scoped overrides

Use cascade layers, predictable class names, component ownership, and low specificity. Avoid selectors tied to fragile DOM depth.

## CSS Nesting

Modern CSS supports nesting in current browsers, but keep nesting shallow.

```css
.card {
  padding: 1rem;
  & > h2 { margin-block-start: 0; }
}
/* Browser result: only direct h2 children inside card lose their top margin. */
```

Use SCSS when its module system, functions, or build-time generation provides real value—not merely for nesting.
