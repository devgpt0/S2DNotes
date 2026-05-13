# Project 05: Student Marks Analyzer

## Estimated Time
3 to 5 hours

## Goal
Create a tool that stores student marks and generates analysis reports.

## Functional Requirements
- Add student with:
  - roll number
  - name
  - subject marks (dict)
- Update marks.
- Compute:
  - total
  - average
  - grade
- Class-level reports:
  - topper
  - subject-wise averages
  - pass/fail counts
- Save/load JSON.

## Non-Functional Requirements
- Marks must be 0 to 100.
- Roll number must be unique.

## Input/Output Shape
- Student dictionary:
```python
{
  "roll": 12,
  "name": "Neha",
  "marks": {"math": 88, "science": 91, "english": 79}
}
```

## Concepts Practiced
- nested dictionaries
- aggregation with loops
- list sorting

## HLD
- `main.py`: menu
- `students.py`: CRUD + calculations
- `reports.py`: class analytics
- `storage.py`: JSON persistence

## LLD
- `add_student(records, item) -> (ok, msg)`
- `update_marks(records, roll, subject, marks) -> bool`
- `student_total(item) -> int|float`
- `student_avg(item) -> float`
- `grade_from_avg(avg) -> str`
- `topper(records) -> dict|None`
- `subject_averages(records) -> dict[str, float]`
- `pass_fail_count(records, pass_mark=35) -> dict[str, int]`

## Passing Criteria
- 5+ students can be added and saved.
- Report values match manual calculations.
- Topper logic correct.

## Implementation Roadmap
1. Build data model + storage.
2. Add add/update functions.
3. Build per-student metrics.
4. Build class reports.
5. Add menu flow.

## Optional Extensions
- Rank list output.
- Subject difficulty index.
