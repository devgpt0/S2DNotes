# 04 - Generated CSS, Optimization, and Common SCSS Mistakes

## Inspect Generated CSS

Developers write SCSS, but users download CSS. Always inspect source maps, selectors, duplication, and final compressed size.

```powershell
npx sass --style=compressed src/styles/main.scss dist/styles.min.css
# Result: emits compressed production CSS; minification does not remove unused selectors automatically.
```

## Avoid Selector Explosion

```scss
.page {
  .content {
    .article {
      .card { color: #222; }
    }
  }
}
// Compiled selector: .page .content .article .card (too coupled and unnecessarily specific).
```

Prefer a direct `.card` component selector.

## Avoid Large Loop Output

A loop over many properties, breakpoints, colors, and values can generate thousands of classes. Estimate combinations before generating them.

## Do Not Replace CSS Features

- runtime theme -> CSS custom properties
- responsive layout -> Grid/Flex/container queries
- simple nesting -> native CSS nesting may be enough
- cascade control -> CSS layers
- color mixing -> modern CSS color functions where supported

## Source Maps

Use source maps in development so DevTools maps generated rules to `.scss`. Decide whether production source maps are public, private to error tooling, or omitted based on debugging and source exposure requirements.

## Browser Compatibility

Sass syntax support is unrelated to browser support of the CSS it produces. A mixin can generate unsupported CSS. Use compatibility data and Autoprefixer/build targets.

## Common Mistakes

- deprecated `@import` and global built-in functions
- variables for values that need runtime theming
- deep nesting
- broad `%placeholder` extends
- mixins that duplicate large declaration blocks
- one giant global stylesheet with unclear ownership
- trusting compilation as proof the CSS works in target browsers
