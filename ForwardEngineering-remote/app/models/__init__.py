"""
Database Models Package
========================
Contains all SQLAlchemy models representing the normalized database schema.

Schema Design Improvements over Legacy:
1. Normalized tables eliminating data redundancy
2. Proper foreign key relationships
3. Password hashing for security
4. Timestamps for audit trails
5. Proper data types (vs text file strings)
6. Referential integrity constraints
"""

from app.models.employee import Employee
from app.models.item import Item
from app.models.sale import Sale, SaleItem
from app.models.rental import Rental, RentalItem
from app.models.activity_log import ActivityLog

__all__ = ['Employee', 'Item', 'Sale', 'SaleItem', 'Rental', 'RentalItem', 'ActivityLog']

