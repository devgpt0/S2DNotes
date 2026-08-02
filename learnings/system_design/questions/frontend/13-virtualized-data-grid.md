# Design a Virtualized Enterprise Data Grid

> **Difficulty:** Hard  
> **Main focus:** large data, editing, accessibility

## Interview prompt

Design a spreadsheet-like grid for millions of server rows with sorting, filters, resizing, selection, and editing.

## 1. Clarify the experience

**What I would say first:** The grid cannot load or render all rows. I will use server-side query state, two-dimensional virtualization, stable row IDs, and an explicit edit state machine.

### Functional requirements

- Sort, filter, paginate, resize, pin, and reorder columns.
- Select ranges, copy/paste, edit cells, and show validation.
- Support millions of rows and hundreds of columns.
- Remain keyboard and screen-reader usable.

### Browser and product constraints

- Variable row heights and pinned regions complicate virtualization.
- Server data may change between pages.
- High-frequency cell rendering can block the main thread.

## 2. State and API contracts

- GET /v1/rows?cursor=...&sort=...&filter=...&columns=...
- PATCH /v1/rows/{id} {changes, expectedVersion, mutationId}
- Grid query key includes dataset, sort, filter, selected columns, and snapshot

## 3. Frontend architecture

```text
grid controller
  |---------- query state/URL ---------- server page cache
  |---------- selection/edit state ----- mutation queue
  |
row virtualizer + column virtualizer
  |
pinned panes / scroll pane -> cell renderer registry
  |
keyboard navigation + accessibility mirror
```

## 4. Critical user flow

1. Query server pages using stable sort plus row-ID tie-breaker.
2. Virtualizers calculate visible row and column windows with overscan.
3. Cell renderers receive pure typed values and do not fetch independently.
4. Editing creates a local draft; commit validates then sends an optimistic versioned mutation.
5. Conflict response keeps the draft and offers refresh or explicit overwrite when permitted.

## 5. Deep dive

- Selection uses logical row IDs and column IDs, not DOM coordinates.
- Separate pinned and scrolling panes must share measurements and vertical scroll.
- Cursor pagination and a query snapshot prevent changing data from shuffling pages unpredictably.
- Copy/paste validates a rectangular operation before applying batched mutations.

## 6. Performance, resilience, and observability

- Memoize column definitions and avoid creating new callbacks for every cell.
- Use fixed row height when product permits; otherwise cache measurements and anchor scroll.
- Fetch only displayed columns and prefetch the next bounded page.
- Track long tasks, scroll frame rate, cell render count, page latency, edit conflicts, and memory.

## 7. Security and accessibility

- Escape cell text and defend CSV export against formula injection.
- Authorize columns and row filters server-side.
- Implement grid keyboard semantics, focus restoration for recycled cells, announced sort state, and a usable non-virtualized accessibility window.

## 8. Trade-offs

| Choice | Consequence |
|---|---|
| Client-side all rows | Rich instant operations but limited dataset size. |
| Server-side query | Scales with network and state complexity. |
| Variable heights | Flexible content with expensive measurement. |
| Fixed heights | Fast predictable virtualization with layout limits. |

## 9. 60-second interview summary

The grid stores server query state separately from local selection and drafts, fetches cursor pages with stable ordering, and virtualizes rows and columns by logical IDs. Versioned edits, pure cell renderers, pinned-pane coordination, and explicit accessibility semantics handle enterprise scale.

## Likely follow-up questions

- What state belongs in the URL, local UI, server cache, or durable local storage?
- What happens on a slow device with a flaky network?
- How do loading, empty, stale, partial-error, and retry states appear?
- Which Core Web Vital or product metric would reveal a bad release?

