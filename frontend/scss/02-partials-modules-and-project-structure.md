# 02 - SCSS Partials, Modules, and Project Structure

## Modules

`@use` loads a Sass module once and namespaces its members. Prefer it over deprecated `@import`.

```scss
// _tokens.scss
$brand: royalblue;
$space-4: 1rem;

// main.scss
@use "tokens";
.button { color: tokens.$brand; padding: tokens.$space-4; }
// Compiled result: .button uses royalblue and 1rem; the partial itself creates no duplicate import.
```

Files beginning with `_` are partials and normally compile only through an entry file.

## Configure a Module

```scss
// _theme.scss
$brand: navy !default;

// main.scss
@use "theme" with ($brand: rebeccapurple);
.link { color: theme.$brand; }
// Compiled result: .link { color: rebeccapurple; }
```

Configuration must occur the first time a module is loaded.

## Forward a Public API

```scss
// design-system/_index.scss
@forward "tokens";
@forward "mixins";

// main.scss
@use "design-system" as ds;
// Result: consumers access the intentionally forwarded design-system members through ds.
```

## Suggested Structure

```text
styles/
|-- abstracts/   # tokens, functions, mixins (normally no CSS output)
|-- base/        # reset, typography, base elements
|-- layout/      # page/grid layout
|-- components/  # buttons, cards, forms
|-- utilities/   # focused helper classes
`-- main.scss    # entry point using the modules
# Result: source ownership is clear and only main.scss is compiled as the main bundle.
```

## Architecture Rules

- one or a few intentional entry files
- modules expose a small public API
- do not create a partial for every three lines
- keep component styles close to component ownership
- use CSS custom properties for runtime theming
- use cascade layers if generated CSS must coexist with vendor/utilities
