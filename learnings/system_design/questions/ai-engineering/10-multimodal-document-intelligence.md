# Design a Multimodal Document Intelligence System

> **Difficulty:** Hard  
> **Main focus:** OCR, layout, extraction, human review

## Interview prompt

Design a system that extracts structured information from scanned PDFs, forms, invoices, and images.

## 1. Clarify the product and success criteria

**What I would say first:** The output must preserve provenance from each field back to page coordinates and model version. Low-confidence important fields require human review.

### Functional requirements

- Upload documents and classify document type.
- Extract text, tables, key-value fields, signatures, and page structure.
- Return confidence and visual evidence for every field.
- Support review, correction, reprocessing, and schema versions.

### AI and product constraints

- Documents contain scans, handwriting, rotations, tables, and mixed languages.
- A plausible wrong amount can be more harmful than a missing value.
- Documents may contain malicious files and sensitive personal data.

## 2. Contracts and data

- POST /v1/document-jobs {objectRef, schemaVersion, localeHints}
- Extraction {field, typedValue, confidence, page, polygon, sourceText, modelVersions}
- POST /v1/reviews/{id}/decisions {field, correctedValue, evidence}

## 3. High-level design

```text
upload -> file validation/sandbox -> page renderer
                                   |
                    orientation/OCR/layout models
                                   |
                       document classifier
                                   |
               schema-guided extraction + table parser
                                   |
                 validation/business-rule checks
                     | high confidence | uncertain
                     v                 v
                  result          review queue/UI
                                      |
                              curated feedback dataset
```

## 4. Critical request flow

1. Validate and render the file in an isolated service; never trust embedded scripts.
2. Detect orientation, page layout, OCR text, and coordinate mapping.
3. Classify the document and select a versioned extraction schema.
4. Extract typed fields, validate totals/dates/identifiers, and attach provenance.
5. Route important low-confidence or rule-breaking fields to a reviewer before completion.

## 5. Quality and evaluation

- Measure exact and normalized field accuracy, table structure, missing-field recall, and review rate.
- Weight fields by business harm; invoice total and decorative text are not equal.
- Evaluate across scanner quality, language, vendor, handwriting, and time.
- Track reviewer agreement and use corrections only after quality validation.

## 6. Reliability, scale, observability, and cost

- Use a durable per-page workflow so failed pages can retry independently.
- Cache deterministic renders and OCR by content hash and model version.
- Keep original, render, extraction, and review lineage for reproducibility and deletion.
- Track queue age, page latency, extraction confidence, validation failures, review SLA, and cost/page.

## 7. Safety, security, and privacy

- Encrypt documents, use least-privilege review access, and apply strict retention.
- Sandbox parsers, block active content, and scan uploads.
- Do not expose one tenant's examples in prompts or shared caches.

## 8. Trade-offs

| Choice | Consequence |
|---|---|
| End-to-end model only | Simple output but weak provenance and debugging. |
| Staged OCR/layout/extraction | Observable and replaceable with more components. |
| Always human review | High assurance but slow and costly. |
| Confidence/risk routing | Efficient with calibration and monitoring needs. |

## 9. 60-second interview summary

A sandboxed page pipeline produces OCR and layout, then schema-guided extraction returns typed fields with page polygons and lineage. Business validation plus calibrated risk routes uncertain high-impact fields to human review, and every stage is independently retryable.

## Likely follow-up questions

- What is the offline evaluation set, and how can it leak or become stale?
- What is the safe fallback when a model or dependency fails?
- How are model, prompt, data, policy, and tool versions traced?
- What metric captures quality per unit cost?

