# Project 01: To-Do CLI with Priorities

## Estimated Time
3 to 4 hours

## Goal
Build a command-line to-do manager that supports add, list, complete, delete, filter by priority, and save/load from file.

## Functional Requirements
- Add a task with:
  - title
  - priority (`high`, `medium`, `low`)
  - optional due date string
- List all tasks.
- Mark task as completed.
- Delete task by ID.
- Filter tasks by:
  - status (`pending`, `completed`)
  - priority
- Save tasks to JSON file.
- Load tasks at startup.

## Non-Functional Requirements
- Use only Python basics + collections.
- Handle bad user input without crashing.
- IDs must remain unique.

## Input/Output Shape
- Task dictionary:
```python
{
  "id": 1,
  "title": "Finish notes",
  "priority": "high",
  "status": "pending",
  "due_date": "2026-05-20"
}
```

## Concepts Practiced
- `list` of task dictionaries
- `dict` for each task record
- file handling (`json`)
- search/filter loops

## HLD
- `main.py`: menu loop
- `task_ops.py`: task CRUD operations
- `storage.py`: load/save tasks
- `utils.py`: input validation

## LLD (Function-Level Design)
- `load_tasks(path) -> list[dict]`
- `save_tasks(path, tasks) -> None`
- `create_task(next_id, title, priority, due_date) -> dict`
- `add_task(tasks, task) -> None`
- `list_tasks(tasks, status=None, priority=None) -> list[dict]`
- `mark_completed(tasks, task_id) -> bool`
- `delete_task(tasks, task_id) -> bool`
- `get_next_id(tasks) -> int`

## Passing Criteria
- Add 5 tasks and list shows all.
- Complete one task and status updates.
- Filtering by `high` returns correct tasks.
- Delete removes only target task.
- Restart app and data persists via JSON.

## Implementation Roadmap
1. Build JSON load/save functions.
2. Build add/list functions.
3. Build complete/delete functions.
4. Add filters.
5. Build menu loop.
6. Add invalid-input handling.

## Optional Extensions
- Sort by due date.
- Export pending tasks to text report.
