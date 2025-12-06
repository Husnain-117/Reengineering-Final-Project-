Project Requirements — Software Reengineering (POS System)

Instructions

Read the instructions very carefully.

1. Project Overview

Students are provided with a legacy desktop-based Point-of-Sale (POS) system originally developed in Java. The current system stores its data in plain .txt files, which is not scalable or maintainable.

The project follows the Software Reengineering Process Model, progressing through the stages of:

Inventory Analysis

Document Restructuring

Reverse Engineering

Code Restructuring

Data Restructuring

Forward Engineering

Goal: Transform the legacy desktop POS system into a modern, web-based system with improved architecture, documentation, data management, and maintainability, demonstrating the ability to apply each phase of the reengineering process systematically.

2. Project Aim

To perform complete software reengineering of the given legacy POS system by applying all stages of the model:

Inventory Analysis – identify, classify, and assess existing software assets.

Document Restructuring – reorganize or recreate technical documentation.

Reverse Engineering – recover design, data structures, and logic from the existing codebase.

Code Restructuring – improve maintainability and readability of the legacy code.

Data Restructuring – redesign and migrate data from plain-text storage to a proper database with a well-designed schema.

Forward Engineering – develop and deliver an improved version of the system as a web-based application using modern technologies and architecture.

3. Technology and Language Choice

The reengineered system must be implemented as a web-based application.

Students may use any programming language, web framework, and database based on their expertise and project goals (for example: Node.js + Express, etc.).

Since the original system uses .txt files for data persistence, students must redesign the data model and migrate all data into a database of their choice (relational or NoSQL). The decision must be justified.

All technology decisions must be explained in the report, including:

Why the chosen programming language is suitable

Why the selected framework supports improved functional or non-functional requirements

Why the chosen database is appropriate

Necessary schema improvements and their justification

Focus: architectural improvement, data quality, maintainability, and clarity of design.

4. Phased Activities and Expected Outputs

Inventory Analysis – Identify all code, libraries, configurations, documentation, and tests. Classify assets (active, obsolete, reusable) and map dependencies.

Document Restructuring – Rebuild or update technical documentation to represent the true system structure.

Reverse Engineering – Analyze legacy code to recover design, workflows, and data structures. Identify code and data smells.

Code Restructuring – Apply refactoring and restructuring to improve modularity, reduce complexity, and improve readability.

Data Restructuring – Redesign and normalize the data model; migrate from .txt files to a proper database with a well-defined schema.

Forward Engineering – Implement the reengineered POS system as a web-based application, ensuring the architecture is modern, modular, maintainable, and improved.

5. Improved Architecture (Requirements)

The reengineered system must present an improved architecture that demonstrates:

Clear separation of concerns

Layered structure (Presentation, Business Logic, Data Access)

Maintainable data flow

Centralized business logic

Database integration using a repository pattern or ORM

Configurable and testable modular design

Use of appropriate design patterns (MVC, Repository, Singleton, Observer, etc.)

Documentation must include:

Both legacy and reengineered architecture diagrams

A comparison table

Clear justification for all design improvements

6. Documentation Requirements
A. Legacy System Documentation (Reverse Engineered)

System overview and module inventory

Extracted architecture and class diagrams

Identified code and data smells

List of current limitations

B. Reengineered System Documentation (Forward Engineered)

Updated architecture and design diagrams

Refactored module and data structures

Database schema, migration plan, and rationale

Technology stack selection and justification

Mapping from legacy components to the new system

Evidence of improved architecture and maintainability

C. Refactoring Documentation

Each team member must identify, perform, and document at least three major refactorings with:

Before and after code

Explanation

Quality impact

7. Team Composition and Work Distribution

Teams of 2–3 members

Each member must contribute to at least one major phase

Each member must document three refactorings

Work distribution must be clearly recorded in a signed table in the report

8. Deliverables

Technical Report covering all model phases, refactorings, and work distribution.

Reengineered Web-Based System Codebase, including database schema, configuration, and deployment instructions.

9. Guidelines

Preserve original system functionality; no unnecessary new features

Justify all architectural, framework, and database decisions

Use version control

Ensure consistency and clarity across all documentation

All improvements must relate back to issues identified in the legacy system

10. Rubric
Total Marks: 110
1. Inventory Analysis & Document Restructuring

ID: inventory_document_restructuring
Marks: 15

Description:
Complete asset inventory; correct classification; accurate dependency mapping; legacy documentation fully reconstructed with diagrams.

Evaluation Guidelines:

List all code, configs, docs, libraries, and tests found

Classify assets (active / obsolete / reusable)

Provide dependency map (modules and external libraries)

Supply legacy diagrams (architecture, class diagrams)

2. Reverse Engineering & Smell Detection

ID: reverse_engineering_smell_detection
Marks: 15

Description:
Strong code understanding; accurate extracted architecture; identifies multiple code/data smells with evidence.

Evaluation Guidelines:

Recover architecture and workflows

Identify code smells with evidence

Identify data smells with evidence

3. Code Restructuring

ID: code_restructuring
Marks: 10

Description:
Comprehensive refactoring; improved modularity and clarity.

Evaluation Guidelines:

Refactorings reduce complexity

Includes before/after code samples

Explains improvements to modularity and readability

4. Data Restructuring

ID: data_restructuring
Marks: 10

Description:
Normalized schema; well-justified data migration.

Evaluation Guidelines:

Provide new database schema

Explain migration plan from .txt to database

Justify choice of relational / NoSQL DB

5. Forward Engineering (Improved Architecture)

ID: forward_engineering_improved_architecture
Marks: 15

Description:
Fully implemented improved architecture with clear layers; justified tech stack; modular and maintainable system.

Evaluation Guidelines:

Layered architecture (Presentation / Business Logic / Data Access)

Justification for tech stack

Use of repository pattern, ORM, or equivalent

6. Reengineering Plan & Migration

ID: reengineering_plan_migration
Marks: 10

Description:
Clear, realistic plan covering all phases; includes timeline, risks, and migration strategy.

Evaluation Guidelines:

Phase-wise plan (inventory → reverse → restructuring → forward engineering)

Timeline with milestones

Risk identification and mitigation

Detailed migration strategy

7. Refactoring Documentation (Individual)

ID: refactoring_documentation_individual
Marks: 10

Description:
Each member documents 3+ major refactorings with before/after code, rationale, and impact.

Evaluation Guidelines:

Each member provides 3+ refactorings

Before and after code present

Rationale and measurable impact explained

8. Risk Analysis & Testing

ID: risk_analysis_testing
Marks: 10

Description:
Key risks identified with mitigation; strong testing evidence (unit, integration, database).

Evaluation Guidelines:

List major risks

Provide mitigation strategies

Include testing artifacts (unit, integration, DB migration tests)

9. Dual Documentation (Legacy ↔ Reengineered)

ID: dual_documentation_legacy_reengineered
Marks: 10

Description:
Complete comparison with diagrams, mapping tables, and justification of changes.

Evaluation Guidelines:

Side-by-side comparison table of legacy vs new system

Mapping of components (legacy → reengineered)

Diagrams for both systems

10. Work Distribution & Team Contribution

ID: work_distribution_team_contribution
Marks: 5

Description:
Clear contribution table; tasks and refactorings documented; all members sign.

Evaluation Guidelines:

Signed contribution table

Tasks mapped to each member

Evidence of contributions (commits, docs)