"""
Pytest Configuration and Fixtures
===================================
Provides shared fixtures for all tests.
"""

import pytest
from app import create_app, db
from app.models import Employee, Item


@pytest.fixture
def app():
    """Create application for testing."""
    app = create_app('testing')
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Create test CLI runner."""
    return app.test_cli_runner()


@pytest.fixture
def init_database(app):
    """Initialize database with test data."""
    with app.app_context():
        # Create test admin
        admin = Employee(
            employee_id='100001',
            first_name='Test',
            last_name='Admin',
            password='testpass',
            role='Admin'
        )
        db.session.add(admin)
        
        # Create test cashier
        cashier = Employee(
            employee_id='100002',
            first_name='Test',
            last_name='Cashier',
            password='testpass',
            role='Cashier'
        )
        db.session.add(cashier)
        
        # Create test items
        items = [
            Item(item_code='T001', name='Test Item 1', price=10.0, quantity=100),
            Item(item_code='T002', name='Test Item 2', price=25.5, quantity=50),
            Item(item_code='T003', name='Test Rental', price=15.0, quantity=20, is_rentable=True),
        ]
        for item in items:
            db.session.add(item)
        
        db.session.commit()
        
        yield
        
        db.session.rollback()


@pytest.fixture
def auth_client(client, init_database):
    """Create authenticated test client."""
    # Login as admin
    client.post('/login', data={
        'employee_id': '100001',
        'password': 'testpass'
    })
    return client

