# SG Technologies POS System - Software Reengineering Project

## 📋 Project Overview

This project documents the complete reengineering of the **SG Technologies Point-of-Sale (POS) System** from a legacy Java Swing desktop application to a modern Python Flask web application.

### Team Members
| Name | Roll Number | Primary Contributions |
|------|-------------|----------------------|
| Abdul Faheem | 22i-2629 | Inventory Analysis, Reverse Engineering |
| Sheryar Ali | 22i-2623 | Code Restructuring, Data Restructuring |
| Husnain Akram | 22i-2464 | Forward Engineering, Testing, Migration |

---

## 🔄 Reengineering Phases

The project follows a systematic reengineering approach:

1. **Inventory Analysis & Document Restructuring** - Asset inventory and classification
2. **Reverse Engineering & Smell Detection** - Architecture extraction and code/data smell identification
3. **Code Restructuring** - Refactoring proposals for improved modularity
4. **Data Restructuring** - Schema normalization and migration planning
5. **Forward Engineering** - Modern Flask web application implementation
6. **Reengineering Plan & Migration** - Timeline, risk considerations, and migration strategy
7. **Refactoring Documentation** - 9 major refactorings (3 per team member)
8. **Risk Analysis & Testing** - Risk mitigation and comprehensive test suite
9. **Dual Documentation** - Legacy vs Reengineered comparison
10. **Work Distribution** - Team contributions and sign-off

---

## 🏗️ Architecture Comparison

### Legacy System
- **Platform:** Java Swing Desktop Application
- **Data Storage:** Plain text files (.txt)
- **Architecture:** Monolithic with mixed concerns
- **Security:** Plaintext passwords ⚠️
- **Testing:** No automated tests

### Reengineered System
- **Platform:** Python Flask Web Application
- **Data Storage:** SQLite/PostgreSQL with SQLAlchemy ORM
- **Architecture:** Layered (Presentation → Service → Data Access → Database)
- **Security:** Bcrypt password hashing, Flask-Login sessions
- **Testing:** Pytest suite with 89% coverage

---

## 📁 Project Structure

```
finalReport/
├── main.tex                 # Main LaTeX document (entry point)
├── sections_1_3.tex         # Points 1-3: Inventory, Reverse Eng, Code Restructuring
├── sections_4_6.tex         # Points 4-6: Data Restructuring, Forward Eng, Migration
├── sections_7_10.tex        # Points 7-10: Refactoring, Testing, Dual Docs, Work Dist
├── generate_diagrams.py     # Python script to generate all diagrams
├── images/
│   ├── 1.png - 9.png        # Application screenshots
│   ├── legacy_system_overview.png
│   ├── legacy_dependency_map.png
│   ├── legacy_class_diagram.png
│   ├── code_restructuring.png
│   ├── database_erd.png
│   ├── architecture_comparison.png
│   ├── reengineering_flow.png
│   ├── refactoring_overview.png
│   ├── testing_pyramid.png
│   ├── dual_architecture.png
│   └── data_model_evolution.png
└── README.md
```

---

## 🛠️ Building the Report

### Prerequisites
- LaTeX distribution (TeX Live, MiKTeX, or similar)
- Python 3.x with matplotlib (for diagram generation)

### Generate Diagrams
```bash
cd finalReport
python generate_diagrams.py
```

### Compile LaTeX
```bash
pdflatex main.tex
pdflatex main.tex  # Run twice for table of contents
```

Or use **Overleaf**:
1. Upload the `finalReport` folder to Overleaf
2. Set `main.tex` as the main document
3. Compile

---

## 📊 Key Deliverables

### Code Smells Identified
| ID | Smell | Location |
|----|-------|----------|
| CS1 | Duplicated Source Trees | src/ and src/src/ |
| CS2 | Scattered File I/O | Multiple classes |
| CS3 | Magic Numbers | POH.java:71 |
| CS4 | Global Mutable State | POSSystem.java |
| CS5 | Plaintext Passwords | POSSystem.java:166 |

### Data Smells Identified
| ID | Smell | Location |
|----|-------|----------|
| DS1 | 1NF Violation | userDatabase.txt |
| DS2 | Plaintext Passwords | employeeDatabase.txt |
| DS3 | Inconsistent Formats | Multiple files |

### Individual Refactorings (9 Total)
- **AF-1, AF-2, AF-3:** Login workflow, Repository abstraction, Data normalization
- **SA-1, SA-2, SA-3:** File→Repository, Late fee service, Unified item model
- **HA-1, HA-2, HA-3:** Thin controller, Atomic transactions, Secure authentication

---

## 🧪 Testing

The reengineered system includes comprehensive testing:

| Test Type | Coverage | Files |
|-----------|----------|-------|
| Unit Tests | 60% | test_models.py, test_services.py |
| Integration Tests | 30% | test_routes.py |
| Database Tests | - | test_database.py |

**Overall Coverage:** 89% | **Total Tests:** 37 | **All Passing:** ✓

---

## 📝 License

This project is submitted as part of the **Software Reengineering** course (BSSE, Semester 7).

---

## 🔗 Links

- **GitHub Repository:** [https://github.com/Husnain-117/Reengineering-Final-Project-](https://github.com/Husnain-117/Reengineering-Final-Project-)
- **Course:** Software Reengineering - Fall 2024

---

*Last Updated: December 2024*
