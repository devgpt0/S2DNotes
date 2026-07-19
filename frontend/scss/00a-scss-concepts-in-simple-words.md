# SCSS Concepts in Simple Words

## The One-Sentence Idea

SCSS is developer-facing source code that Sass compiles into ordinary CSS. The browser never runs SCSS.

```text
.scss modules -> Sass compiler -> .css -> browser
# Result: Sass features disappear or become CSS rules/values during the build.
```

## What Sass Adds

- build-time variables
- modules and controlled namespaces
- mixins that emit declarations/rules
- functions that return values
- loops/conditions for finite generated CSS
- parent selector and extended nesting

## Sass vs Modern CSS

| Need | Prefer |
|---|---|
| runtime theme | CSS custom properties |
| responsive layout | CSS Grid/Flex/container queries |
| module namespace/calculation | Sass |
| finite generated utilities | Sass carefully |
| simple nesting | native CSS may be enough |
| cascade ordering | CSS layers |

## Small Example

```scss
@use "sass:color";
$brand: royalblue;
.button {
  background: $brand;
  &:hover { background: color.adjust($brand, $lightness: 8%); }
}
// Compiled result: normal .button and .button:hover CSS rules with concrete colors.
```

## Beginner Decision Rule

Before writing SCSS, ask: what CSS should the browser receive? If generated output is hard to predict, simplify the SCSS.
