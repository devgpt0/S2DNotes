# 06 - How Browsers Load HTML, Performance, and Security

## Navigation Steps

Simplified browser journey:

1. Parse the URL.
2. Resolve DNS.
3. Establish network and TLS connections.
4. Send an HTTP request.
5. Receive response headers and bytes.
6. Decode and parse HTML into the DOM.
7. Discover CSS, JavaScript, fonts, and images.
8. Build CSSOM/render tree, calculate layout, paint, and composite.

## Parser-Blocking Scripts

```html
<script src="legacy.js"></script>
<!-- Browser behavior: HTML parsing normally pauses while this classic script downloads and runs. -->
```

Modern choices:

```html
<script src="app.js" defer></script>
<script type="module" src="module.js"></script>
<!-- Browser behavior: both download without blocking parsing and execute after the document is parsed. -->
```

`async` executes as soon as download finishes, so order is not guaranteed. Use it for independent scripts.

## Resource Hints

```html
<link rel="preconnect" href="https://fonts.example.com" crossorigin>
<link rel="preload" href="hero.avif" as="image" fetchpriority="high">
<!-- Browser behavior: prepares an important origin and prioritizes the known hero image. -->
```

Too many preloads compete with truly critical resources.

## Core Web Vitals

- LCP: how quickly the largest important content appears
- INP: responsiveness to user interactions
- CLS: unexpected visual movement

Improve them with appropriately sized images, reserved dimensions, minimal render-blocking work, small JavaScript, fast server responses, and avoiding late inserted content above existing content.

## Browser Caching

Versioned static assets can use long cache lifetimes. HTML usually needs shorter/revalidation behavior so users discover new asset filenames.

## Security Boundaries

- same-origin policy restricts cross-origin reads
- CORS is a server permission mechanism, not authentication
- CSP limits approved script/style/resource sources
- Subresource Integrity verifies selected third-party assets
- sandboxed iframes restrict embedded content

```html
<iframe src="https://untrusted.example" sandbox="allow-scripts" title="Embedded demo"></iframe>
<!-- Browser behavior: scripts are allowed, but many other iframe capabilities remain restricted. -->
```

## DevTools Lessons

- Elements: inspect DOM and accessibility tree
- Network: find blocking, large, uncached, or failed resources
- Performance: inspect scripting, layout, paint, and long tasks
- Lighthouse: automated starting point, not proof of quality
- Coverage: find unused CSS/JavaScript during the recorded flow

Always test real mobile devices and slower CPU/network profiles, not only a wide desktop.
