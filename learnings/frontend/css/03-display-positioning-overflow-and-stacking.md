# 03 - Display, Positioning, Overflow, and Stacking

## Normal Flow and Display

- block elements usually start a new line and fill available inline space
- inline elements flow within text and ignore some box sizing behavior
- inline-block flows inline but accepts width/height
- flex/grid create layout formatting contexts
- `display: none` removes rendering and accessibility-tree presence

```css
.badge { display: inline-block; padding: .25rem .5rem; }
/* Browser result: badge sits within text but behaves like a box. */
```

## Positioning

```css
.card { position: relative; }
.badge { position: absolute; inset-block-start: .5rem; inset-inline-end: .5rem; }
/* Browser result: badge is anchored to the card's top logical end corner. */
```

- static: normal default
- relative: stays in flow and becomes containing block for positioned descendants
- absolute: removed from normal flow and positioned against a containing block
- fixed: positioned against viewport (with some transform-related exceptions)
- sticky: behaves relative until a scroll threshold, then sticks within its scroll container

```css
.toolbar { position: sticky; inset-block-start: 0; z-index: 10; }
/* Browser result: toolbar sticks to the top while its container scrolls. */
```

Sticky can fail when an ancestor's overflow or available scroll area prevents it.

## Overflow

```css
.table-wrapper { overflow-x: auto; overscroll-behavior-inline: contain; }
/* Browser result: wide tables scroll horizontally without widening the page. */
```

Avoid hiding overflow merely to conceal a broken layout.

## Stacking Contexts

`z-index` compares elements inside stacking contexts, not across the entire page. New contexts can be created by positioned elements with z-index, transforms, opacity, isolation, and other properties.

```css
.modal-layer { position: fixed; inset: 0; z-index: 100; isolation: isolate; }
/* Browser result: a full-viewport modal layer with its own predictable stacking context. */
```

If `z-index: 999999` fails, inspect ancestor stacking contexts instead of increasing the number.

## Visually Hidden Content

```css
.sr-only {
  position: absolute;
  inline-size: 1px;
  block-size: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip-path: inset(50%);
  white-space: nowrap;
  border: 0;
}
/* Accessibility result: content remains available to screen readers but is visually hidden. */
```
