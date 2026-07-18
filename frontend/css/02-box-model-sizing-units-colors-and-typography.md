# 02 - Box Model, Sizing, Units, Colors, and Typography

## Box Model

Every visible element has content, padding, border, and margin.

```css
*, *::before, *::after { box-sizing: border-box; }
.card { width: 300px; padding: 20px; border: 2px solid; }
/* Browser result: total card width remains 300px because padding and border are included. */
```

With default `content-box`, the same card would be 344px wide.

## Sizing Safely

```css
.content {
  width: min(100% - 2rem, 70rem);
  margin-inline: auto;
}
img { max-inline-size: 100%; block-size: auto; }
/* Browser result: centered content never exceeds 70rem or touches narrow viewport edges; images shrink safely. */
```

Prefer `min/max-inline-size` and `min/max-block-size` when writing direction should be respected.

## Units

- `px`: CSS pixel; useful for borders and exact small values
- `rem`: relative to root font size; useful for spacing/type
- `em`: relative to current element font size
- `%`: relative to a containing/reference value
- `vw`, `vh`, `dvh`: viewport-related
- `ch`: approximate width of the `0` glyph; useful for readable lines
- `fr`: Grid fraction of remaining space

```css
.article { max-inline-size: 65ch; padding: 1rem; }
/* Browser result: readable line length and spacing that respects the user's root font setting. */
```

Use `dvh` for dynamic mobile viewport height when browser controls appear/disappear.

## Fluid Typography

```css
h1 { font-size: clamp(2rem, 1rem + 4vw, 4rem); }
/* Browser result: heading grows fluidly from 2rem to 4rem without becoming too small or large. */
```

## Colors

```css
:root { color-scheme: light dark; }
.status { color: hsl(145 65% 25%); background: hsl(145 60% 92%); }
/* Browser result: accessible green status styling; actual contrast must be measured. */
```

Modern CSS also supports `oklch()`, which is useful for perceptually consistent palettes. Provide fallback when supporting older browsers.

## Typography Tips

- use a system font stack or efficiently subset web fonts
- set comfortable `line-height` around 1.4-1.7 for body text
- limit line length around 45-75 characters
- never disable user zoom
- avoid tiny fixed text
- preload only a truly critical font and use `font-display`

```css
body { font: 1rem/1.6 system-ui, sans-serif; }
h1, h2 { line-height: 1.15; text-wrap: balance; }
p { text-wrap: pretty; }
/* Browser result: readable body rhythm and improved heading/paragraph wrapping in supporting browsers. */
```
