# CSS Concepts in Simple Words

## The One-Sentence Idea

CSS matches HTML elements and gives them visual/layout rules. The browser resolves competing rules, calculates geometry, paints pixels, and composites layers.

## The Five Concepts Everything Uses

1. **Cascade:** which competing declaration wins.
2. **Box model:** content, padding, border, and margin.
3. **Normal flow:** default placement before special layouts.
4. **Layout system:** Flexbox, Grid, positioning, and intrinsic sizing.
5. **Responsive behavior:** content adapts to available space and user preferences.

```css
.card {
  box-sizing: border-box;
  inline-size: min(100%, 24rem);
  padding: 1rem;
  border: 1px solid #ccc;
}
/* Browser result: card includes padding/border in a width capped at 24rem. */
```

## Browser Rendering in Plain Language

```text
match CSS -> compute values -> layout boxes -> paint -> composite layers
# Result: some changes affect only pixels/layers; others force geometry recalculation.
```

## Flexbox vs Grid

- Flexbox answers: how should items share one row or column?
- Grid answers: how should items align across rows and columns?
- Normal flow remains best for ordinary document text.

## Responsive Formula

Responsive design is not “add three device breakpoints.” Use:

- fluid widths with maximums
- wrapping Flex/Grid
- responsive media
- content-based breakpoints
- container queries for portable components
- user preference queries
- long-content, zoom, keyboard, RTL, and real-device tests

## Debugging Order

1. Is selector matching?
2. Did cascade/specificity/layer override it?
3. What is the computed value?
4. What containing block/formatting context applies?
5. Is intrinsic minimum size causing overflow?
6. Is a stacking context trapping z-index?
7. Does target browser support the feature?
