# Project 03: Expense Tracker with Monthly Summary

## Estimated Time
4 to 6 hours

## Goal
Build a tracker to record expenses and produce monthly/category summaries.

## Functional Requirements
- Add expense entry:
  - date (`YYYY-MM-DD`)
  - amount
  - category
  - note
- List all expenses.
- Filter by month (`YYYY-MM`) and category.
- Show summary:
  - total spent in month
  - category-wise totals
  - highest single expense
- Save/load JSON.

## Non-Functional Requirements
- Amount must be positive number.
- Date format basic validation.

## Input/Output Shape
- Expense dictionary:
```python
{
  "id": 7,
  "date": "2026-05-13",
  "amount": 450.0,
  "category": "food",
  "note": "Dinner"
}
```

## Concepts Practiced
- `list` for expenses
- `dict` for grouped totals
- aggregation loops
- numeric operations

## HLD
- `main.py`: menu and command flow
- `expense_ops.py`: add/list/filter
- `reports.py`: summary calculations
- `storage.py`: JSON I/O

## LLD
- `add_expense(expenses, item) -> None`
- `filter_by_month(expenses, month) -> list[dict]`
- `filter_by_category(expenses, category) -> list[dict]`
- `category_totals(expenses) -> dict[str, float]`
- `monthly_total(expenses, month) -> float`
- `highest_expense(expenses, month=None) -> dict|None`
- `load_data(path) -> list[dict]`
- `save_data(path, expenses) -> None`

## Passing Criteria
- Adding 10 entries works.
- Monthly summary matches manual math.
- Category totals correct.
- Data survives restart.

## Implementation Roadmap
1. Build storage + add/list.
2. Add month/category filters.
3. Add summary functions.
4. Add validation.
5. Add sample dataset and test manually.

## Optional Extensions
- Budget limit warnings.
- CSV export.
