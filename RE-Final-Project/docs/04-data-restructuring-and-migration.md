# Data Restructuring & Migration

## Target Schema (MongoDB)

- `products`
  - `legacyId` (Number, unique), `name` (String), `salePriceCents` (Number), `stock` (Number), `isActive` (Boolean)
- `rentalItems`
  - `legacyId` (Number, unique), `name` (String), `rentalPriceCents` (Number), `stock` (Number), `isActive` (Boolean)
- `orders`
  - `orderKey` (String, unique), `orderedAt` (Date, index), `cashierUsername` (String), `items` (Array of `{ legacyProductId, name, qty, unitPriceCents }`), `totals` (`{ subtotalCents, taxCents, discountCents, grandCents }`), `source` (String)
- `rentals`
  - `rentalKey` (String, unique), `customerPhone` (String, index), `legacyRentalItemId` (Number, index), `rentedAt` (Date), `returnedAt` (Date), `legacyDateStr` (String), `status` (`rented|returned`), `source` (String)
- `customers`
  - `phone` (String, unique)
- `users` (future work)
  - `username` (unique), `role`, `name`, `passwordHash`

## Mapping from Legacy Files

- `Database/itemDatabase.txt` → `products`
- `Database/rentalDatabase.txt` → `rentalItems`
- `Database/employeeDatabase.txt` → `users`
- `Database/userDatabase.txt` → `rentals` grouped by `phone`; derive `customers`
- `Database/saleInvoiceRecord.txt` → `orders` using timestamp blocks and item lines

## Migration Rules

- Money normalized to integer cents; avoid floating-point drift
- Sales timestamps parsed from `yyyy-MM-dd HH:mm:ss.SSS`; discard "Total with tax" lines and drop empty orders
- Rental dates parsed from `MM/dd/yy`; preserve `legacyDateStr` for auditing
- Deterministic keys (`orderKey`, `rentalKey`) ensure idempotent upserts

## Implementation References

- Parser fixes and totals computation: `forward-engineered/migration/index.js`
- Timestamp parsing utilities: `forward-engineered/migration/index.js`
- Rental date parsing: `forward-engineered/migration/index.js`
- Bulk upsert commit pipeline: `forward-engineered/migration/index.js`
- DB count summary after commit: `forward-engineered/migration/index.js`

## Verification Summary

- Post-migration counts (Atlas):
  - Products: 101
  - Rental Items: 24
  - Orders: 26
  - Customers: 13
  - Rentals: 21

## Handoff Notes

- Keep `.env` files untracked and secure; configure `MONGODB_URI` for the team’s environment
- Migration reads `MONGODB_URI` from `server/.env` by default; you may relocate to `forward-engineered/migration/.env` if you update the script path
- Forward Engineering, Testing, and Auth will be handled by the next team members per project requirements
