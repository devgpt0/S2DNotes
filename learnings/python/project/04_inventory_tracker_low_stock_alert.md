# Project 04: Inventory Tracker with Low-Stock Alerts

## Estimated Time
4 to 6 hours

## Goal
Build a stock tracking CLI for small shop inventory.

## Functional Requirements
- Add product:
  - SKU
  - name
  - quantity
  - reorder threshold
- Increase/decrease stock.
- View all products.
- Show low-stock products.
- Save/load inventory JSON.

## Non-Functional Requirements
- SKU must be unique.
- Quantity cannot go below zero.

## Input/Output Shape
- Product dictionary:
```python
{
  "sku": "P1001",
  "name": "Notebook",
  "qty": 14,
  "threshold": 10
}
```

## Concepts Practiced
- `dict` keyed by SKU for O(1) access
- `list` for reporting output
- validation and state updates

## HLD
- `main.py`: menu
- `inventory.py`: add/update/report functions
- `storage.py`: JSON read/write
- `validators.py`: input checks

## LLD
- `add_product(inv, product) -> (ok, msg)`
- `increase_stock(inv, sku, amount) -> bool`
- `decrease_stock(inv, sku, amount) -> bool`
- `list_products(inv) -> list[dict]`
- `low_stock_products(inv) -> list[dict]`
- `load_inventory(path) -> dict[str, dict]`
- `save_inventory(path, inv) -> None`

## Passing Criteria
- Duplicate SKU blocked.
- Decrease below zero blocked.
- Low-stock list returns correct SKUs.
- Inventory persists across runs.

## Implementation Roadmap
1. Build inventory dict and storage.
2. Add add/increase/decrease functions.
3. Add low-stock report.
4. Add menu and error handling.

## Optional Extensions
- Value by product (`qty * unit_price`).
- Search by name.
