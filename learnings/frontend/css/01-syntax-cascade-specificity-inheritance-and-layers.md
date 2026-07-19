# 01 - CSS Syntax, Cascade, Specificity, Inheritance, and Layers

## Rule Anatomy

```css
.notice {
  color: navy;
  font-weight: 700;
}
/* Browser result: every element with class="notice" becomes bold navy text. */
```

The selector chooses elements. Each declaration has a property and value.

## Selectors

```css
p { color: #222; }                 /* type */
.card { padding: 1rem; }           /* class */
#main-title { line-height: 1.2; }   /* ID */
nav a { text-decoration: none; }    /* descendant */
button:hover { background: navy; }  /* pseudo-class */
input[required] { border-color: red; } /* attribute */
/* Browser result: each rule targets the element pattern described by its selector. */
```

Prefer classes and low-specificity selectors for reusable styling.

## The Cascade

When declarations compete, the browser considers:

1. origin and importance
2. cascade layer
3. specificity
4. scoping proximity where applicable
5. source order

```html
<p class="message">Hello</p>
<style>
  p { color: blue; }
  .message { color: green; }
</style>
<!-- Browser result: green, because the class selector is more specific. -->
```

## Specificity

Rough comparison: inline styles > IDs > classes/attributes/pseudo-classes > elements/pseudo-elements. `:where()` always has zero specificity.

Avoid `!important` as a normal solution; it makes later overrides harder.

## Inheritance

Text properties such as `color` and `font-family` usually inherit. Layout properties such as margin, border, and width usually do not.

```css
body { color: #222; font-family: system-ui, sans-serif; }
button { font: inherit; }
/* Browser result: page text inherits body styles; buttons explicitly inherit the complete font. */
```

Use `inherit`, `initial`, `unset`, or `revert` deliberately when resetting values.

## Cascade Layers

```css
@layer reset, base, components, utilities;

@layer base { a { color: blue; } }
@layer components { .button { color: white; background: navy; } }
/* Browser result: later layers outrank earlier layers regardless of selector specificity within different layers. */
```

Layers help control third-party, base, component, and utility CSS without specificity wars.

## DevTools Tip

In Elements > Styles/Computed, crossed-out declarations lost the cascade. Inspect why before adding a stronger selector.
