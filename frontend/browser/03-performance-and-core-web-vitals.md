# 03 - Performance and Core Web Vitals in Chrome

## Performance Is User Waiting

The browser does not care that code looks elegant if the user waits for content, taps an unresponsive control, or loses their reading position because the page moves.

Measure the user experience first. Then connect it to technical work.

## The Three Core Web Vitals

The commonly used “good” thresholds are evaluated at the 75th percentile of real visits:

| Metric | What it asks | Good |
|---|---|---:|
| LCP | When did the largest important visible content finish rendering? | at most 2.5 s |
| INP | How quickly did the page show the next frame after an interaction? | at most 200 ms |
| CLS | How much unexpected layout movement occurred? | at most 0.1 |

Thresholds are product signals, not permission to stop improving. Check current official definitions when implementing organization-wide policy because metrics and tooling evolve.

## Field Data vs Lab Data

- **field data:** real users, devices, networks, locations, caches, and sessions
- **lab data:** controlled repeatable test environment

Field data tells you whether users have a problem. Lab data helps reproduce and diagnose it.

Do not claim a production improvement from one Lighthouse run on a fast laptop.

## Largest Contentful Paint

LCP often points to a hero image, heading block, or large text/content element.

Break the time into questions:

1. When did the initial document respond?
2. When did Chrome discover the LCP resource?
3. How long did the resource take to download?
4. How long did rendering wait after the resource arrived?

Common fixes by cause:

- slow document: improve server/cache/edge work
- late discovery: put the resource in initial HTML or preload only when justified
- oversized image: correct dimensions, format, compression, and responsive source
- render delay: reduce blocking CSS/JavaScript and main-thread work

Responsive image example:

```html
<img
  src="hero-960.webp"
  srcset="hero-640.webp 640w, hero-960.webp 960w, hero-1600.webp 1600w"
  sizes="(min-width: 70rem) 60rem, 100vw"
  width="1600"
  height="900"
  fetchpriority="high"
  alt="Learner building a frontend project">
```

Use `fetchpriority="high"` only for a genuinely important early resource. Do not lazy-load the LCP image.

## Interaction to Next Paint

INP considers interaction latency throughout a page visit. A slow interaction can contain:

- input delay: earlier main-thread work blocks the event
- processing time: event handlers run
- presentation delay: style, layout, paint, and frame scheduling occur

Record the slow interaction in Performance. Expand the event and main-thread task. Use Bottom-Up or Call Tree to find expensive functions.

Break long CPU work into smaller tasks only when the operation can safely yield. Better fixes often remove unnecessary work, render fewer items, or move pure heavy computation to a worker.

Yielding example for non-urgent batch work:

```javascript
async function processInBatches(items, processItem, batchSize = 100) {
  if (!Array.isArray(items)) throw new TypeError("items must be an array");
  for (let start = 0; start < items.length; start += batchSize) {
    for (const item of items.slice(start, start + batchSize)) processItem(item);
    await new Promise((resolve) => setTimeout(resolve, 0));
  }
}
```

This allows other tasks between batches. It is not a free speed improvement: total work remains. Prefer `scheduler.yield()` only after checking support and providing the required compatibility policy.

## Cumulative Layout Shift

CLS measures unexpected movement, not all movement.

Common causes:

- images or embeds without dimensions
- late banners inserted above content
- font changes that alter text geometry
- animations of layout properties
- content that changes size after loading

Reserve space:

```css
.video-frame { aspect-ratio: 16 / 9; }
.notice-slot { min-block-size: 3rem; }
```

```html
<img src="course.webp" width="800" height="450" alt="Course dashboard">
```

Use Performance trace layout-shift entries and Rendering > Layout Shift Regions to identify the moving element and the earlier change that caused it.

## Read a Performance Trace

1. Open Performance.
2. Choose realistic CPU/network settings.
3. Record and reload for load analysis, or record one interaction.
4. Stop as soon as the important behavior completes.
5. Use screenshots and timings to locate the visible delay.
6. Inspect Network, Main, Frames, and Experience tracks around that time.
7. Select a long task and inspect Summary, Bottom-Up, Call Tree, and Event Log.
8. Ignore unrelated work outside the reproduction window.

Look for:

- long purple style/layout work
- long yellow scripting work
- repeated layout forced by JavaScript
- large green paint work
- request waterfalls
- layout-shift markers
- third-party execution

Colors and UI details can change; rely on labels and event names, not color alone.

## Forced Synchronous Layout

This pattern can force repeated layout because it writes, then immediately reads geometry in a loop:

```javascript
for (const item of items) {
  item.style.width = `${item.offsetWidth + 1}px`;
}
```

Batch reads before writes:

```javascript
const widths = items.map((item) => item.offsetWidth);
items.forEach((item, index) => {
  const width = widths[index];
  if (width === undefined) throw new RangeError("missing measured width");
  item.style.width = `${width + 1}px`;
});
```

Prefer CSS layout when the goal is purely visual.

## JavaScript and Bundle Cost

Downloaded bytes are only part of cost. JavaScript must be decompressed, parsed, compiled, and executed.

Use:

- Network for transfer and resource size
- Coverage for used code during one tested flow
- a bundle visualizer for module composition
- Performance for parse/compile/execute impact

Split at meaningful routes or features. Do not create hundreds of tiny chunks without measuring request and execution behavior.

## Fonts

- load only used families, weights, styles, and scripts
- prefer modern compressed formats
- subset when product language support permits it
- use a deliberate `font-display` choice
- preload only fonts needed immediately
- test layout shift and readability during fallback

## Performance Budgets

A budget makes regression visible. Example categories:

- maximum initial JavaScript bytes
- maximum image bytes for a route
- maximum number of critical requests
- lab LCP/INP/CLS targets under a named profile
- real-user percentile targets

Budgets need an owner, measurement environment, and CI or release response.

## Measure in Code

```javascript
performance.mark("course-render-start");
renderCourses();
performance.mark("course-render-end");
performance.measure("course-render", "course-render-start", "course-render-end");

const entry = performance.getEntriesByName("course-render").at(-1);
if (!entry) throw new Error("course-render measurement is missing");
console.log(entry.duration);
```

Marks measure your named operation. They do not replace user-centric metrics.

## Optimization Order

1. fix correctness and accessibility
2. reproduce on representative hardware and network
3. identify the user-visible delay
4. remove unnecessary work or bytes
5. improve discovery, scheduling, or caching
6. compare before and after under the same conditions
7. watch field data for regressions
