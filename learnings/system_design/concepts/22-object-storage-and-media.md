# Object Storage and Media Pipelines

## Idea

Large immutable blobs belong in object storage; databases hold metadata,
ownership, state, and indexes.

## Classroom board

```text
client -> request upload permission -> API
client -> signed multipart upload -> object storage
storage event -> scan/transcode workers -> variants -> CDN
```

## Design steps

1. Create an upload record and short-lived signed URL.
2. Upload directly and verify size, checksum, type, and authorization.
3. Scan/process asynchronously and publish only safe completed objects.
4. Serve immutable variants through CDN; garbage-collect abandoned uploads.

## When to use it

Use for files, images, audio, video, model artifacts, and backups.

## Trade-offs and mistakes

Direct upload removes API bandwidth but requires strict signed constraints.
Never trust filename/MIME alone, expose raw storage keys, or mark an upload
ready before verification and processing finish.
