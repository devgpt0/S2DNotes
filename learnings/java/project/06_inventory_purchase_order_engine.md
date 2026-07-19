# Project 06: Inventory + Purchase Order Engine

## Estimated Time
5 to 7 hours

## Goal
Create a backend inventory engine that auto-generates purchase orders for low stock.

## Functional Requirements
- Maintain product stock and reorder threshold.
- Deduct stock on sales input.
- Detect low stock products.
- Generate purchase order list:
  - product
  - reorder qty
  - supplier
- Mark purchase order as fulfilled and update stock.

## Non-Functional Requirements
- Prevent negative stock.
- SKU and PO IDs must be unique.

## Concepts Practiced
- `Map<String, ProductRecord>` inventory
- `List<PurchaseOrderRecord>`
- report generation loops

## HLD
- `InventoryService`
- `PoGeneratorService`
- `PoFulfillmentService`
- `StorageService`

## LLD
- `recordSale(invMap, sku, qty): boolean`
- `findLowStock(invMap): List<ProductRecord>`
- `generatePOs(lowStockList): List<PurchaseOrderRecord>`
- `fulfillPO(invMap, poList, poId): boolean`
- `save/load methods`

## Passing Criteria
- Low stock detection correct.
- PO generated with correct quantities.
- Fulfillment updates stock correctly.

## Implementation Roadmap
1. Build inventory map.
2. Add sale and low-stock checks.
3. Add PO generation.
4. Add PO fulfillment and persistence.
