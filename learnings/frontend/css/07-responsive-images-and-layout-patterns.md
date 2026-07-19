# 07 - Responsive Images and Reusable Layout Patterns

## Intrinsic Media

```css
img, picture, video, canvas, svg { max-inline-size: 100%; block-size: auto; }
/* Browser result: media shrinks inside its container without distortion. */
```

HTML `srcset` chooses a file; CSS controls the rendered layout.

## Aspect Ratio

```css
.thumbnail { aspect-ratio: 16 / 9; object-fit: cover; inline-size: 100%; }
/* Browser result: responsive 16:9 crop that fills its box. */
```

## Sidebar Pattern

```css
.with-sidebar { display: flex; flex-wrap: wrap; gap: 1rem; }
.with-sidebar > :first-child { flex: 1 1 16rem; }
.with-sidebar > :last-child { flex: 999 1 30rem; }
/* Browser result: sidebar and content sit together when space allows, otherwise stack. */
```

## Cluster Pattern

```css
.cluster { display: flex; flex-wrap: wrap; gap: .75rem; align-items: center; }
/* Browser result: tags/actions form a wrapping row without media queries. */
```

## Full-Bleed Content

```css
.article { display: grid; grid-template-columns: 1fr min(65ch, 100% - 2rem) 1fr; }
.article > * { grid-column: 2; }
.article > .full-bleed { grid-column: 1 / -1; }
/* Browser result: readable text column with selected full-width sections. */
```

## Responsive Tables

```css
.table-scroll { overflow-x: auto; -webkit-overflow-scrolling: touch; }
table { border-collapse: collapse; min-inline-size: 40rem; }
/* Browser result: wide table remains usable through horizontal scrolling on narrow screens. */
```

Do not change a data table into unlabelled blocks. If using a card transformation, preserve header relationships and test assistive technology.

## Content Stress Tests

Test:

- a very long name/URL
- translated text 30-100% longer
- missing/slow image
- one item and one hundred items
- empty state and error state
- 200% zoom
- right-to-left content

Responsive design means content survives these cases, not only that screenshots look good.
