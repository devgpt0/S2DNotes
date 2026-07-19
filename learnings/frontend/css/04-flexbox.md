# 04 - Flexbox

Flexbox lays out items along one main axis. It is ideal for navigation bars, aligned controls, toolbars, and component rows/columns.

## Container and Items

```css
.toolbar {
  display: flex;
  align-items: center;
  gap: 1rem;
}
.toolbar__actions { margin-inline-start: auto; }
/* Browser result: items align vertically; actions move to the far logical end. */
```

## Main vs Cross Axis

With `flex-direction: row`, main axis is inline/horizontal in common left-to-right writing. `justify-content` controls main-axis distribution; `align-items` controls cross-axis alignment.

```css
.center {
  display: flex;
  justify-content: center;
  align-items: center;
  min-block-size: 15rem;
}
/* Browser result: child is centered on both axes. */
```

## Grow, Shrink, Basis

`flex` combines grow, shrink, and basis.

```css
.sidebar { flex: 0 0 16rem; }
.main { flex: 1 1 30rem; min-inline-size: 0; }
/* Browser result: fixed 16rem sidebar and flexible main area that may shrink without text overflow. */
```

`min-inline-size: 0` often fixes overflowing flex children because their automatic minimum can otherwise preserve long content width.

## Wrapping Cards

```css
.cards { display: flex; flex-wrap: wrap; gap: 1rem; }
.card { flex: 1 1 16rem; }
/* Browser result: cards grow, shrink, and wrap when roughly below 16rem each. */
```

## Ordering Warning

CSS `order` changes visual order but not DOM, keyboard, or screen-reader order. Keep DOM order meaningful.

## Common Mistakes

- using flex when two-dimensional row/column alignment needs Grid
- adding widths to every child instead of using flexible basis
- forgetting wrapping
- using `space-between` for layouts where a fixed `gap` is more predictable
- hiding overflow instead of setting correct minimum sizing
