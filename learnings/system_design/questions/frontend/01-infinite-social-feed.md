# Design an Infinite Social Feed Frontend

> **Difficulty:** Easy  
> **Main focus:** cursor pagination, virtualization, resilient state

## Interview prompt

Design the web frontend for a ranked infinite feed with posts, media, reactions, and refresh.

## 1. Clarify the experience

**What I would say first:** I will separate server state from temporary UI state, use cursor pagination, virtualize the list, and preserve scroll position across navigation.

### Functional requirements

- Load an initial feed and append pages near the viewport end.
- Render text, images, video previews, reactions, and deleted items.
- Support refresh, retry, navigation back, and accessible keyboard use.
- Avoid duplicate posts and excessive memory on long sessions.

### Browser and product constraints

- Assume mid-range mobile devices and unreliable networks.
- The first useful post should render quickly; media loads progressively.
- Feed order may change while the user is reading.

## 2. State and API contracts

- GET /v1/feed?cursor=opaque&limit=20 -> items, nextCursor, snapshotId
- PUT /v1/posts/{id}/reaction {type, clientMutationId}
- Post model includes stable id, content type, aspect ratio, author, version, and moderation state

## 3. Frontend architecture

```text
route
  |
feed controller -> query/page cache -> feed API
  |                      |
  |                      +-> normalized post entities
  |
virtualized list -> post renderer -> responsive media / lazy video
  |
scroll anchor + intersection observer + accessibility announcements
```

## 4. Critical user flow

1. Render a lightweight shell and request the first page.
2. Normalize posts by stable ID and keep page order separately.
3. Reserve media space from aspect ratio to prevent layout shift.
4. An intersection sentinel requests the next cursor once; obsolete requests are cancelled.
5. Virtualization removes far-away DOM nodes while retaining measured heights and scroll anchor.

## 5. Deep dive

- Cursor pagination is stable under insertions; offset pagination can skip or duplicate posts.
- Deduplicate by post ID when refresh and older pages overlap.
- Optimistic reactions update a local overlay and roll back only that mutation on failure.
- When navigating back, restore pages, scroll anchor ID, and within-item offset rather than raw pixels alone.

## 6. Performance, resilience, and observability

- Budget JavaScript, image bytes, and main-thread work; code-split heavy post types.
- Prefetch only the next page and media close to the viewport.
- Use skeletons with fixed dimensions, not layout-shifting spinners.
- Track LCP, INP, CLS, feed load failures, duplicate rate, and scroll restoration success.

## 7. Security and accessibility

- Sanitize rich content, isolate embeds, and enforce server authorization.
- Use semantic article/list structure, visible focus, alt text, captions, and reduced-motion support.
- Do not announce every appended item to screen readers; use a controlled status message.

## 8. Trade-offs

| Choice | Consequence |
|---|---|
| Full DOM list | Simple but memory and layout cost grow without bound. |
| Virtualized list | Scalable with measurement and accessibility complexity. |
| Optimistic reactions | Responsive but needs precise rollback. |
| Wait for server | Simpler consistency but feels slow. |

## 9. 60-second interview summary

I use a normalized cursor-paginated server-state cache, a virtualized accessible list, reserved media dimensions, cancellable prefetch, and anchor-based restoration. Optimistic actions are isolated overlays, while stale or deleted posts reconcile by version.

## Likely follow-up questions

- What state belongs in the URL, local UI, server cache, or durable local storage?
- What happens on a slow device with a flaky network?
- How do loading, empty, stale, partial-error, and retry states appear?
- Which Core Web Vital or product metric would reveal a bad release?

