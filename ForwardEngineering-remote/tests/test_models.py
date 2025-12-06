"""
Unit Tests for Database Models
===============================
Tests for model creation, validation, and methods.
"""

import pytest
from app.models import Employee, Item, Sale, SaleItem


class TestEmployeeModel:
    """Tests for Employee model."""
    
    def test_create_employee(self, app):
        """Test employee creation."""
        with app.app_context():
            from app import db
            
            employee = Employee(
                employee_id='999999',
                first_name='John',
                last_name='Doe',
                password='secret123',
                role='Cashier'
            )
            db.session.add(employee)
            db.session.commit()
            
            assert employee.id is not None
            assert employee.employee_id == '999999'
            assert employee.full_name == 'John Doe'
            assert employee.role == 'Cashier'
            assert not employee.is_admin
    
    def test_password_hashing(self, app):
        """Test password is properly hashed."""
        with app.app_context():
            employee = Employee(
                employee_id='999998',
                first_name='Jane',
                last_name='Doe',
                password='mypassword',
                role='Admin'
            )
            
            # Password should not be stored in plain text
            assert employee.password_hash != 'mypassword'
            
            # Password verification should work
            assert employee.check_password('mypassword')
            assert not employee.check_password('wrongpassword')
    
    def test_is_admin_property(self, app):
        """Test is_admin property."""
        with app.app_context():
            admin = Employee(
                employee_id='999997',
                first_name='Admin',
                last_name='User',
                password='admin',
                role='Admin'
            )
            
            cashier = Employee(
                employee_id='999996',
                first_name='Cashier',
                last_name='User',
                password='cashier',
                role='Cashier'
            )
            
            assert admin.is_admin is True
            assert cashier.is_admin is False


class TestItemModel:
    """Tests for Item model."""
    
    def test_create_item(self, app):
        """Test item creation."""
        with app.app_context():
            from app import db
            
            item = Item(
                item_code='TEST001',
                name='Test Product',
                price=9.99,
                quantity=100,
                category='Test'
            )
            db.session.add(item)
            db.session.commit()
            
            assert item.id is not None
            assert item.item_code == 'TEST001'
            assert item.price == 9.99
            assert item.quantity == 100
    
    def test_low_stock_detection(self, app):
        """Test low stock detection."""
        with app.app_context():
            item = Item(
                item_code='LOW001',
                name='Low Stock Item',
                price=5.0,
                quantity=5
            )
            item.min_stock_level = 10
            
            assert item.is_low_stock is True
            assert item.is_out_of_stock is False
    
    def test_out_of_stock_detection(self, app):
        """Test out of stock detection."""
        with app.app_context():
            item = Item(
                item_code='OUT001',
                name='Out of Stock Item',
                price=5.0,
                quantity=0
            )
            
            assert item.is_out_of_stock is True
    
    def test_update_quantity(self, app):
        """Test quantity update methods."""
        with app.app_context():
            item = Item(
                item_code='QTY001',
                name='Quantity Test',
                price=10.0,
                quantity=50
            )
            
            # Test subtract
            result = item.update_quantity(10, 'subtract')
            assert result is True
            assert item.quantity == 40
            
            # Test add
            result = item.update_quantity(20, 'add')
            assert result is True
            assert item.quantity == 60
            
            # Test insufficient stock
            result = item.update_quantity(100, 'subtract')
            assert result is False
            assert item.quantity == 60  # Unchanged


class TestSaleModel:
    """Tests for Sale model."""
    
    def test_create_sale(self, app, init_database):
        """Test sale creation."""
        with app.app_context():
            from app import db
            
            # Get the admin employee
            employee = Employee.query.filter_by(employee_id='100001').first()
            
            sale = Sale(
                transaction_id='TEST-SALE-001',
                employee_id=employee.id,
                tax_rate=0.06
            )
            db.session.add(sale)
            db.session.commit()
            
            assert sale.id is not None
            assert sale.transaction_id == 'TEST-SALE-001'
            assert sale.tax_rate == 0.06
    
    def test_calculate_totals(self, app, init_database):
        """Test sale total calculations."""
        with app.app_context():
            from app import db
            
            employee = Employee.query.filter_by(employee_id='100001').first()
            item = Item.query.filter_by(item_code='T001').first()
            
            sale = Sale(
                transaction_id='TEST-SALE-002',
                employee_id=employee.id,
                tax_rate=0.06
            )
            db.session.add(sale)
            db.session.commit()
            
            # Add items
            sale_item = SaleItem(
                sale_id=sale.id,
                item_id=item.id,
                quantity=2,
                unit_price=item.price
            )
            db.session.add(sale_item)
            db.session.commit()
            
            # Calculate totals
            sale.calculate_totals()
            
            expected_subtotal = 20.0  # 2 * 10.0
            expected_tax = 1.2  # 20.0 * 0.06
            expected_total = 21.2
            
            assert sale.subtotal == expected_subtotal
            assert abs(sale.tax_amount - expected_tax) < 0.01
            assert abs(sale.total - expected_total) < 0.01

