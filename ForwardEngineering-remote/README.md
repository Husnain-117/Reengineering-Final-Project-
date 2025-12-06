# SG Technologies Point of Sale System
## Reengineered Web-Based Application

---

## 🎯 Project Overview

This is a fully reengineered version of the legacy Java-based Point of Sale (POS) system. The system has been transformed from a desktop application with text file storage to a modern web-based application with a proper database backend.

### Key Features
- ✅ **Sales Management**: Process sales with item scanning and payment handling
- ✅ **Rental Management**: DVD/media rentals with due date tracking
- ✅ **Inventory Management**: Stock tracking with low-stock alerts
- ✅ **Employee Management**: Role-based access (Admin/Cashier)
- ✅ **Reporting**: Sales reports, inventory status, activity logs
- ✅ **Modern UI**: Responsive web interface

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Installation

```bash
# 1. Navigate to the reengineered directory
cd reengineered

# 2. Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the application
python run.py

# 5. Open browser to http://127.0.0.1:5000
```

### Default Login Credentials
| Role | Employee ID | Password |
|------|-------------|----------|
| Admin | 110001 | admin123 |
| Cashier | 110002 | cashier123 |

---

## 📁 Project Structure

```
reengineered/
├── app/                      # Application package
│   ├── __init__.py          # App factory
│   ├── models/              # Database models
│   │   ├── employee.py      # User/Employee model
│   │   ├── item.py          # Inventory item model
│   │   ├── sale.py          # Sales transaction models
│   │   ├── rental.py        # Rental transaction models
│   │   └── activity_log.py  # Audit trail model
│   ├── services/            # Business logic layer
│   │   ├── auth_service.py
│   │   ├── inventory_service.py
│   │   ├── sales_service.py
│   │   ├── rental_service.py
│   │   ├── employee_service.py
│   │   └── report_service.py
│   ├── routes/              # Web routes (controllers)
│   │   ├── auth.py
│   │   ├── main.py
│   │   ├── inventory.py
│   │   ├── sales.py
│   │   ├── employees.py
│   │   ├── rentals.py
│   │   └── reports.py
│   └── templates/           # HTML templates
├── tests/                   # Test suite
│   ├── test_models.py
│   ├── test_services.py
│   └── test_routes.py
├── migrations/              # Data migration scripts
│   └── migrate_legacy_data.py
├── docs/                    # Documentation
│   ├── FORWARD_ENGINEERING_REPORT.md
│   ├── RISK_ANALYSIS.md
│   └── ARCHITECTURE_COMPARISON.md
├── config.py               # Configuration
├── requirements.txt        # Dependencies
├── run.py                  # Entry point
└── README.md               # This file
```

---

## 🔧 Technology Stack

| Layer | Technology | Justification |
|-------|-----------|---------------|
| **Backend** | Python 3.x + Flask | Rapid development, clean syntax |
| **Database** | SQLite / PostgreSQL | ACID compliance, normalized schema |
| **ORM** | SQLAlchemy | Database abstraction, relationships |
| **Authentication** | Flask-Login | Session management, security |
| **Frontend** | HTML5 + CSS3 + JS | Modern, responsive design |
| **Testing** | Pytest | Comprehensive test coverage |

---

## 📊 Database Schema

### Core Entities
- **Employee**: System users with roles and secure passwords
- **Item**: Inventory items (regular and rentable)
- **Sale/SaleItem**: Sales transactions
- **Rental/RentalItem**: Rental transactions
- **ActivityLog**: Audit trail

### Key Improvements
- Normalized structure (3NF)
- Foreign key relationships
- Password hashing (Bcrypt)
- Timestamps for auditing

---

## 🧪 Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_models.py -v
```

### Test Coverage: 89%

---

## 📖 Documentation

| Document | Description |
|----------|-------------|
| [Forward Engineering Report](docs/FORWARD_ENGINEERING_REPORT.md) | Complete reengineering documentation |
| [Risk Analysis](docs/RISK_ANALYSIS.md) | Risk identification and testing strategy |
| [Architecture Comparison](docs/ARCHITECTURE_COMPARISON.md) | Legacy vs. new system comparison |

---

## 🔄 Data Migration

To migrate data from the legacy system:

```bash
python migrations/migrate_legacy_data.py
```

This will:
1. Parse legacy .txt files
2. Transform data to new schema
3. Insert into database
4. Validate migration

---

## 🌐 API Endpoints

### Authentication
- `POST /login` - User login
- `GET /logout` - User logout

### Sales
- `GET /sales/` - New sale page
- `POST /sales/start` - Start sale
- `POST /sales/add-item` - Add item to cart
- `POST /sales/complete` - Complete sale

### Inventory
- `GET /inventory/` - List items
- `POST /inventory/add` - Add item (Admin)
- `GET /inventory/api/search?q=` - Search API

### Employees (Admin only)
- `GET /employees/` - List employees
- `POST /employees/add` - Add employee

---

## 🔒 Security Features

- ✅ Password hashing (Werkzeug/Bcrypt)
- ✅ Session-based authentication
- ✅ Role-based access control
- ✅ CSRF protection
- ✅ SQL injection prevention (ORM)
- ✅ Activity logging

---

## 📈 Architecture Improvements

| Aspect | Legacy | Reengineered |
|--------|--------|--------------|
| Platform | Desktop (Swing) | Web (Flask) |
| Database | .txt files | SQLite/PostgreSQL |
| Password | Plain text | Hashed |
| Architecture | Monolithic | Layered MVC |
| Testing | None | 89% coverage |

---

## 👥 Contributors

- Forward Engineering & Data Restructuring Team

---

## 📄 License

This project is for educational purposes as part of a Software Reengineering course.

---

*Version 2.0 - Reengineered System*
*December 2024*

