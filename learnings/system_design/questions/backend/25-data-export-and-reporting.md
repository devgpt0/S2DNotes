# Design a Large Data Export and Reporting System

> **Difficulty:** Medium  
> **Main focus:** snapshot consistency, asynchronous jobs, secure download

## Interview prompt

Design user-requested CSV/Parquet reports that may contain billions of rows.

## 1. Clarify the scope

**What I would say first:** Large exports are asynchronous snapshot jobs. The API returns a job ID, not a long-held HTTP response.

### Functional requirements

- Create filtered reports and track progress.
- Read a consistent snapshot without harming production traffic.
- Write partitioned output, combine manifests, and provide secure download.
- Cancel, expire, retry, and audit exports.

### Out of scope for the first version

- Interactive dashboard queries use a separate low-latency path.

## 2. Estimate the scale

These are interview assumptions, not claims about a specific company:

- Export size ranges from kilobytes to terabytes.
- Concurrent scans can overwhelm transactional databases.
- Output storage and egress are dominant costs.

## 3. API and data model

### Main contracts

- POST /v1/exports {dataset, filters, format, columns} -> 202 jobId
- GET /v1/exports/{jobId}
- POST /v1/exports/{jobId}/cancel
- GET /v1/exports/{jobId}/download -> short-lived signed URL

### Important data

- ExportJob(job_id, tenant_id, query_spec, snapshot_id, state, progress, expires_at)
- ExportPart(job_id, part_number, object_ref, row_count, checksum, state)
- ExportManifest(job_id, schema_version, parts, total_rows, checksum)

## 4. High-level design

```text
client -> export API -> job database -> durable workflow
                                          |
                                  snapshot/query planner
                                          |
                              partition workers -> object storage
                                          |
                                  manifest/finalizer
                                          |
client <- status/notification <- signed download
```

## 5. Critical request flow

1. Validate fields, authorization, estimated size, and tenant quota.
2. Pin a warehouse snapshot or read replica checkpoint.
3. Split the query into deterministic non-overlapping partitions.
4. Workers stream rows directly to compressed object parts and record checksums.
5. Finalizer verifies every part, writes a manifest, and notifies the user.

## 6. Deep dive

- Use key-range partitions rather than offset pagination, which becomes slow and inconsistent.
- Keep snapshot identity and schema version with the job for reproducibility.
- Retry one deterministic part without duplicating rows.
- Very large exports should remain multipart rather than concatenating into one giant file.

## 7. Scaling, failures, and observability

- Lease parts to workers and retry expired leases idempotently.
- Cancellation stops new work and garbage-collects partial objects after a safety window.
- Admission control limits concurrent scans by tenant and data source.
- Monitor queue age, scan bytes, rows per second, retry rate, storage, and download egress.

## 8. Security and privacy

- Authorize requested columns and rows, apply masking, and audit every export.
- Use encrypted temporary storage and short-lived single-purpose download links.
- Expire exports and delete all parts according to retention policy.

## 9. Trade-offs

| Choice | Consequence |
|---|---|
| Read production primary | Fresh but risks customer traffic. |
| Warehouse/read replica | Safer with some freshness delay. |
| One output file | Convenient but expensive to assemble. |
| Manifest plus parts | Scalable and parallel with more client handling. |

## 10. 60-second interview summary

An export request becomes a quota-controlled durable workflow pinned to a reproducible snapshot. Deterministic partition workers stream encrypted parts to object storage, a manifest verifies completion, and short-lived downloads plus retention protect the data.

## Likely follow-up questions

- What breaks first at ten times the assumed traffic?
- Which operation needs strong consistency, and why?
- How would you recover and prove no work was lost?
- Which metric best reflects the user's experience?

