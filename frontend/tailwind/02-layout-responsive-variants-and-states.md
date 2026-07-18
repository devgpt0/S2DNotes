# 02 - Tailwind Layout, Responsive Variants, and States

## Flex and Grid

```html
<div class="flex items-center gap-4">
  <span>Logo</span><nav class="ms-auto">Navigation</nav>
</div>

<div class="grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-4">
  <article>Card 1</article><article>Card 2</article>
</div>
<!-- Browser result: flex toolbar; cards use 1, 2, then 4 columns at configured breakpoints. -->
```

Tailwind is mobile-first: unprefixed utilities apply everywhere; `md:` applies at medium width and above.

## Responsive Container

```html
<main class="mx-auto w-full max-w-6xl px-4 sm:px-6 lg:px-8">Content</main>
<!-- Browser result: centered bounded content with increasing side padding. -->
```

## States

```html
<input class="border p-2 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-700 disabled:cursor-not-allowed disabled:opacity-50">
<!-- Browser result: visible keyboard focus and clear disabled appearance. -->
```

Variants include `hover`, `focus`, `focus-visible`, `active`, `disabled`, `checked`, `invalid`, `group-*`, `peer-*`, and responsive/preference variants.

## Group and Peer

```html
<label class="group block">
  <span class="group-focus-within:text-blue-700">Email</span>
  <input class="peer border invalid:border-red-600">
  <span class="hidden text-red-700 peer-invalid:block">Enter a valid email.</span>
</label>
<!-- Browser result: label reacts to focus; validation message appears when input is invalid. -->
```

CSS display is not a replacement for correct accessible error announcement and server validation.

## Container Queries

```html
<div class="@container">
  <article class="grid gap-4 @md:grid-cols-[10rem_1fr]">Responsive component</article>
</div>
<!-- Browser result: article changes layout based on its container's width. -->
```

Use variants only when the underlying CSS behavior is understood.
