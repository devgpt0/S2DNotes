# Design a Video Streaming Platform

> **Difficulty:** Hard  
> **Main focus:** media processing, CDN delivery, adaptive bitrate

## Interview prompt

Design video upload, processing, playback, and global delivery.

## 1. Clarify the scope

**What I would say first:** The control plane manages metadata and jobs; the data plane moves large media directly through object storage and CDNs.

### Functional requirements

- Upload large source videos reliably.
- Transcode into multiple resolutions and package adaptive streams.
- Play globally with low startup time and buffering.
- Support metadata, captions, thumbnails, privacy, and takedown.

### Out of scope for the first version

- Recommendations and advertising auctions are separate systems.

## 2. Estimate the scale

These are interview assumptions, not claims about a specific company:

- Assume millions of uploads and billions of viewing minutes per day.
- Media bandwidth dominates cost; origin application servers must not carry playback bytes.
- Popular releases create extreme CDN hot spots.

## 3. API and data model

### Main contracts

- POST /v1/videos -> upload session
- POST /v1/videos/{id}/publish
- GET /v1/videos/{id}/playback -> manifest URL and playback token

### Important data

- Video(video_id, owner_id, title, visibility, processing_status, manifest_ref)
- Rendition(video_id, codec, resolution, bitrate, object_prefix, status)
- TranscodeJob(job_id, video_id, stage, attempt, status)

## 4. High-level design

```text
uploader -> upload service -> object storage (source)
                                  |
                                  +-> durable workflow
                                      -> transcode workers
                                      -> package segments/captions/thumbnails
                                      -> object storage (renditions)

viewer -> playback API -> signed manifest -> CDN -> segment origin
```

## 5. Critical request flow

1. Client uploads the source directly with a resumable multipart session.
2. A durable workflow probes, transcodes, packages, scans, and creates thumbnails.
3. Publish only when the minimum playable rendition is ready; add others later.
4. Playback API authorizes the viewer and returns a short-lived manifest URL.
5. Player selects segment bitrate from bandwidth and buffer health.

## 6. Deep dive

- Use short independent segments so the player can switch bitrate between segments.
- CDN cache keys must include immutable version paths but not per-user tokens when token validation can occur at the edge.
- Workflow stages are idempotent and store checkpoints because transcoding is long and expensive.
- Pre-warm or origin-shield highly anticipated content.

## 7. Scaling, failures, and observability

- Retry failed segments or renditions rather than restarting the entire video.
- If one codec fails, publish supported alternatives when product policy allows.
- Multi-CDN steering handles regional provider failures.
- Monitor time to first frame, rebuffer ratio, playback error rate, transcode queue age, and cost per minute.

## 8. Security and privacy

- Validate media structure, sandbox codecs, scan content, and protect processing workers.
- Use authorization-aware playback tokens, DRM where required, and rapid takedown propagation.
- Keep private source objects inaccessible from public CDN paths.

## 9. Trade-offs

| Choice | Consequence |
|---|---|
| More renditions | Better adaptation but higher compute and storage cost. |
| Shorter segments | Faster adaptation with more request overhead. |
| Single CDN | Simpler and cheaper until availability or regional performance requires more. |
| Multi-CDN | Higher resilience with routing and contract complexity. |

## 10. 60-second interview summary

Uploads go directly to object storage, a durable idempotent workflow creates adaptive renditions, and immutable segments are served through CDN and origin shield. Playback quality is measured at the client, while authorization and takedown remain in the control plane.

## Likely follow-up questions

- What breaks first at ten times the assumed traffic?
- Which operation needs strong consistency, and why?
- What happens when the main dependency times out after completing its work?
- Which metric best reflects the user's experience?

