# Design a Secure Self-Hosted LLM Deployment

> **Difficulty:** Hard  
> **Main focus:** model download, artifact security, GPU sizing, serving, and rollout

## Interview prompt

How would you safely download an open-weight LLM and deploy it as a reliable,
scalable production service?

## 1. Start with the real goal

The goal is not merely to copy model files onto a GPU. The goal is to create a
repeatable path from an approved model version to a measurable, reversible
production deployment.

**What I would say first:** I will separate the model supply chain from the
online serving system. Production workers never download unverified files from
the public internet.

### Functional requirements

- Select and approve a model for the product's quality, language, and safety needs.
- Download one immutable model version and preserve its tokenizer and chat template.
- Serve batch and streaming requests behind authentication and quotas.
- Scale across GPUs while keeping latency and cost within targets.
- Test, canary, observe, and roll back every model release.

### Non-functional requirements

- No unverified executable model code or mutable `latest` revision.
- No request is accepted by a worker until the model is fully loaded and warmed.
- Tenant data, adapters, prompts, and caches remain isolated.
- A failed rollout can return to the last healthy version quickly.

### Questions to ask the interviewer

- Is this a base, instruction, code, vision, or embedding model?
- What are the context length, output length, and quality targets?
- What are peak requests per second and concurrent sequences?
- What are the time-to-first-token and tokens-per-second targets?
- May data leave our network, and what retention policy applies?
- Do we need one model, many models, or tenant-specific adapters?

## 2. Classroom-board view

```text
PUBLIC / BUILD SIDE                    PRIVATE / PRODUCTION SIDE

model publisher
      |
      v
isolated download job -- verify --> approved artifact store
      |                    |              |
      |                    +-> manifest   +-> immutable model files
      |                    +-> hashes     +-> tokenizer + template
      |                    +-> license
      v
model registry: candidate -> tested -> approved
                                      |
                                      v
client -> API gateway -> admission queue -> model workers on GPUs
             |                 |                  |
          auth/quota       fair scheduling    batch + KV cache
                                                   |
client <------------ sequenced token stream <------+
```

The left side establishes **what may run**. The right side controls **how it
runs**. Keeping these paths separate prevents a public repository change from
silently changing production.

## 3. Choose the model before downloading it

Evaluate candidates against the real workload, not only public leaderboards.

| Check | Why it matters |
|---|---|
| License and acceptable-use terms | A technically good model may not permit the intended commercial use. |
| Model card and training limitations | Reveal supported languages, context limits, and known risks. |
| Task quality | Measure on the product's prompts and scoring rules. |
| Safety and privacy behavior | Test refusal, leakage, memorization, and jailbreak cases. |
| Architecture support | The serving runtime must understand the model without unsafe remote code. |
| Hardware fit | Weights, KV cache, and runtime memory must fit the available GPUs. |
| Latency and throughput | A larger model is useful only if the product can serve it. |

> [!IMPORTANT]
> Pin the exact repository commit or immutable artifact version. A model name or
> branch such as `main` is not a reproducible release.

## 4. Build a safe model-download pipeline

### Idea

Download in an isolated build environment, verify every required artifact, and
promote the verified result into a private store. Production nodes can access
that private store but do not need public internet access.

### Steps

1. Approve the publisher, model ID, license, architecture, and full revision ID.
2. Give an isolated download job a short-lived, read-only credential.
3. Download only the required files: configuration, tokenizer, chat template,
   generation configuration, and `safetensors` weight shards.
4. Reject unexpected executable files and unsafe serialized formats. Keep
   remote model code disabled unless it has been reviewed and vendored.
5. Verify publisher signatures when available and calculate a cryptographic
   hash for every file.
6. Scan the files and build image; record provenance and a software bill of materials.
7. Run a load test and a small golden-prompt test in the isolated environment.
8. Copy the verified bundle to an immutable private artifact store.
9. Register its manifest as a candidate. Promotion to production requires
   quality, safety, compatibility, and performance gates.

An example download in a controlled build job may look like this:

```bash
hf download organization/model-name \
  --revision <full-immutable-commit-id> \
  --include "*.safetensors" "*.json" "tokenizer.*" "*.jinja" \
  --local-dir ./model
```

The command is only the copy step. The revision check, file allowlist, hash
verification, scanning, testing, and private promotion make it production-safe.
Never place access tokens in the command, image, source code, or shell history.

### Model release manifest

```text
release_id: support-llm-2026-08-02-01
source_model: organization/model-name
source_revision: <full immutable commit id>
license: <approved license id>
architecture: <expected architecture>
tokenizer_hash: <sha256>
weight_hashes: [<sha256 per shard>]
chat_template_hash: <sha256>
precision: bf16
runtime_image_digest: <immutable image digest>
evaluation_report: <immutable report reference>
approval_state: candidate | approved | retired
```

The weights, tokenizer, template, runtime, and evaluation report form one
release. Changing any one of them creates a new release.

## 5. Size the deployment

### Weight memory

Start with this lower-bound estimate:

```text
weight memory ~= parameter count x bytes per parameter
```

For a 7-billion-parameter model:

```text
BF16 or FP16: 7B x 2 bytes ~= 14 GB just for weights
INT8:         7B x 1 byte  ~=  7 GB plus quantization metadata
4-bit:        7B x 0.5     ~= 3.5 GB plus quantization metadata
```

This is not the total. Also reserve memory for the KV cache, temporary
activations, communication buffers, runtime kernels, and fragmentation.

### KV-cache memory

The KV cache grows with active tokens and concurrent sequences:

```text
KV bytes ~= 2 x layers x KV heads x head dimension
           x bytes per value x cached tokens
```

The exact layout depends on the architecture and runtime. Measure it on the
chosen model. Long contexts can consume more memory than expected even when the
weights fit comfortably.

### Capacity test

Benchmark the actual distribution of prompt and output lengths. Record:

- maximum safe concurrent sequences;
- time to first token at p50 and p95;
- inter-token latency and output tokens per second;
- throughput under continuous batching;
- memory use and out-of-memory rate;
- quality loss caused by quantization.

Keep operating headroom and reject excess traffic with an explicit overload
response. An unbounded queue only converts overload into extreme latency.

## 6. Serving architecture

```text
                         CONTROL PLANE
    model registry -> deployment controller -> canary/rollback policy
           |                    |
           +---------- capacity and health ----------+

                          DATA PLANE
client -> gateway -> validator -> quota/admission -> fair scheduler
            |                                        |
       auth, limits                           compatible request queues
                                                     |
                              +----------------------+----------------+
                              |                                       |
                      GPU worker group A                      GPU worker group B
                   tokenizer + model + KV                  tokenizer + model + KV
                              |                                       |
                              +------ streamed token gateway ---------+
```

### Request contract

```http
POST /v1/generate
Authorization: Bearer <short-lived-token>
Idempotency-Key: <request-id>
Content-Type: application/json

{
  "modelRelease": "support-llm-2026-08-02-01",
  "messages": [{"role": "user", "content": "Explain this error."}],
  "maxOutputTokens": 400,
  "temperature": 0.2,
  "stream": true
}
```

Validate types and limits exactly. Reject unsupported model releases, excessive
context, invalid sampling values, and exhausted quota before work enters a GPU
queue.

### Critical request flow

1. Authenticate the caller and resolve tenant policy.
2. Validate the request, tokenize it, and calculate the total token budget.
3. Reserve quota and admit the request only if a bounded queue has capacity.
4. Route it to a worker with the exact model release.
5. Use continuous batching to add and remove sequences without waiting for the
   longest request in a fixed batch.
6. Stream numbered token events so disconnects and incomplete responses are visible.
7. On completion or cancellation, release KV-cache memory and record usage.

### Multi-GPU choices

| Method | Use it when | Cost |
|---|---|---|
| One model replica per GPU | The entire model fits on one GPU | Simple and scales throughput well |
| Tensor parallelism | One request needs weights split across GPUs | Fast interconnect and coordination are required |
| Pipeline parallelism | Model layers must be split across devices or nodes | Pipeline bubbles add latency |
| Quantization | Memory or cost prevents the original precision | Quality and kernel support must be re-evaluated |

Prefer one replica per GPU when it meets the requirement. Distributed serving
adds failure modes and should solve a measured capacity problem.

### Step-by-step deployment

1. Build a pinned serving-runtime image. Keep the large model weights in the
   private artifact store so a runtime security patch does not require copying
   them into a new image.
2. Provision compatible GPU nodes, drivers, runtime libraries, networking, and
   encrypted storage. Validate this combination in the compatibility gate.
3. Give the workload read-only access to exactly the approved release path.
4. Copy the release from the private store to a local cache and verify its
   manifest and hashes again before loading.
5. Start the worker with readiness disabled. Load the tokenizer, chat template,
   weights, and generation settings from the same release.
6. Run warm-up prompts that exercise expected context sizes and kernels.
7. Enable readiness only after load, warm-up, and a golden response check pass.
8. Let the gateway send canary traffic to the new worker group.
9. Scale replicas from queue time, active sequences, and KV-cache pressure;
   GPU utilization alone does not show whether users are waiting.

Use separate health signals:

```text
liveness:  is the worker process making progress?
readiness: can this exact model release accept a real request now?
```

A worker that is alive but still loading a model must not receive traffic.

## 7. Deploy without surprising users

### Release gates

Every candidate must pass:

1. **Artifact gate:** hashes, license, provenance, and allowed files are correct.
2. **Compatibility gate:** tokenizer, template, runtime, and hardware load correctly.
3. **Quality gate:** task, language, safety, and structured-output tests pass.
4. **Performance gate:** latency, throughput, memory, and cost meet targets.
5. **Reliability gate:** cancellation, overload, worker loss, and restart tests pass.

### Progressive rollout

```text
offline tests -> shadow traffic -> internal users -> 1% canary
              -> 10% -> 50% -> 100%
                         |
             automatic rollback on guardrail failure
```

Shadow traffic measures performance without returning the candidate output to
users. A canary exposes only a controlled population. Keep the old model warm
until the rollback window has passed.

Do not compare only global averages. Segment results by language, task, prompt
length, output length, tenant class, and safety category.

## 8. Reliability and failure handling

| Failure | Correct behavior |
|---|---|
| Hash or manifest mismatch | Stop promotion immediately; never attempt to load the release. |
| Worker cannot load model | Keep readiness false and replace the worker. |
| GPU out of memory | Fail the affected request clearly, reduce admission, and investigate sizing. |
| Queue is full | Return an explicit overload response with retry guidance. |
| Worker dies before output | Retry on a healthy worker if the request policy permits it. |
| Worker dies after streaming starts | Mark the stream incomplete; do not silently append a second generation. |
| Client disconnects | Cancel generation and free KV cache promptly. |
| New release regresses | Stop rollout and route traffic to the previous immutable release. |
| Artifact store is unavailable | Existing warm workers continue; new workers fail readiness rather than fetching elsewhere. |

## 9. Security and privacy

- Keep production workers off the public internet.
- Use short-lived workload identity and least-privilege artifact access.
- Encrypt prompts, outputs, adapters, and model artifacts in transit and at rest.
- Never share private prefix caches, KV caches, or adapters across tenants.
- Treat prompts and outputs as sensitive; store only what policy allows.
- Validate structured outputs before another system executes them.
- Rate-limit requests by tokens, not only request count.
- Red-team the model, API, and tool integrations before promotion.

## 10. Observability

Track each model release separately:

- queue time and admission rejection rate;
- time to first token and inter-token latency;
- input and output tokens per second;
- active sequences, batch size, and KV-cache utilization;
- GPU memory, utilization, temperature, OOM, and worker restart rate;
- cancellation, truncated stream, and error rate;
- quality, safety, and structured-output failure rate;
- GPU-seconds and cost per successful request.

Use request IDs and release IDs in traces. Do not place unrestricted prompt or
response text in logs.

## 11. Trade-offs

| Choice | Benefit | Cost |
|---|---|---|
| Managed model API | Fastest operation and elastic capacity | Less control and possible data/residency limits |
| Self-hosted model | Control over weights, data path, tuning, and capacity | GPU operations, security, and rollout burden |
| Full precision | Best fidelity to the original model | Highest memory and cost |
| Quantized model | Lower memory and often higher throughput | Possible quality loss and hardware-specific behavior |
| Many warm models | Low cold-start latency | Expensive idle GPU memory |
| Load on demand | Better utilization for rare models | Slow starts and more failure paths |

## 12. 60-second interview summary

I would pin an approved model revision, download it in an isolated job, allow
only safe files, verify hashes and provenance, test it, and promote the bundle
to a private immutable store. Production uses a versioned registry, bounded
admission queues, continuous batching, isolated caches, and warmed GPU workers.
Artifact, quality, safety, performance, and reliability gates lead into a
canary rollout with an immediate rollback path. This makes model deployment a
controlled software release rather than an untracked file download.

## Likely follow-up questions

- How would you choose between a smaller model and a quantized larger model?
- How does continuous batching differ from normal request batching?
- How do context length and concurrency affect KV-cache capacity?
- How would you deploy tenant-specific adapters without leaking data?
- What changes when one model cannot fit on one GPU?
- Which metrics should trigger automatic rollback?
