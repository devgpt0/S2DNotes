# Design a Large Media Gallery Frontend

> **Difficulty:** Easy  
> **Main focus:** responsive media, virtualization, uploads

## Interview prompt

Design a gallery that browses millions of images and videos and supports large uploads.

## 1. Clarify the experience

**What I would say first:** The client never loads original media for thumbnails. I will use cursor pages, responsive derivatives, layout reservation, virtualization, and direct resumable uploads.

### Functional requirements

- Browse, filter, select, preview, and download media.
- Support responsive thumbnails and full-screen viewing.
- Upload large files with progress, resume, cancellation, and processing states.
- Remain fast for long sessions and accessible to keyboard users.

### Browser and product constraints

- Media bytes dominate network and memory.
- Image dimensions are needed before download to prevent layout shift.
- Uploads and server processing can take minutes.

## 2. State and API contracts

- GET /v1/media?cursor=...&filter=... -> id, aspectRatio, thumbnailSrcSet, status
- POST /v1/uploads -> multipart session and signed URLs
- POST /v1/uploads/{id}/complete
- GET /v1/media/{id}/processing

## 3. Frontend architecture

```text
gallery route -> query cache -> media metadata API
      |
virtualized grid -> responsive image component -> CDN derivatives
      |
selection/lightbox state

upload manager -> IndexedDB session -> signed multipart upload -> object storage
                                              |
                                      processing status stream
```

## 4. Critical user flow

1. Load metadata first and reserve each tile's aspect-ratio box.
2. Virtualize rows and lazy-load the closest responsive thumbnail size.
3. Prefetch adjacent full-screen items only after the selected image.
4. Upload chunks directly with bounded concurrency and persist session progress.
5. After completion, show processing state until safe derivatives are ready.

## 5. Deep dive

- A justified grid needs row measurement; a fixed grid is simpler and faster when acceptable.
- Use object URLs for local previews and revoke them after use.
- Decode large images off the critical path and cap simultaneous decodes.
- Selection state stores IDs independently from mounted tile components.

## 6. Performance, resilience, and observability

- Set budgets for decoded pixels, in-flight requests, DOM tiles, and prefetch distance.
- Cancel requests for media far from the viewport.
- Do not store full binary files in application state.
- Track LCP, layout shift, decode failures, memory, upload retry rate, and time to first preview.

## 7. Security and accessibility

- Treat metadata and filenames as untrusted text; isolate unsafe previews.
- Use short-lived upload/download URLs and server-side content validation.
- Provide alt text, grid keyboard navigation, visible focus, captions, and reduced-motion transitions.

## 8. Trade-offs

| Choice | Consequence |
|---|---|
| Original media thumbnails | Simple but wastes bandwidth and memory. |
| Generated derivatives | Efficient delivery with processing/storage cost. |
| Aggressive prefetch | Fast navigation but expensive data use. |
| Viewport-near prefetch | Balanced performance and cost. |

## 9. 60-second interview summary

A cursor-paginated virtual grid renders CDN derivatives in reserved aspect-ratio boxes. Full media and uploads stay outside app state; a resumable direct-upload manager persists sessions, while accessibility and strict byte/decode budgets protect long browsing sessions.

## Likely follow-up questions

- What state belongs in the URL, local UI, server cache, or durable local storage?
- What happens on a slow device with a flaky network?
- How do loading, empty, stale, partial-error, and retry states appear?
- Which Core Web Vital or product metric would reveal a bad release?

