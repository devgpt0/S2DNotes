# 05 - Tables, Media, Metadata, and SEO

## Data Tables

Use tables for relationships between rows and columns, not page layout.

```html
<table>
  <caption>Course completion</caption>
  <thead><tr><th scope="col">Student</th><th scope="col">Progress</th></tr></thead>
  <tbody><tr><th scope="row">Asha</th><td>80%</td></tr></tbody>
</table>
<!-- Browser result: an accessible two-column data table with caption and headers. -->
```

Complex tables may need header IDs and `headers` relationships. On small screens, prefer horizontal overflow or a redesigned summary rather than shrinking text until unreadable.

## Audio and Video

```html
<video controls width="640" poster="poster.jpg">
  <source src="lesson.webm" type="video/webm">
  <source src="lesson.mp4" type="video/mp4">
  <track kind="captions" src="captions-en.vtt" srclang="en" label="English" default>
  Your browser cannot play this video.
</video>
<!-- Browser result: controlled video with fallback source and English captions. -->
```

Provide captions for spoken content and transcripts when appropriate. Avoid autoplay with sound.

## Essential Head Metadata

```html
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>HTML Course | Example Academy</title>
  <meta name="description" content="Learn semantic, accessible HTML from beginner to expert.">
  <link rel="canonical" href="https://example.com/courses/html">
</head>
<!-- Browser/search result: correct encoding, mobile viewport, descriptive title, summary, canonical URL. -->
```

## Social Metadata

```html
<meta property="og:title" content="HTML Course">
<meta property="og:image" content="https://example.com/html-course.jpg">
<meta name="twitter:card" content="summary_large_image">
<!-- Sharing result: supported social sites can show a rich preview. -->
```

## Structured Data

JSON-LD can describe products, articles, organizations, breadcrumbs, and other supported schema types. It must match visible page content.

```html
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"Course","name":"HTML Course"}
</script>
<!-- Search result: eligible engines may understand the page as a Course; rich display is not guaranteed. -->
```

## SEO Fundamentals

- useful unique content and clear headings
- crawlable links with meaningful text
- descriptive title and metadata
- canonical URLs and correct status codes
- mobile-friendly responsive layout
- fast Core Web Vitals
- accessible images and navigation
- sitemap/robots configuration appropriate to the site

SEO is not keyword repetition or hiding text.
