# Forward Engineering — Improved Architecture

## Goals

- Deliver a modern, layered web architecture with clear separation of concerns.
- Centralize business rules and enforce data quality via repositories/ORM.
- Provide maintainable modules and configuration for continued development.

## Current Baseline (Implemented)

- API server (Express) with routers and models
  - Routers: `forward-engineered/api/routes/orders.js`, `forward-engineered/api/routes/rentals.js`, `forward-engineered/api/routes/customers.js`
  - Models: `forward-engineered/api/models/order.js`, `forward-engineered/api/models/rental.js`, `forward-engineered/api/models/customer.js`
  - Boot: `forward-engineered/api/index.js` loads `.env` and mounts routers
- Data migration script (Node): `forward-engineered/migration/index.js` parses legacy `.txt` files and commits to MongoDB Atlas
  - Parser fixes and totals: `forward-engineered/migration/index.js`
  - Timestamp parsing: `forward-engineered/migration/index.js`
  - Rental date parsing: `forward-engineered/migration/index.js`
  - Bulk upsert commit: `forward-engineered/migration/index.js`

## Target Layered Architecture

- Presentation
  - Web client (to be added by next team) consuming REST endpoints
  - Typical stack: React/Vite or Angular; not required for your scope here
- API Layer (Controllers/Routers)
  - Location: `forward-engineered/api/routes/*`
  - Responsibility: Input parsing, pagination, calling services, returning DTOs
- Business Logic (Services)
  - Proposed: `forward-engineered/api/services/*` (to add)
  - Responsibility: Orchestrate rules (tax, discounts, late fees), validations, transactions
- Data Access (Repositories)
  - Proposed: `forward-engineered/api/repositories/*` (to add)
  - Responsibility: Abstract persistence via Mongoose models; enforce query hygiene and projections
- Models/ORM
  - Location: `forward-engineered/api/models/*`
  - Responsibility: Schema, indexes, and type enforcement
- Configuration
  - `.env` loaded in `forward-engineered/api/index.js` with `MONGODB_URI`

## Proposed API Folder Structure

```
forward-engineered/api/
  index.js
  models/
    order.js
    rental.js
    customer.js
    product.js
    rentalItem.js
  repositories/
    ordersRepository.js
    rentalsRepository.js
    customersRepository.js
    productsRepository.js
  services/
    orderService.js
    rentalService.js
    inventoryService.js
    authService.js
  routes/
    orders.js
    rentals.js
    customers.js
  middleware/
    error.js
  .env
```

## Repository Pattern (Outline)

- OrdersRepository
  - Methods: `list({ start, end, limit, skip })`, `getByKey(orderKey)`, `createOrUpdate(order)`
  - Backed by model at `forward-engineered/api/models/order.js`
- RentalsRepository
  - Methods: `list({ status, phone, itemId, limit, skip })`, `getByKey(rentalKey)`, `createOrUpdate(rental)`
  - Backed by model at `forward-engineered/api/models/rental.js`
- CustomersRepository
  - Methods: `list({ phone, limit, skip })`, `upsert(phone)`
  - Backed by model at `forward-engineered/api/models/customer.js`
- ProductsRepository (planned)
  - Methods: `list({ limit, skip })`, `upsert(item)`
  - Backed by Product and RentalItem models

## Services (Business Rules)

- OrderService
  - Calculates totals using integer cents; applies tax in basis points (e.g., `taxBps = 600`) and future discounts
  - Validates items and resolves legacy → product references
- RentalService
  - Computes status transitions; handles late fees via configurable rates
  - Normalizes dates and maintains audit trail (`legacyDateStr`)
- InventoryService
  - Applies stock mutations consistently; clamps quantities; rejects negative inventory updates
- AuthService (planned)
  - Password hashing (bcrypt or argon2); JWT issuance; RBAC for admin endpoints

## Endpoints (Current and Planned)

- Current
  - `GET /api/products` — paginated list from `Database/itemDatabase.txt`
  - `GET /api/rental-items` — paginated list from `Database/rentalDatabase.txt`
  - `GET /api/orders` — list with date range filters via `orderedAt` (`forward-engineered/api/routes/orders.js`)
  - `GET /api/rentals` — list with filters `status`, `phone`, `itemId` (`forward-engineered/api/routes/rentals.js`)
  - `GET /api/customers` — list with optional `phone` filter (`forward-engineered/api/routes/customers.js`)
- Planned (post-handoff)
  - `POST /api/orders` — create order; validates via `OrderService`, writes via `OrdersRepository`
  - `POST /api/rentals` — create rental; computes price/late fee policies
  - `PATCH /api/inventory/:id` — admin-only stock updates
  - `POST /api/auth/login` — returns JWT, sets claims

## Design Patterns

- Singleton
  - Legacy `Inventory` is a singleton (`src/Inventory.java:12–24`); in the new system prefer stateless services with DI instead of singletons
- Repository
  - Abstracts persistence; enables swapping between MongoDB and stubs for tests
- MVC (Routers/Controllers ↔ Services ↔ Repositories)
  - Maintains a strict separation of concerns

## Data Quality Practices

- Monetary values stored as integer cents across models and computations
- Deterministic keys (`orderKey`, `rentalKey`) to ensure idempotent migrations and imports
- Indexed fields for performance and integrity: `orderedAt`, `customerPhone`, `legacyRentalItemId`, unique `phone`
- Strict input validation at routers; clamp `limit` ≤ 200, safe `skip` default 0

## Configuration & Security

- `.env` file: `MONGODB_URI` and planned `JWT_SECRET`, `PORT`
- Never commit secrets; rotate credentials in Atlas when sharing
- Add rate limiting and CORS policies as appropriate
- Sanitize inputs; validate IDs and dates

## Testing Plan

- Unit tests for services (totals, late fee calculations)
- Integration tests for repositories (CRUD, filters, pagination)
- API tests for routers (200/400/401/403 cases)
- Migration verification: compare counts and spot-check sample records

## Handoff Checklist

- Implement `repositories/*` and `services/*` according to outlines above
- Add auth (JWT) and secure admin routes
- Create web client to consume the existing endpoints
- Add linting (`eslint`, `prettier`) and a test runner (`jest`) with scripts in `forward-engineered/api/package.json`
