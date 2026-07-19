# 05 - CSS Grid

Grid controls rows and columns together. It is ideal for page shells, galleries, dashboards, and aligned card layouts.

## Responsive Card Grid

```css
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 16rem), 1fr));
  gap: 1rem;
}
/* Browser result: as many 16rem cards as fit; one safe column on narrow screens. */
```

`auto-fit` collapses empty tracks; `auto-fill` can retain them.

## Explicit Placement

```css
.layout {
  display: grid;
  grid-template-columns: 15rem minmax(0, 1fr);
  grid-template-areas: "sidebar content";
  gap: 1.5rem;
}
.sidebar { grid-area: sidebar; }
.content { grid-area: content; }
/* Browser result: two-column named layout with a fixed sidebar and flexible content. */
```

## Responsive Change

```css
@media (max-width: 48rem) {
  .layout {
    grid-template-columns: 1fr;
    grid-template-areas: "content" "sidebar";
  }
}
/* Browser result below 48rem: content and sidebar stack in the declared visual areas. */
```

Remember that visual placement does not change DOM reading/focus order.

## Alignment

- `justify-items`: align items inside tracks on inline axis
- `align-items`: align items inside tracks on block axis
- `place-items`: shorthand for both
- `justify-content`/`align-content`: align the whole grid when extra container space exists

## Subgrid

```css
.card { display: grid; grid-template-rows: subgrid; grid-row: span 3; }
/* Browser result in supporting browsers: nested card rows align to parent grid tracks. */
```

Check compatibility and provide an acceptable non-subgrid fallback.

## Flexbox vs Grid

- Flexbox: content-driven layout primarily along one axis
- Grid: layout-driven control across rows and columns
- They work well together; Grid for page/cards, Flexbox inside a card is common
