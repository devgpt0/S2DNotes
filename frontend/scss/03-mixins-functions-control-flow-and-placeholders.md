# 03 - SCSS Mixins, Functions, Control Flow, and Placeholders

## Mixin

A mixin generates declarations and can accept arguments.

```scss
@mixin focus-ring($color: royalblue) {
  outline: .2rem solid $color;
  outline-offset: .2rem;
}
.button:focus-visible { @include focus-ring(); }
// Compiled result: .button:focus-visible receives the two outline declarations.
```

Mixins duplicate their generated declarations at each include. Keep them purposeful.

## Function

A function returns a value.

```scss
@use "sass:math";
@function rem($pixels, $base: 16) {
  @return math.div($pixels, $base) * 1rem;
}
.title { font-size: rem(32); }
// Compiled result: .title { font-size: 2rem; }
```

Use built-in modules such as `sass:math`, `sass:color`, `sass:map`, and `sass:list` instead of deprecated global functions.

## Maps and Loops

```scss
$spaces: (1: .25rem, 2: .5rem, 4: 1rem);
@each $name, $value in $spaces {
  .p-#{$name} { padding: $value; }
}
// Compiled result: .p-1, .p-2, and .p-4 utility classes.
```

Generated class sets must be finite and actually used; otherwise CSS size grows quickly.

## Conditions

```scss
@mixin theme($dark: false) {
  @if $dark { color: white; background: #111; }
  @else { color: #111; background: white; }
}
.panel { @include theme(true); }
// Compiled result: dark panel declarations.
```

## Placeholder and Extend

```scss
%control { border: 1px solid #777; border-radius: .25rem; }
.input { @extend %control; }
.select { @extend %control; }
// Compiled result: .input, .select share one grouped declaration rule.
```

`@extend` can create surprising combined selectors across modules. A mixin or shared class is often easier to predict.
