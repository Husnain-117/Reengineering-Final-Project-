# Code Restructuring

## Goals

- Improve modularity and readability
- Reduce duplication and side effects
- Prepare for repository-driven persistence

## Proposed Refactorings (Legacy)

- Consolidate duplicated trees
  - Remove `src/src/*` duplicate classes; keep a single `src/` with packages (e.g., `interfaces`, `bl`)
- Relocate forward-engineered code
  - Place all new web code under `forward-engineered/` (e.g., `forward-engineered/api`, `forward-engineered/migration`) to separate from legacy
- Extract repositories from file I/O
  - Define interfaces (e.g., `InventoryRepository`, `EmployeeRepository`, `RentalRepository`, `SalesRepository`)
  - Implement text-backed adapters initially; later swap to DB-backed implementations
- Encapsulate business rules
  - Create `TransactionService` to handle tax, discounts, and late fee calculations invoked by UI controllers
- Input validation and error handling
  - Wrap user inputs (phone, card) with validators; avoid `Long.parseLong` loops without try/catch

## Before/After Illustrations (Conceptual)

- Before (direct file write of sales): `src/POS.java:81`

```java
bw2.write("Total with tax: "+totalPrice);
```

- After (repository call)

```java
salesRepository.appendInvoice(order);
```

- Before (late fee inline calculation): `src/POH.java:71`

```java
itemPrice = amount * price * 0.1 * days;
```

- After (service call)

```java
itemPrice = lateFeeService.calculate(amount, price, days);
```

## Restructuring Plan

- Phase 1: Directory cleanup and package declarations
- Phase 1.1: Create `forward-engineered/` for new web code to avoid mixing with legacy
- Phase 2: Introduce repository interfaces and swap file calls
- Phase 3: Add services for business rules; unit tests for calculations
