---
title: Inter-Warehouse Transfer Process
description: How stock is moved between Nova Trading UK Ltd distribution centres.
---

# Inter-Warehouse Transfer Process

Nova Trading UK Ltd operates two distribution centres: Manchester (primary) and Bristol (secondary). Stock is frequently rebalanced between the two.

## When a Transfer Is Triggered

- Bristol falls below its minimum stock threshold for a fast-moving SKU
- A regional promotion requires temporary stock concentration
- Seasonal rebalancing ahead of peak demand periods

## Transfer Steps

### 1. Transfer Request

A warehouse supervisor raises a transfer request in the ERP system, specifying source, destination, SKU, and quantity. The request is validated against the source warehouse's available (non-reserved) stock.

### 2. Dispatch Confirmation

Once picked and loaded, the dispatching warehouse confirms the transfer in the system, which immediately deducts the quantity from the source location's available stock, even though it has not yet arrived at the destination.

### 3. Receipt Confirmation

The receiving warehouse scans the incoming pallets and confirms receipt. Only at this point does the stock become available for sale from the destination location. Goods in transit are visible in the system under a distinct "In Transit" status and cannot be sold from either location during that window.

## Discrepancy Handling

If the received quantity does not match the dispatched quantity, the receiving warehouse must log a discrepancy ticket before confirming receipt. Transfers with unresolved discrepancies remain in "In Transit" status indefinitely and block the source SKU from being used in further transfer requests until resolved.
