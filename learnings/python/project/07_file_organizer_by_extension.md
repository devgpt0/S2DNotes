# Project 07: File Organizer by Extension

## Estimated Time
4 to 6 hours

## Goal
Build a script that organizes files from one folder into extension-based folders.

## Functional Requirements
- Scan input directory.
- Group files by extension:
  - `.txt`, `.csv`, `.jpg`, no-extension, etc.
- Move files to target folders:
  - `txt/`, `csv/`, `jpg/`, `no_ext/`
- Create operation summary:
  - moved count by extension
  - skipped files

## Non-Functional Requirements
- Do not process subfolders unless enabled.
- Handle name collision (`file.txt` already exists) safely.

## Concepts Practiced
- `dict` grouping and counting
- `list` of file paths
- `set` for processed files
- `os` / `pathlib` operations

## HLD
- `scanner.py`: collect files
- `organizer.py`: move logic
- `report.py`: summary output
- `main.py`: CLI input and run flow

## LLD
- `scan_files(folder) -> list[str]`
- `get_extension(filename) -> str`
- `target_folder_for_ext(ext) -> str`
- `safe_target_path(dst_dir, filename) -> str`
- `move_file(src, dst) -> bool`
- `organize(folder) -> dict`

## Passing Criteria
- Files moved into correct extension folders.
- No data loss on same-name collision.
- Summary report accurate.

## Implementation Roadmap
1. Build scanner and extension extractor.
2. Build folder creation and move logic.
3. Add safe rename on conflicts.
4. Build summary report.
5. Test on sample folder.

## Optional Extensions
- Dry-run mode (show planned actions only).
- Undo log file.
