# 02 - Semantic HTML and Accessibility

## What Does Semantic Mean?

Semantic elements describe purpose. `button` means an action; a styled `div` does not. Correct elements provide keyboard and accessibility behavior for free.

## Page Landmarks

```html
<header>Site header</header>
<nav aria-label="Main navigation"><a href="/courses">Courses</a></nav>
<main>
  <article>
    <h1>Accessible HTML</h1>
    <section><h2>Why it matters</h2><p>Everyone can use the page.</p></section>
  </article>
</main>
<footer>Copyright information</footer>
<!-- Browser result: meaningful header, navigation, main, article, section, and footer landmarks. -->
```

Other useful elements: `aside`, `figure`, `figcaption`, `address`, `details`, and `summary`.

## Button vs Link

- Link navigates to another location.
- Button performs an action on the current page.

```html
<a href="/profile">Open profile</a>
<button type="button" id="save">Save changes</button>
<!-- Browser result: Enter activates the link; Enter or Space activates the button. -->
```

Never use `href="#"` as a fake button or add click behavior to a plain `div`.

## Images and Alternative Text

```html
<img src="team.jpg" alt="Four developers reviewing a design diagram">
<img src="decorative-line.svg" alt="">
<!-- Accessibility result: the meaningful image is described; the decorative image is ignored. -->
```

Alternative text describes purpose in context, not every visual detail. Do not begin with “image of.”

## Labels and Accessible Names

```html
<label for="email">Email address</label>
<input id="email" name="email" type="email" autocomplete="email">
<!-- Browser result: clicking the label focuses the field; assistive technology announces its name. -->
```

Placeholder text is not a label because it disappears and often has poor contrast.

## Keyboard and Focus

- all interactive controls must be reachable with Tab
- focus order should follow DOM order
- never remove the focus outline without a clear replacement
- avoid positive `tabindex` values
- Escape should close dialogs/menus when expected
- return focus logically after closing a dialog

## ARIA Rule

Use native HTML first. ARIA can add missing name, state, or relationship information, but it does not automatically add keyboard behavior.

```html
<button aria-expanded="false" aria-controls="menu">Menu</button>
<ul id="menu" hidden><li><a href="/home">Home</a></li></ul>
<!-- Accessibility result: the button exposes the controlled menu and its collapsed state. -->
```

JavaScript must update `aria-expanded` and `hidden` together when the menu changes.

## Expert Checklist

Test zoom to 200%, keyboard-only use, screen-reader names/landmarks, color contrast, reduced motion, error announcements, and touch target size. Automated audits help but cannot prove usability.
