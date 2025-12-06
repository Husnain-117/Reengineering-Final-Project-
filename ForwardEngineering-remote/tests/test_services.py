"""
Unit Tests for Service Layer
==============================
Tests for business logic services.
"""

import pytest
from app.services.auth_service import AuthService
from app.services.inventory_service import InventoryService
from app.services.sales_service import SalesService
from app.models import Employee, Item


class TestAuthService:
    """Tests for Authentication Service."""
    
    def test_authenticate_valid_credentials(self, app, init_database):
        """Test authentication with valid credentials."""
        with app.app_context():
            success, employee, message = AuthService.authenticate('100001', 'testpass')
            
            assert success is True
            assert employee is not None
            assert employee.employee_id == '100001'
    
    def test_authenticate_invalid_password(self, app, init_database):
        """Test authentication with wrong password."""
        with app.app_context():
            success, employee, message = AuthService.authenticate('100001', 'wrongpass')
            
            assert success is False
            assert employee is None
    
    def test_authenticate_invalid_user(self, app, init_database):
        """Test authentication with non-existent user."""
        with app.app_context():
            success, employee, message = AuthService.authenticate('999999', 'testpass')
            
            assert success is False
            assert employee is None
    
    def test_is_admin(self, app, init_database):
        """Test admin check."""
        with app.app_context():
            admin = Employee.query.filter_by(employee_id='100001').first()
            cashier = Employee.query.filter_by(employee_id='100002').first()
            
            assert AuthService.is_admin(admin) is True
            assert AuthService.is_admin(cashier) is False


class TestInventoryService:
    """Tests for Inventory Service."""
    
    def test_get_all_items(self, app, init_database):
        """Test getting all items."""
        with app.app_context():
            items = InventoryService.get_all_items()
            
            assert len(items) >= 3  # We created 3 test items
    
    def test_get_item_by_code(self, app, init_database):
        """Test getting item by code."""
        with app.app_context():
            item = InventoryService.get_item_by_code('T001')
            
            assert item is not None
            assert item.name == 'Test Item 1'
            assert item.price == 10.0
    
    def test_search_items(self, app, init_database):
        """Test item search."""
        with app.app_context():
            # Search by name
            items = InventoryService.search_items('Test Item')
            assert len(items) >= 2
            
            # Search by code
            items = InventoryService.search_items('T001')
            assert len(items) >= 1
    
    def test_create_item(self, app, init_database):
        """Test creating new item."""
        with app.app_context():
            success, item, message = InventoryService.create_item(
                item_code='NEW001',
                name='New Test Item',
                price=15.99,
                quantity=50,
                category='New Category'
            )
            
            assert success is True
            assert item is not None
            assert item.item_code == 'NEW001'
    
    def test_create_duplicate_item(self, app, init_database):
        """Test creating item with duplicate code."""
        with app.app_context():
            success, item, message = InventoryService.create_item(
                item_code='T001',  # Already exists
                name='Duplicate Item',
                price=10.0,
                quantity=10
            )
            
            assert success is False
            assert 'already exists' in message
    
    def test_update_item(self, app, init_database):
        """Test updating item."""
        with app.app_context():
            item = InventoryService.get_item_by_code('T001')
            
            success, updated_item, message = InventoryService.update_item(
                item.id,
                name='Updated Item Name',
                price=12.99
            )
            
            assert success is True
            assert updated_item.name == 'Updated Item Name'
            assert updated_item.price == 12.99
    
    def test_update_quantity(self, app, init_database):
        """Test quantity update."""
        with app.app_context():
            item = InventoryService.get_item_by_code('T001')
            original_qty = item.quantity
            
            success, message = InventoryService.update_quantity(
                item.id, 10, 'subtract'
            )
            
            assert success is True
            assert item.quantity == original_qty - 10


class TestSalesService:
    """Tests for Sales Service."""
    
    def test_create_sale(self, app, init_database):
        """Test creating new sale."""
        with app.app_context():
            employee = Employee.query.filter_by(employee_id='100001').first()
            
            sale = SalesService.create_sale(employee.id)
            
            assert sale is not None
            assert sale.transaction_id is not None
            assert sale.status == 'in_progress'
    
    def test_add_item_to_sale(self, app, init_database):
        """Test adding item to sale."""
        with app.app_context():
            employee = Employee.query.filter_by(employee_id='100001').first()
            sale = SalesService.create_sale(employee.id)
            
            success, message, sale_item = SalesService.add_item_to_sale(
                sale.id, 'T001', quantity=2
            )
            
            assert success is True
            assert sale_item is not None
            assert sale_item.quantity == 2
    
    def test_add_invalid_item_to_sale(self, app, init_database):
        """Test adding non-existent item to sale."""
        with app.app_context():
            employee = Employee.query.filter_by(employee_id='100001').first()
            sale = SalesService.create_sale(employee.id)
            
            success, message, sale_item = SalesService.add_item_to_sale(
                sale.id, 'INVALID', quantity=1
            )
            
            assert success is False
            assert 'not found' in message
    
    def test_complete_sale(self, app, init_database):
        """Test completing sale."""
        with app.app_context():
            employee = Employee.query.filter_by(employee_id='100001').first()
            sale = SalesService.create_sale(employee.id)
            
            # Add item
            SalesService.add_item_to_sale(sale.id, 'T001', quantity=2)
            
            # Complete sale (item price is 10.0, qty 2 = 20.0 + tax)
            success, message, completed_sale = SalesService.complete_sale(
                sale.id, 
                amount_paid=25.0, 
                payment_method='Cash'
            )
            
            assert success is True
            assert completed_sale.status == 'completed'
            assert completed_sale.payment_method == 'Cash'
    
    def test_insufficient_payment(self, app, init_database):
        """Test sale with insufficient payment."""
        with app.app_context():
            employee = Employee.query.filter_by(employee_id='100001').first()
            sale = SalesService.create_sale(employee.id)
            
            # Add item (price 10.0)
            SalesService.add_item_to_sale(sale.id, 'T001', quantity=2)
            
            # Try to complete with insufficient payment
            success, message, completed_sale = SalesService.complete_sale(
                sale.id,
                amount_paid=5.0,  # Less than total
                payment_method='Cash'
            )
            
            assert success is False
            assert 'Insufficient payment' in message

