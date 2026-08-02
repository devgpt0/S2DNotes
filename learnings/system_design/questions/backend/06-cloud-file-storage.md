# Design Cloud File Storage and Sync

> **Difficulty:** Hard  
> **Main focus:** metadata, chunk upload, sync conflicts

## Interview prompt

Design a Dropbox- or Drive-like service for upload, download, folders, sharing, and device sync.

## 1. Clarify the scope

**What I would say first:** File bytes belong in object storage; transactional metadata and versions belong in a database. Sync uses an ordered change log.

### Functional requirements

- Upload, download, rename, move, delete, and restore files.
- Support folders, sharing permissions, versions, and multiple devices.
- Resume large uploads and deduplicate chunks where safe.
- Notify clients of changes and resolve offline conflicts.

### Out of scope for the first version

- Document co-editing is a separate collaboration design.

## 2. Estimate the scale

These are interview assumptions, not claims about a specific company:

- Assume 100 million users and petabytes of immutable file chunks.
- Large uploads must bypass application servers.
- Metadata operations are much smaller but require stronger consistency.

## 3. API and data model

### Main contracts

- POST /v1/uploads {path, size, checksum} -> upload session and signed chunk URLs
- POST /v1/uploads/{id}/complete {parts, checksum}
- GET /v1/changes?cursor=...
- POST /v1/items/{id}/share {principalId, role}

### Important data

- Item(item_id, parent_id, owner_id, name, type, current_version, status)
- FileVersion(item_id, version, manifest_id, checksum, size, created_at)
- Change(owner_or_space_id, sequence, item_id, operation, version)

## 4. High-level design

```text
client -> metadata API -> metadata database -> ordered change log
   |
   +-> signed multipart upload -> object storage -> scan/checksum workers
   |
   +<- CDN/signed download URL

sync client <- push hint / polling <- change service <- change log
```

## 5. Critical request flow

1. Create an upload session after quota and path authorization checks.
2. Client uploads chunks directly to object storage and can resume missing parts.
3. Complete verifies checksums, scans content, and atomically publishes a new file version.
4. Metadata transaction appends a sequence-numbered change.
5. Other devices fetch changes after their cursor and download only required chunks.

## 6. Deep dive

- Use immutable content-addressed chunks and version manifests; reference counting controls deletion.
- A uniqueness rule on parent ID plus normalized name prevents duplicate paths.
- Offline simultaneous edits create conflict copies or require a product-specific merge.
- Sharing is evaluated from explicit ACLs and inherited workspace policy.

## 7. Scaling, failures, and observability

- Incomplete upload sessions expire and orphan chunks are garbage-collected after a safety delay.
- Change consumers are idempotent and clients can perform a full metadata resync if a cursor expires.
- Object-storage replication and tested restores protect file bytes; metadata needs point-in-time recovery.
- Monitor upload success, checksum failures, sync lag, conflict rate, and orphan storage.

## 8. Security and privacy

- Use short-lived signed URLs scoped to one object and operation.
- Scan uploads, encrypt per tenant where required, and never trust file extensions.
- Authorize every metadata and download operation; propagate deletion to replicas and search indexes.

## 9. Trade-offs

| Choice | Consequence |
|---|---|
| Whole-file upload | Simple but poor for resume and large edits. |
| Chunk manifests | Efficient resume and deduplication with more metadata. |
| Global deduplication | Saves space but can leak existence across tenants. |
| Tenant-scoped deduplication | Safer isolation with fewer savings. |

## 10. 60-second interview summary

I separate strongly consistent metadata from immutable object chunks. Resumable direct uploads publish a version only after verification, and a sequence-numbered change log drives device sync, conflict handling, and recovery.

## Likely follow-up questions

- What breaks first at ten times the assumed traffic?
- Which operation needs strong consistency, and why?
- What happens when the main dependency times out after completing its work?
- Which metric best reflects the user's experience?

