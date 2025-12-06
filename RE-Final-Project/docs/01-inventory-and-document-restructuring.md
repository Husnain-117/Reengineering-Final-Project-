# Inventory Analysis & Document Restructuring

## Asset Inventory

- Code (legacy Java)
  - UI: `src/Login_Interface.java`, `src/Cashier_Interface.java`, `src/Admin_Interface.java`, `src/Transaction_Interface.java`
  - Business logic: `src/PointOfSale.java`, `src/POS.java`, `src/POR.java`, `src/POH.java`, `src/POSSystem.java`, `src/Inventory.java`, `src/Management.java`, `src/EmployeeManagement.java`, `src/Item.java`, `src/Employee.java`
  - Note: duplicated copies under `src/src/...` (interfaces and bl) — treat as obsolete duplicates for restructuring
- Data files (plain text)
  - Inventory: `Database/itemDatabase.txt`, `Database/rentalDatabase.txt`
  - Employees: `Database/employeeDatabase.txt`
  - Rentals/Customers: `Database/userDatabase.txt`
  - Sales invoices: `Database/saleInvoiceRecord.txt`
  - Temporary: `Database/newTemp.txt`, `Database/newEmployeeDatabase.txt`
- Forward-engineered code (Node.js)
  - API: `forward-engineered/api/index.js`, routers in `forward-engineered/api/routes/*`, models in `forward-engineered/api/models/*`
  - Config: `forward-engineered/api/.env` (contains `MONGODB_URI`; do not commit secrets)
  - Migration utilities: `forward-engineered/migration/index.js`, `forward-engineered/migration/package.json`

## Classification (Active / Obsolete / Reusable)

- Active (legacy)
  - `src/PointOfSale.java`, `src/POS.java`, `src/POR.java`, `src/POH.java`, `src/POSSystem.java`, `src/Inventory.java`, `src/Management.java`, `src/EmployeeManagement.java`, `src/Transaction_Interface.java`
- Obsolete or duplicate
  - `src/src/interfaces/*` and `src/src/bl/*` duplicates of legacy classes; unify to a single `src/` tree
  - Temporary DB files: `Database/newTemp.txt`, `Database/newEmployeeDatabase.txt` are intermediate artifacts
- Reusable for forward engineering
  - Data files as migration sources under `Database/*`
  - Extracted domain concepts in Java (Item, Employee) — use as reference models
  - Forward-engineered API and migration under `forward-engineered/*`

## Dependency Map (Legacy)

- UI → Business
  - `src/Login_Interface.java` calls `POSSystem.logIn(...)` (`src/POSSystem.java:166`)
  - `src/Cashier_Interface.java` launches `Transaction_Interface` based on operation (`src/Cashier_Interface.java:106`)
  - `src/Admin_Interface.java` uses `EmployeeManagement` (`src/Admin_Interface.java:35`)
- Business → Persistence
  - `src/PointOfSale.java` orchestrates transactions; starts with inventory access (`src/PointOfSale.java:33`)
  - Sale writes to invoices in `src/POS.java:81`
  - Rental updates via `src/POR.java:55`; returns compute late fees in `src/POH.java:71`
  - Inventory read/update in `src/Inventory.java:26` and `src/Inventory.java:67`
  - Rentals/Customers maintained via `src/Management.java:200`

## Document Restructuring Plan

- Consolidate legacy code under a single `src/` tree; mark `src/src/*` duplicates as obsolete
- Establish `docs/` directory with phase-focused files to support team handoff:
  - `docs/01-inventory-and-document-restructuring.md` (this file)
  - `docs/02-reverse-engineering-and-smell-detection.md`
  - `docs/03-code-restructuring.md`
  - `docs/04-data-restructuring-and-migration.md`
- Record code references using `file_path:line_number` for precise traceability
