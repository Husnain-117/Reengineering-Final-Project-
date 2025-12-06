# Forward Engineering Report
## SG Technologies Point of Sale System - Reengineered

---

## Table of Contents
1. [Executive Summary](#executive-summary)
2. [Technology Stack Selection](#technology-stack-selection)
3. [Architecture Design](#architecture-design)
4. [Data Restructuring](#data-restructuring)
5. [Component Mapping](#component-mapping)
6. [Risk Analysis & Testing](#risk-analysis--testing)
7. [Deployment Guide](#deployment-guide)

---

## 1. Executive Summary

This document details the forward engineering process for transforming the legacy Java desktop POS system into a modern web-based application. The reengineered system addresses all identified limitations and code smells while maintaining full functionality.

### Key Achievements
- ✅ Transformed from desktop to web-based architecture
- ✅ Migrated from .txt files to normalized SQLite/PostgreSQL database
- ✅ Implemented secure password hashing (vs plain text)
- ✅ Added proper layered architecture (MVC + Service Layer)
- ✅ Implemented comprehensive audit logging
- ✅ Added modern responsive UI
- ✅ Comprehensive test coverage

---

## 2. Technology Stack Selection

### 2.1 Programming Language: Python 3.x

**Justification:**
- **Readability**: Python's clean syntax improves maintainability
- **Rapid Development**: Faster development cycle than Java
- **Rich Ecosystem**: Extensive libraries for web development
- **Community Support**: Large, active community for troubleshooting

**Comparison with Legacy:**
| Aspect | Legacy (Java) | Reengineered (Python) |
|--------|--------------|----------------------|
| Lines of Code | ~2500 | ~1800 |
| Setup Time | Complex | Simple (pip install) |
| Deployment | JAR file | WSGI server |
| Testing | JUnit | Pytest (simpler) |

### 2.2 Web Framework: Flask

**Justification:**
- **Lightweight**: Minimal overhead, only what's needed
- **Flexibility**: Easy to customize architecture
- **Blueprint Support**: Modular route organization
- **Extension Ecosystem**: Flask-SQLAlchemy, Flask-Login, etc.
- **Learning Curve**: Gentler than Django for this project scope

**Why Flask over Django:**
- POS system is focused (doesn't need Django's kitchen sink)
- More control over architecture decisions
- Simpler for understanding/maintenance

### 2.3 Database: SQLite (Development) / PostgreSQL (Production)

**Justification:**
- **SQLite for Development**: Zero configuration, file-based
- **PostgreSQL for Production**: ACID compliance, scalability
- **SQLAlchemy ORM**: Database-agnostic code

**Comparison with Legacy .txt Files:**
| Feature | .txt Files | Relational DB |
|---------|-----------|---------------|
| Data Integrity | None | Constraints |
| Concurrent Access | File locks | Transactions |
| Query Capability | Parse entire file | SQL queries |
| Relationships | Embedded/duplicated | Foreign keys |
| Scalability | Poor | Excellent |

### 2.4 ORM: SQLAlchemy

**Justification:**
- **Repository Pattern**: Abstracts database operations
- **Migration Support**: Schema evolution via Flask-Migrate
- **Query Building**: Type-safe, readable queries
- **Relationship Handling**: Automatic joins, lazy loading

---

## 3. Architecture Design

### 3.1 Architectural Pattern: Layered Architecture + MVC

```
┌─────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                        │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────────┐ │
│  │   Routes    │ │  Templates  │ │     Static Assets       │ │
│  │ (Flask BP)  │ │  (Jinja2)   │ │    (CSS, JS)            │ │
│  └─────────────┘ └─────────────┘ └─────────────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│                    BUSINESS LOGIC LAYER                      │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────────┐ │
│  │AuthService  │ │SalesService │ │   InventoryService      │ │
│  └─────────────┘ └─────────────┘ └─────────────────────────┘ │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────────┐ │
│  │RentalService│ │EmployeeServ│ │   ReportService         │ │
│  └─────────────┘ └─────────────┘ └─────────────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│                    DATA ACCESS LAYER                         │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────────┐ │
│  │  Employee   │ │    Item     │ │   Sale / SaleItem       │ │
│  └─────────────┘ └─────────────┘ └─────────────────────────┘ │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────────┐ │
│  │   Rental    │ │ RentalItem  │ │   ActivityLog           │ │
│  └─────────────┘ └─────────────┘ └─────────────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│                    DATABASE LAYER                            │
│               SQLite / PostgreSQL                            │
└─────────────────────────────────────────────────────────────┘
```

### 3.2 Design Patterns Used

| Pattern | Implementation | Benefit |
|---------|---------------|---------|
| **MVC** | Flask Blueprints + Templates + Models | Separation of concerns |
| **Repository** | SQLAlchemy Models | Data access abstraction |
| **Service Layer** | `app/services/` | Centralized business logic |
| **Factory** | `create_app()` | Configurable app creation |
| **Singleton** | Flask extensions (db, login_manager) | Single instance guarantee |
| **Blueprint** | Route modules | Modular code organization |

### 3.3 Legacy vs Reengineered Architecture

**Legacy Architecture:**
```
┌─────────────────────────────┐
│     Monolithic Classes      │
│  (UI + Logic + Data Mixed)  │
├─────────────────────────────┤
│        File I/O             │
│    (Direct txt access)      │
├─────────────────────────────┤
│      .txt Files             │
└─────────────────────────────┘
```

**Reengineered Architecture:**
- Clear layer separation
- Independent testability
- Centralized business rules
- Database abstraction

---

## 4. Data Restructuring

### 4.1 Schema Design

#### Entity Relationship Diagram
```
┌──────────────┐       ┌──────────────┐       ┌──────────────┐
│   Employee   │       │     Sale     │       │   SaleItem   │
├──────────────┤       ├──────────────┤       ├──────────────┤
│ id (PK)      │───┐   │ id (PK)      │───┐   │ id (PK)      │
│ employee_id  │   └──>│ employee_id  │   └──>│ sale_id (FK) │
│ first_name   │       │ transaction_id│      │ item_id (FK) │──┐
│ last_name    │       │ subtotal     │       │ quantity     │  │
│ role         │       │ tax_amount   │       │ unit_price   │  │
│ password_hash│       │ total        │       │ line_total   │  │
│ is_active    │       │ status       │       └──────────────┘  │
│ created_at   │       │ created_at   │                         │
└──────────────┘       └──────────────┘                         │
                                                                │
┌──────────────┐       ┌──────────────┐       ┌──────────────┐  │
│    Rental    │       │  RentalItem  │       │     Item     │<─┘
├──────────────┤       ├──────────────┤       ├──────────────┤
│ id (PK)      │───┐   │ id (PK)      │       │ id (PK)      │
│ rental_id    │   └──>│ rental_id(FK)│       │ item_code    │
│ customer_phone│      │ item_id (FK) │───────>│ name         │
│ employee_id  │       │ quantity     │       │ price        │
│ status       │       │ is_returned  │       │ quantity     │
│ due_date     │       │ return_date  │       │ category     │
└──────────────┘       └──────────────┘       │ is_rentable  │
                                              └──────────────┘
```

### 4.2 Legacy to New Schema Mapping

| Legacy File | New Table(s) | Key Changes |
|-------------|--------------|-------------|
| `employeeDatabase.txt` | `employees` | Password hashing, separated names, timestamps |
| `itemDatabase.txt` | `items` | Added category, min_stock_level, is_rentable |
| `rentalDatabase.txt` | `items` (is_rentable=True) | Merged into items table |
| `userDatabase.txt` | `rentals`, `rental_items` | Normalized structure |
| `saleInvoiceRecord.txt` | `sales`, `sale_items` | Proper transaction records |
| `employeeLogfile.txt` | `activity_logs` | Structured audit trail |

### 4.3 Normalization Improvements

**Before (1NF Violation in userDatabase.txt):**
```
6096515668 1000,6/30/09,true 1022,6/31/11,true
```

**After (Normalized Tables):**
```sql
-- rentals table
id | rental_id | customer_phone | status
1  | RENT-001  | 6096515668     | returned

-- rental_items table
id | rental_id | item_id | is_returned | return_date
1  | 1         | 1       | true        | 2009-06-30
2  | 1         | 22      | true        | 2011-06-31
```

### 4.4 Data Migration Strategy

1. **Parse Legacy Files**: Read and parse .txt files
2. **Transform Data**: Map to new schema format
3. **Validate**: Check data integrity
4. **Load**: Insert into database with relationships
5. **Verify**: Count records, spot check data

See: `migrations/migrate_legacy_data.py`

---

## 5. Component Mapping

### Legacy to Reengineered Component Mapping

| Legacy Component | Reengineered Component | Improvements |
|-----------------|----------------------|--------------|
| `Register.java` | `run.py` | Application factory pattern |
| `Login_Interface.java` | `routes/auth.py`, `templates/auth/` | Session-based auth, secure passwords |
| `Admin_Interface.java` | `routes/main.py`, `templates/main/admin_dashboard.html` | Role-based access |
| `Cashier_Interface.java` | `routes/main.py`, `templates/main/cashier_dashboard.html` | Modern UI |
| `Employee.java` | `models/employee.py` | Password hashing, relationships |
| `EmployeeManagement.java` | `services/employee_service.py` | CRUD with validation |
| `Item.java` | `models/item.py` | Stock tracking, categories |
| `Inventory.java` | `services/inventory_service.py` | Search, low stock alerts |
| `POS.java` | `services/sales_service.py` | Transaction management |
| `POR.java` | `services/rental_service.py` | Due date tracking |
| `POH.java` | `services/rental_service.py` | Return processing |
| `.txt files` | SQLite/PostgreSQL | ACID compliance |

---

## 6. Risk Analysis & Testing

### 6.1 Risk Identification & Mitigation

| Risk | Likelihood | Impact | Mitigation Strategy |
|------|-----------|--------|---------------------|
| **Data Loss During Migration** | Medium | Critical | Backup original files, validate counts, staged rollout |
| **Authentication Bypass** | Low | Critical | Use Flask-Login, session management, password hashing |
| **SQL Injection** | Low | High | SQLAlchemy ORM parameterized queries |
| **Concurrent Transaction Issues** | Medium | Medium | Database transactions, proper locking |
| **Performance Degradation** | Low | Medium | Query optimization, indexing, caching |
| **Browser Compatibility** | Low | Low | Modern CSS, progressive enhancement |
| **Data Integrity Issues** | Medium | High | Foreign key constraints, validation |
| **Session Hijacking** | Low | High | Secure cookies, HTTPS in production |

### 6.2 Testing Strategy

#### Unit Tests (`tests/test_models.py`, `tests/test_services.py`)
- Model creation and validation
- Password hashing verification
- Business logic correctness
- Stock calculations

#### Integration Tests (`tests/test_routes.py`)
- API endpoint responses
- Authentication flow
- CRUD operations via routes

#### Test Coverage Summary
| Component | Tests | Coverage |
|-----------|-------|----------|
| Models | 10 | Employee, Item, Sale |
| Services | 15 | Auth, Inventory, Sales |
| Routes | 12 | Auth, Inventory, Sales, Employees |
| **Total** | **37** | Core functionality |

### 6.3 Running Tests

```bash
# Install test dependencies
pip install pytest pytest-flask pytest-cov

# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_models.py

# Run with verbose output
pytest -v
```

---

## 7. Deployment Guide

### 7.1 Development Setup

```bash
# 1. Navigate to reengineered directory
cd reengineered

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or: venv\Scripts\activate  # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run development server
python run.py

# 5. Access at http://127.0.0.1:5000
# Default login: 
#   Admin: 110001 / admin123
#   Cashier: 110002 / cashier123
```

### 7.2 Data Migration

```bash
# Run migration script
python migrations/migrate_legacy_data.py
```

### 7.3 Production Deployment

```bash
# Install production server
pip install gunicorn

# Run with Gunicorn
export FLASK_ENV=production
gunicorn -w 4 -b 0.0.0.0:8000 'app:create_app("production")'
```

### 7.4 Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Session encryption key | dev-secret-key |
| `DATABASE_URL` | Database connection string | sqlite:///pos_system.db |
| `FLASK_ENV` | Environment (development/production) | development |

---

## Appendix

### A. File Structure
```
reengineered/
├── app/
│   ├── __init__.py          # Application factory
│   ├── models/              # SQLAlchemy models
│   │   ├── employee.py
│   │   ├── item.py
│   │   ├── sale.py
│   │   ├── rental.py
│   │   └── activity_log.py
│   ├── services/            # Business logic
│   │   ├── auth_service.py
│   │   ├── inventory_service.py
│   │   ├── sales_service.py
│   │   ├── rental_service.py
│   │   └── report_service.py
│   ├── routes/              # Flask blueprints
│   │   ├── auth.py
│   │   ├── main.py
│   │   ├── inventory.py
│   │   ├── sales.py
│   │   ├── employees.py
│   │   ├── rentals.py
│   │   └── reports.py
│   └── templates/           # Jinja2 templates
├── tests/                   # Test suite
├── migrations/              # Data migration scripts
├── docs/                    # Documentation
├── config.py                # Configuration
├── requirements.txt         # Dependencies
└── run.py                   # Entry point
```

### B. API Endpoints

| Endpoint | Method | Description | Auth Required |
|----------|--------|-------------|---------------|
| `/login` | GET/POST | User login | No |
| `/logout` | GET | User logout | Yes |
| `/dashboard` | GET | Main dashboard | Yes |
| `/sales/` | GET | New sale page | Yes |
| `/sales/start` | POST | Start sale | Yes |
| `/sales/add-item` | POST | Add item to sale | Yes |
| `/sales/complete` | POST | Complete sale | Yes |
| `/inventory/` | GET | List items | Yes |
| `/inventory/add` | GET/POST | Add item | Admin |
| `/employees/` | GET | List employees | Admin |
| `/reports/` | GET | Reports dashboard | Admin |

---

*Document Version: 1.0*
*Last Updated: December 2024*
*Author: Forward Engineering Team*

