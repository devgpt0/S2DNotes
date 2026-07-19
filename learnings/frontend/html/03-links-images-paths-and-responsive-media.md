# 03 - Links, Images, Paths, and Responsive Media

## Relative and Absolute URLs

```html
<a href="about.html">Same folder</a>
<a href="../index.html">Parent folder</a>
<a href="/courses/html">Root-relative path</a>
<a href="https://example.com">Absolute URL</a>
<!-- Browser result: each link resolves from a different base location. -->
```

Use forward slashes in web URLs. File-system paths such as `C:\images\photo.jpg` do not work for website visitors.

## Useful Link Attributes

```html
<a href="guide.pdf" download>Download guide</a>
<a href="https://external.example" target="_blank" rel="noopener">External site</a>
<a href="mailto:team@example.com">Email the team</a>
<!-- Browser result: download, safe new tab, and email-client actions. -->
```

Avoid opening new tabs unexpectedly unless the context justifies it.

## Image Dimensions and Loading

```html
<img
  src="course-800.jpg"
  width="800"
  height="450"
  loading="lazy"
  decoding="async"
  alt="Student building a responsive webpage">
<!-- Browser result: reserved 16:9 space prevents layout shift; off-screen loading is delayed. -->
```

Do not lazy-load the main above-the-fold hero image because it may delay the largest visible content.

## Responsive Images

```html
<img
  src="photo-800.jpg"
  srcset="photo-480.jpg 480w, photo-800.jpg 800w, photo-1280.jpg 1280w"
  sizes="(max-width: 600px) 100vw, 50vw"
  width="1280"
  height="720"
  alt="A mountain beside a lake">
<!-- Browser result: the browser chooses an appropriate file for viewport size and pixel density. -->
```

`srcset` describes available files. `sizes` describes the image's expected rendered width.

## Art Direction with `picture`

```html
<picture>
  <source media="(max-width: 600px)" srcset="portrait.jpg">
  <source type="image/avif" srcset="landscape.avif">
  <img src="landscape.jpg" width="1200" height="600" alt="Team working together">
</picture>
<!-- Browser result: mobile receives a portrait crop; supported browsers may receive AVIF. -->
```

## Figure and Caption

```html
<figure>
  <img src="chart.svg" alt="Sales increase from January to March">
  <figcaption>Quarter-one sales trend.</figcaption>
</figure>
<!-- Browser result: image and visible caption are semantically grouped. -->
```

## Performance Tips

- choose AVIF/WebP when supported and retain suitable fallback
- resize images instead of sending camera-sized originals
- reserve width/height to reduce layout shift
- preload only truly critical resources
- use SVG for suitable icons/illustrations, but sanitize untrusted SVG
