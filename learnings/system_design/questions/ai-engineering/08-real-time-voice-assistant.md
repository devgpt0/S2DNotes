# Design a Real-Time Voice Assistant

> **Difficulty:** Hard  
> **Main focus:** streaming audio, interruption, latency

## Interview prompt

Design a conversational voice assistant that listens, reasons, uses tools, and speaks in real time.

## 1. Clarify the product and success criteria

**What I would say first:** The end-to-end latency budget matters more than one model's speed. The system must support partial results, turn detection, cancellation, and user interruption.

### Functional requirements

- Stream microphone audio and partial transcripts.
- Detect turns, generate a response, and stream speech.
- Support barge-in, cancellation, tools, and reconnect.
- Handle consent, retention, and unsafe actions.

### AI and product constraints

- Capture, network, ASR, reasoning, and TTS each consume latency.
- Partial transcripts can change and must not trigger irreversible actions.
- Background noise and overlapping speakers reduce confidence.

## 2. Contracts and data

- WebRTC or low-latency stream carries ordered audio frames and control events
- Events: speech_started, transcript_partial, transcript_final, response_delta, audio_chunk, interrupted
- Tool proposal uses a typed schema and explicit approval policy

## 3. High-level design

```text
microphone -> echo cancel/VAD -> realtime transport -> ASR stream
       ^                                              |
       |                                              v
speaker <- jitter buffer <- TTS stream <- response orchestrator <- model/tools
   |                               ^             |
   +----------- barge-in ----------+------ cancel tokens/work

session state -> transcript/checkpoints -> observability
```

## 4. Critical request flow

1. Capture small timestamped frames and run local or server voice activity detection.
2. ASR emits partial text for display, then a final committed turn.
3. Orchestrator builds context and starts model output; safe tool calls pass policy.
4. TTS begins from stable text chunks and sends interruptible audio.
5. New user speech cancels generation, tools where safe, buffered audio, and playback.

## 5. Quality and evaluation

- Evaluate word error rate by environment plus task completion and user correction rate.
- Measure semantic latency: user stops speaking to first meaningful audio.
- Test interruption, accents, noise, code switching, silence, and ambiguous commands.
- Evaluate voice naturalness without allowing style to hide wrong content.

## 6. Reliability, scale, observability, and cost

- Use bounded jitter and audio buffers; drop or degrade optional features under overload.
- Reconnect resumes session state but not stale audio playback.
- Fallback to text or a smaller model when latency budgets are exceeded.
- Track end-of-turn delay, ASR finalization, first audio, interruption latency, tool errors, packet loss, and cost/minute.

## 7. Safety, security, and privacy

- Show recording state and obtain required consent; retain raw audio only when justified.
- Voice identity is not authorization by default.
- High-impact tools require deterministic authorization and often explicit confirmation.

## 8. Trade-offs

| Choice | Consequence |
|---|---|
| Long audio chunks | Efficient recognition but slower response. |
| Short chunks | Low latency with more overhead. |
| Aggressive turn detection | Fast but interrupts thoughtful pauses. |
| Conservative detection | Fewer false turns with sluggish conversation. |

## 9. 60-second interview summary

A realtime transport streams timestamped audio through VAD and ASR into an interruptible model/tool/TTS pipeline. Partial text is never treated as committed intent, barge-in cancels every downstream stage, and user-perceived latency, consent, and safe authorization drive the design.

## Likely follow-up questions

- What is the offline evaluation set, and how can it leak or become stale?
- What is the safe fallback when a model or dependency fails?
- How are model, prompt, data, policy, and tool versions traced?
- What metric captures quality per unit cost?

