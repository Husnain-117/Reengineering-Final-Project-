# Reverse Engineering & Smell Detection

## Extracted Architecture & Workflows

- Login flow
  - `src/Login_Interface.java` authenticates via `POSSystem.logIn(...)` (`src/POSSystem.java:166`)
  - Role determines next UI: Cashier/Admin
- Cashier workflow
  - `src/Cashier_Interface.java` triggers `Transaction_Interface` with operation: Sale/Rental/Return (`src/Cashier_Interface.java:106`)
- Transaction workflow
  - `src/Transaction_Interface.java` selects `POS` (sale), `POR` (rental), `POH` (returns), and sets DB file accordingly (`src/Transaction_Interface.java:87` and `src/Transaction_Interface.java:95`)
  - `src/PointOfSale.java` initializes with inventory (`src/PointOfSale.java:33`), builds cart (`src/PointOfSale.java:43`), and delegates to operation-specific `endPOS`
- Persistence
  - Inventory: `src/Inventory.java:26` read, `src/Inventory.java:67` write-back
  - Employees: `src/EmployeeManagement.java:97` update, rewrite DB
  - Rentals/Customers: `src/Management.java:200` appends rental entries to `Database/userDatabase.txt`
  - Sales: `src/POS.java:81` writes item lines and `Total with tax`

## Code Smells (Examples)

- Duplicated source trees: `src/*` and `src/src/*` — increases maintenance overhead
- File I/O scattered, no repository layer: direct `FileReader/FileWriter` throughout (`src/Inventory.java:26`, `src/POS.java:81`, `src/Management.java:200`)
- Magic numbers and implicit constants
  - Sales tax embedded via `totalPrice = totalPrice*tax` in `src/POR.java:55` and similar logic; not centralized
  - Late fee rate `0.1` hardcoded in `src/POH.java:99` (within block starting at `src/POH.java:71`)
- Global mutable state in `POSSystem` (`src/POSSystem.java:19` onwards): `username`, `password`, `name`, `employees` — risk of side effects
- Password handling: plaintext passwords in `Database/employeeDatabase.txt` and `src/EmployeeManagement.java` — security risk
- OS-specific path switching sprinkled (commented toggles) in `src/Management.java:12` and others
- Weak validation and error handling
  - Phone parsing with `Long.parseLong` loops in `src/Cashier_Interface.java:69` — no try/catch around invalid inputs
  - Multiple catch blocks only printing to console; no recovery strategy (`src/Inventory.java:47`, `src/POS.java:90`)

## Data Smells (Examples)

- Plain-text storage without normalization: `Database/userDatabase.txt` mixes customer identity and rental history
- Inconsistent monetary precision: floats in item databases lead to rounding errors
- Mixed date formats: `saleInvoiceRecord.txt` uses `yyyy-MM-dd HH:mm:ss.SSS` while `userDatabase.txt` uses `MM/dd/yy`
- Erroneous totals and anomalies: repeated/negative totals in `Database/saleInvoiceRecord.txt` lines such as `Total with tax: -79.5`

## Observations for Reengineering

- Centralize business rules (tax, discounts, late fees) into a service layer
- Introduce repository abstraction for Inventory/Employees/Rentals/Sales
- Normalize data model and migrate to a database with enforced indexes and types
- Keep reengineered web code isolated under `forward-engineered/` to improve clarity and reduce coupling with legacy
