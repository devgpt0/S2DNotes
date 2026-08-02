# Design a Video Streaming Web Client

> **Difficulty:** Hard  
> **Main focus:** adaptive playback, buffering, DRM, QoE

## Interview prompt

Design a browser video player for live and on-demand adaptive streaming.

## 1. Clarify the experience

**What I would say first:** The player is a feedback controller: it chooses bitrate from bandwidth, buffer, viewport, and device capability while keeping playback continuous.

### Functional requirements

- Play adaptive live and on-demand streams.
- Support seek, captions, playback speed, quality choice, and picture-in-picture.
- Recover from segment and CDN failures.
- Report quality-of-experience metrics and enforce content authorization.

### Browser and product constraints

- Browser codec, DRM, autoplay, and background policies differ.
- Network throughput changes faster than a full video download.
- Low live latency competes with a safe playback buffer.

## 2. State and API contracts

- GET /v1/videos/{id}/playback -> signed manifest, DRM config, session ID
- Manifest describes renditions and immutable media segments
- POST /v1/playback-events batches startup, rebuffer, quality, error, and watch events

## 3. Frontend architecture

```text
player UI -> playback state machine
                    |
          manifest/segment controller
             |              |
       ABR estimator     bounded buffer
             |              |
             +-> CDN segment fetch -> Media Source buffer -> video element
             |
          DRM/CDM + caption tracks
QoE batcher -> analytics endpoint
```

## 4. Critical user flow

1. Authorize playback and fetch the manifest plus device-supported rendition set.
2. Start with a conservative segment to minimize time to first frame.
3. Estimate throughput from completed segments and choose a bitrate that protects buffer health.
4. Append validated segments to the media buffer and evict old buffered ranges.
5. On error, retry another CDN or lower rendition within a strict recovery budget.

## 5. Deep dive

- ABR should consider throughput uncertainty, buffer occupancy, viewport, decode ability, and recent switches.
- Live playback tracks a target distance from the live edge and can slightly adjust playback rate.
- User-selected fixed quality overrides automation but still needs an out-of-buffer failure path.
- Captions and audio descriptions are synchronized timed tracks, not visual overlays alone.

## 6. Performance, resilience, and observability

- Limit parallel segment requests and buffered duration to control memory.
- Preload only metadata or the first segment according to user intent and data-saving policy.
- Send QoE events in batches and use beacon-style delivery at session end.
- Track time to first frame, rebuffer ratio, fatal error rate, live latency, and quality-switch instability.

## 7. Security and accessibility

- Use short-lived playback authorization, DRM where required, and strict media origins.
- Treat subtitle content and metadata as untrusted.
- Provide keyboard controls, visible focus, labeled controls, captions, transcripts, and no autoplay with sound.

## 8. Trade-offs

| Choice | Consequence |
|---|---|
| Large playback buffer | Fewer stalls but higher live latency and memory. |
| Small buffer | Low latency with greater rebuffer risk. |
| Aggressive high bitrate | Better image until throughput drops. |
| Conservative bitrate | Stable playback with lower visual quality. |

## 9. 60-second interview summary

The player is a state machine around manifest parsing, adaptive segment selection, a bounded media buffer, DRM, and timed tracks. Bitrate follows throughput and buffer health, recovery has bounded CDN/rendition fallbacks, and client QoE metrics measure real playback.

## Likely follow-up questions

- What state belongs in the URL, local UI, server cache, or durable local storage?
- What happens on a slow device with a flaky network?
- How do loading, empty, stale, partial-error, and retry states appear?
- Which Core Web Vital or product metric would reveal a bad release?

