# Project Status & Next Steps

## Summary

- Completed rubric phases 1–4: Inventory Analysis, Document Restructuring, Reverse Engineering & Smell Detection, Code Restructuring plan, and Data Restructuring.
- Forward-engineered code is isolated under `forward-engineered/` with an independent API and migration utilities.
- MongoDB Atlas migration implemented with idempotent upserts and normalized parsing; endpoints verified locally.

## Technology Stack

- Legacy (Desktop Java)
  - UI controllers: `src/Transaction_Interface.java:87`, `src/Cashier_Interface.java:106`, `src/Login_Interface.java:26`, `src/Admin_Interface.java:38`
  - Business logic: `src/PointOfSale.java:33`, `src/POS.java:81`, `src/POR.java:55`, `src/POH.java:71`, `src/Inventory.java:26`, `src/Management.java:200`, `src/EmployeeManagement.java:97`
  - Data files: `Database/itemDatabase.txt`, `Database/rentalDatabase.txt`, `Database/employeeDatabase.txt`, `Database/userDatabase.txt`, `Database/saleInvoiceRecord.txt`
- Forward-Engineered (Web)
  - Node.js + Express + Mongoose (MongoDB)
  - API entry: `forward-engineered/api/index.js`
  - Routers: `forward-engineered/api/routes/orders.js`, `forward-engineered/api/routes/rentals.js`, `forward-engineered/api/routes/customers.js`
  - Models: `forward-engineered/api/models/order.js`, `forward-engineered/api/models/rental.js`, `forward-engineered/api/models/customer.js`, `forward-engineered/api/models/product.js`, `forward-engineered/api/models/rentalItem.js`
  - Migration: `forward-engineered/migration/index.js` (dry-run and commit)
  - Config: `.env` per app; keep secrets out of VCS

## Forward-Engineered Structure

```
forward-engineered/
  api/
    index.js
    models/
      order.js
      rental.js
      customer.js
      product.js
      rentalItem.js
    routes/
      orders.js
      rentals.js
      customers.js
    middleware/
      error.js
    package.json
    .env (untracked)
  migration/
    index.js
    package.json
    .env (untracked; `.env.example` provided)
```

## Data Restructuring Highlights

- Money normalized to integer cents; totals computed from items to prevent float drift.
- Idempotent migration via `bulkWrite` upserts keyed by deterministic `orderKey` and `rentalKey`.
- Date parsing
  - Sales timestamps `yyyy-MM-dd HH:mm:ss.SSS` → ISO via `parseTimestamp`
  - Rental dates `MM/DD/YY` → normalized via `parseMMDDYY` with audit `legacyDateStr`
- Skips “Total with tax” lines and drops empty orders during parsing (`forward-engineered/migration/index.js`).

## Endpoints (Verified)

- `GET /api/health` → health check
- `GET /api/products` → paginated products from legacy inventory
- `GET /api/rental-items` → paginated rental items
- `GET /api/orders` → paginated orders with `start`/`end` filters on `orderedAt`
- `GET /api/rentals` → filters `status`, `phone`, `itemId`
- `GET /api/customers` → optional `phone` filter

## Migration Verification (Atlas)

- Products: 101
- Rental Items: 24
- Orders: 26
- Customers: 13
- Rentals: 21

## How to Run Locally

- API
  - `cd forward-engineered/api`
  - `npm install`
  - `npm start`
  - Default port: `3001` (override with `PORT_FWD`)
- Migration
  - `cd forward-engineered/migration`
  - `npm install`
  - `npm run dry-run`
  - `npm run migrate` (requires `MONGODB_URI` set in `.env`)

## Security

- Keep `.env` untracked; never commit secrets
- Use `.env.example` to indicate required variables (e.g., `MONGODB_URI`)
- Consider secret rotation in Atlas when sharing access

## Remaining Tasks (Team Continuation)

- Repositories/Services (Layering)
  - Implement `repositories/*` and `services/*` under `forward-engineered/api` to centralize business rules (tax, discounts, late fees) and data access.
- Auth & Admin
  - Add JWT-based auth; protect admin endpoints for inventory/user management; enforce RBAC.
- Frontend Client
  - Build web UI (e.g., React/Vite) consuming the existing REST endpoints.
- Testing & Quality
  - Unit tests for services; integration tests for repositories; API tests for routers; add `eslint`, `prettier`, and `jest` to `forward-engineered/api/package.json`.
- Documentation (Rubric Continuation)
  - Dual docs (legacy ↔ reengineered) with diagrams and comparison tables.
  - Risk analysis & mitigation; refactoring documentation for each member (3+ with before/after, rationale, impact).
  - Deployment instructions and CI (optional).

## GitHub (Push Only Forward-Engineered and Docs)

- Ensure `.gitignore` excludes `api/.env`, `migration/.env`, and `node_modules/`.
- Commands:

```
git init
git branch -M main
git remote add origin git@github.com:FaheemPechuho/RE-Final-Project.git
git add forward-engineered docs
git commit -m "Add forward-engineered API and migration; update docs"
git push -u origin main
```

## References

- Legacy
  - Inventory access: `src/PointOfSale.java:33`
  - Sales write: `src/POS.java:81`
  - Rental add: `src/POR.java:55`
  - Returns & late fee: `src/POH.java:71`
  - Inventory I/O: `src/Inventory.java:26`, `src/Inventory.java:67`
  - Rentals DB I/O: `src/Management.java:200`
- Forward-Engineered
  - API entry: `forward-engineered/api/index.js`
  - Orders router: `forward-engineered/api/routes/orders.js`
  - Rentals router: `forward-engineered/api/routes/rentals.js`
  - Customers router: `forward-engineered/api/routes/customers.js`
  - Migration: `forward-engineered/migration/index.js`

