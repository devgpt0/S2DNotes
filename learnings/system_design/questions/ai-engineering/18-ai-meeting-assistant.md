# Design an AI Meeting Assistant

> **Difficulty:** Hard  
> **Main focus:** realtime transcription, diarization, summaries

## Interview prompt

Design an assistant that joins meetings, transcribes speakers, summarizes discussion, and extracts action items.

## 1. Clarify the product and success criteria

**What I would say first:** Consent and participant visibility come first. Realtime captions, final transcript, and generated summary have different latency and correctness requirements.

### Functional requirements

- Capture authorized meeting audio and stream captions.
- Identify speakers where permitted and produce a corrected final transcript.
- Generate summaries, decisions, and action items with citations to timestamps.
- Support editing, sharing permissions, retention, and deletion.

### AI and product constraints

- Audio may have overlap, noise, accents, and participant name ambiguity.
- Partial captions change; summaries must use committed transcript.
- Meetings often contain highly sensitive information.

## 2. Contracts and data

- MeetingSession {meetingId, tenant, consentState, participants, policy, retention}
- TranscriptSegment {segmentId, start, end, speakerId?, text, confidence, revision}
- ActionItem {text, owner?, dueDate?, supportingSegmentIds, confidence}

## 3. High-level design

```text
meeting platform/audio -> consent gate -> realtime audio pipeline
                                      |
                          VAD/ASR -> partial captions
                                      |
                           diarization/alignment
                                      |
                      committed transcript store
                         |                 |
                  summary/action model   search/index
                         |
                 grounded artifacts -> editor/share controls
```

## 4. Critical request flow

1. Verify tenant policy and visible participant consent before capture.
2. Stream timestamped audio through VAD and ASR; display revisable partial captions.
3. Finalize segments, align speakers, and permit participant corrections.
4. Generate summary, decisions, and action items only from committed segments.
5. Attach every generated item to supporting timestamps and apply meeting permissions.

## 5. Quality and evaluation

- Measure word error rate, speaker attribution, caption latency, summary factuality, and action-item precision/recall.
- Evaluate noise, overlap, accents, domain terms, long meetings, and code switching.
- Require citation support for decisions and owner assignments.
- Track user edits as signals but validate them before training.

## 6. Reliability, scale, observability, and cost

- Bound audio buffers and checkpoint transcript so a worker failure loses little work.
- Use custom vocabulary scoped to tenant or meeting without leaking it to others.
- Retry offline finalization independently from live captions.
- Track caption delay, finalization lag, diarization uncertainty, summary edits, storage, and cost/hour.

## 7. Safety, security, and privacy

- Show an unmistakable recording indicator and support participant removal requests.
- Encrypt audio/transcripts, minimize raw-audio retention, and enforce meeting ACLs everywhere.
- Do not infer sensitive participant traits or assign actions without evidence.

## 8. Trade-offs

| Choice | Consequence |
|---|---|
| Keep raw audio | Enables reprocessing but increases privacy and storage risk. |
| Delete after transcript | Safer with less future correction ability. |
| Realtime summary | Immediate but based on unstable context. |
| Post-meeting grounded summary | More accurate with delayed availability. |

## 9. 60-second interview summary

After an explicit consent gate, timestamped audio produces revisable live captions and a corrected committed transcript. Summaries and action items cite supporting segments, inherit meeting permissions, and run independently from the realtime path, with strict retention and deletion.

## Likely follow-up questions

- What is the offline evaluation set, and how can it leak or become stale?
- What is the safe fallback when a model or dependency fails?
- How are model, prompt, data, policy, and tool versions traced?
- What metric captures quality per unit cost?

