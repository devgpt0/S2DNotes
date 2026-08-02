# Design an AI Assistant Frontend

> **Difficulty:** Hard  
> **Main focus:** streaming output, tool states, trust

## Interview prompt

Design the frontend for an AI assistant that streams responses, cites sources, and invokes tools.

## 1. Clarify the experience

**What I would say first:** An AI response is a state machine, not one string. I will model user input, assistant stream, citations, tool proposals, approvals, errors, and cancellation explicitly.

### Functional requirements

- Send messages and stream partial assistant output.
- Render citations, structured artifacts, and tool progress.
- Require confirmation for high-impact actions.
- Retry or branch conversations without corrupting history.

### Browser and product constraints

- Streams can disconnect after partial output.
- Model text and tool results are untrusted content.
- Long conversations cannot remain fully mounted or always sent.

## 2. State and API contracts

- POST /v1/conversations/{id}/turns {clientTurnId, content, attachments}
- SSE/WebSocket events: turn.started, text.delta, citation, tool.proposed, tool.result, turn.completed, error
- POST /v1/tool-calls/{id}/approve {approvalToken}

## 3. Frontend architecture

```text
composer -> conversation controller -> turn state machine
                         |                 |
                         |                 +-> normalized message/artifact store
                         |
stream client <- event protocol <- AI gateway
     |
     +-> renderer registry: text / citation / code / artifact / tool
     +-> approval boundary -> explicit user action
```

## 4. Critical user flow

1. Persist the user's clientTurnId and create a pending assistant turn.
2. Apply sequenced stream events to typed turn state.
3. Batch text deltas for rendering while preserving the exact received content.
4. Render tool proposals separately and collect explicit confirmation when policy requires it.
5. On disconnect, resume from event cursor or fetch canonical completed turn state.

## 5. Deep dive

- Never parse security decisions from prose; tool events have validated structured schemas.
- Citations link claims to source metadata and show unavailable-source states honestly.
- Branching creates a new conversation path instead of mutating shared earlier history.
- Virtualize long histories and summarize for model context independently from what the user can inspect.

## 6. Performance, resilience, and observability

- Throttle Markdown parsing and syntax highlighting during token streaming.
- Cancel generation and network work immediately when the user stops a turn.
- Lazy-load heavy artifact renderers in sandboxed boundaries.
- Track time to first token, stream stalls, cancellation latency, render long tasks, and approval completion.

## 7. Security and accessibility

- Escape model output, sanitize Markdown, isolate generated HTML, and block unsafe URLs.
- Show tool scope, target, and consequence before approval; prevent double submission.
- Support screen-reader live regions with batched announcements, keyboard controls, and a reduced-motion mode.

## 8. Trade-offs

| Choice | Consequence |
|---|---|
| Render every token | Feels live but causes excessive parsing and announcements. |
| Batch deltas | Smooth and efficient with tiny display delay. |
| Prose-encoded tools | Easy demo but unsafe and brittle. |
| Typed tool events | Reliable boundaries with protocol design cost. |

## 9. 60-second interview summary

The UI models each turn as typed sequenced events, batches streaming text, renders citations and artifacts through isolated components, and treats tools as structured proposals with explicit approval. Resume cursors, cancellation, virtualization, and output sanitization make it production-ready.

## Likely follow-up questions

- What state belongs in the URL, local UI, server cache, or durable local storage?
- What happens on a slow device with a flaky network?
- How do loading, empty, stale, partial-error, and retry states appear?
- Which Core Web Vital or product metric would reveal a bad release?

