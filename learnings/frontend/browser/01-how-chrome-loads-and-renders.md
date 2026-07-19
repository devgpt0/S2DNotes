# 01 - How Chrome Turns a URL into Pixels

## Start with the Big Picture

When you enter a URL, Chrome must get bytes, understand them, create a page, and draw pixels.

```text
URL
 -> network request
 -> HTML bytes
 -> DOM
 -> CSSOM
 -> render tree
 -> layout
 -> paint
 -> compositing
 -> pixels
```

JavaScript can run during this process and can change the DOM, styles, requests, and timing.

## 1. Find the Server

For an HTTPS URL, the browser normally performs work such as:

1. check caches and service-worker rules
2. resolve the host name through DNS when needed
3. create a network connection
4. negotiate TLS security
5. send the HTTP request
6. wait for response headers and bytes

Connection reuse, HTTP version, proxy rules, caches, and network conditions can change the exact sequence.

In Chrome DevTools, Network > Timing shows phases for an individual request. A long “Waiting for server response” period is not fixed by changing CSS.

## 2. Parse HTML into the DOM

Chrome reads HTML and creates the **Document Object Model**, or DOM.

```html
<main>
  <h1>Java course</h1>
</main>
```

The DOM is an object tree representing document structure. It is not a screenshot and it is not the original source text.

The parser may discover more resources:

- stylesheets
- scripts
- images
- fonts
- module imports

Resource discovery order affects the network waterfall.

## 3. Parse CSS into the CSSOM

Chrome parses applicable CSS rules and builds information used to calculate each element's style.

```css
h1 { color: royalblue; }
```

The final style can depend on origin, importance, layer, specificity, scoping, source order, inheritance, media queries, container queries, and supported features.

Elements > Styles explains which rule won. Elements > Computed shows the final value.

## 4. Run JavaScript

A normal blocking script can pause HTML parsing while it downloads and runs:

```html
<script src="app.js"></script>
```

Common choices:

```html
<script defer src="app.js"></script>
<script type="module" src="app.js"></script>
<script async src="analytics.js"></script>
```

- `defer`: download while parsing; run after HTML parsing, in document order
- module: deferred by default and follows module dependency rules
- `async`: run as soon as ready; order relative to other async scripts is not guaranteed

Choose from dependency and timing needs. Do not apply `async` to code that requires earlier DOM or script order.

## 5. Build What Can Be Rendered

The browser combines DOM structure and calculated styles into information needed for visible content.

Some DOM nodes do not create a visible box, such as metadata or elements with `display: none`.

## 6. Layout: Decide Size and Position

Layout calculates geometry: where boxes are and how large they are.

Changes to width, font metrics, content, or layout rules can trigger new layout work.

Responsive CSS is layout work done by the browser. Prefer CSS Grid, Flexbox, intrinsic sizing, media queries, and container queries over JavaScript measuring every element.

## 7. Paint: Create Drawing Instructions

Paint records how backgrounds, borders, text, shadows, and other visual parts should be drawn.

A change may require repaint without changing layout. Paint flashing in the Rendering panel helps show repainted regions.

## 8. Compositing: Assemble Layers

Chrome may place content into composited layers and let the compositor combine them.

Transforms and opacity can often update without layout or repainting page content. That does not mean every element should receive `will-change` or its own layer. Layers consume memory and have management cost.

## A Frame Budget

At a 60 Hz display, one frame lasts about 16.7 ms. Browser and system work also need time, so application main-thread work must stay comfortably below that to animate smoothly.

A task longer than 50 ms is called a **long task**. It can delay input and rendering.

## Critical Rendering Path in Simple Words

The critical rendering path is the work required to show the current view.

Common delays include:

- slow HTML response
- render-blocking CSS
- large or synchronous JavaScript
- late fonts or hero images
- request chains where one resource reveals the next
- expensive style, layout, or paint work

The correct fix depends on the measured delay.

## Browser Processes and Threads

Chrome uses multiple processes for isolation and reliability. A simplified view includes:

- browser process: tabs, navigation, permissions, and coordination
- renderer process: web content for a site or isolated frame
- network service: requests and cache behavior
- GPU process: accelerated drawing and compositing work

Inside a renderer, important work includes the main thread, compositor work, and worker threads.

JavaScript, style, layout, and much DOM work use the main thread. A Web Worker can run JavaScript away from the main thread but cannot directly edit the DOM.

## A Small Experiment

Create this page and record a Performance trace while clicking the button:

```html
<!doctype html>
<html lang="en">
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Render experiment</title>
  <button id="move">Move box</button>
  <div id="box" style="width:100px;height:100px;background:royalblue"></div>
  <script>
    const button = document.querySelector("#move");
    const box = document.querySelector("#box");
    if (!(button instanceof HTMLButtonElement) || !(box instanceof HTMLDivElement)) {
      throw new Error("required elements are missing");
    }
    button.addEventListener("click", () => {
      box.style.transform = "translateX(100px)";
    });
  </script>
</html>
```

In the trace, find the click event, JavaScript work, rendering update, and resulting frame.

## Quick Memory Card

- DOM: document structure
- CSSOM/style calculation: which styles apply
- layout: size and position
- paint: drawing instructions
- compositing: assemble layers into a frame
- main-thread blocking can delay both input and pixels
- measure the slow stage before choosing a fix
