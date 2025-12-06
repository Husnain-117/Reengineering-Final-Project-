"""
Service Layer Package
======================
Contains business logic services following the Service Layer pattern.

Architecture Benefits:
1. Separates business logic from presentation (routes)
2. Enables reusability across different interfaces
3. Centralizes business rules
4. Facilitates unit testing

Design Pattern: Service Layer / Business Logic Layer
"""

from app.services.auth_service import AuthService
from app.services.inventory_service import InventoryService
from app.services.sales_service import SalesService
from app.services.rental_service import RentalService
from app.services.employee_service import EmployeeService
from app.services.report_service import ReportService

__all__ = [
    'AuthService',
    'InventoryService', 
    'SalesService',
    'RentalService',
    'EmployeeService',
    'ReportService'
]

