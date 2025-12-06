"""
Integration Tests for Routes
==============================
Tests for web endpoints and views.
"""

import pytest


class TestAuthRoutes:
    """Tests for authentication routes."""
    
    def test_login_page(self, client):
        """Test login page loads."""
        response = client.get('/login')
        assert response.status_code == 200
        assert b'Login' in response.data
    
    def test_login_success(self, client, init_database):
        """Test successful login."""
        response = client.post('/login', data={
            'employee_id': '100001',
            'password': 'testpass'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert b'Dashboard' in response.data or b'Welcome' in response.data
    
    def test_login_failure(self, client, init_database):
        """Test failed login."""
        response = client.post('/login', data={
            'employee_id': '100001',
            'password': 'wrongpassword'
        }, follow_redirects=True)
        
        assert b'Invalid' in response.data or b'error' in response.data
    
    def test_logout(self, auth_client):
        """Test logout."""
        response = auth_client.get('/logout', follow_redirects=True)
        
        assert response.status_code == 200
        assert b'Login' in response.data


class TestMainRoutes:
    """Tests for main routes."""
    
    def test_index_redirect(self, client):
        """Test index redirects to login when not authenticated."""
        response = client.get('/', follow_redirects=True)
        assert b'Login' in response.data
    
    def test_dashboard_requires_auth(self, client):
        """Test dashboard requires authentication."""
        response = client.get('/dashboard')
        assert response.status_code == 302  # Redirect to login
    
    def test_admin_dashboard(self, auth_client):
        """Test admin dashboard access."""
        response = auth_client.get('/admin')
        assert response.status_code == 200
        assert b'Dashboard' in response.data


class TestInventoryRoutes:
    """Tests for inventory routes."""
    
    def test_inventory_list(self, auth_client):
        """Test inventory list page."""
        response = auth_client.get('/inventory/')
        assert response.status_code == 200
        assert b'Inventory' in response.data
    
    def test_inventory_search(self, auth_client):
        """Test inventory search."""
        response = auth_client.get('/inventory/?search=Test')
        assert response.status_code == 200
    
    def test_add_item_page(self, auth_client):
        """Test add item page loads."""
        response = auth_client.get('/inventory/add')
        assert response.status_code == 200
        assert b'Add' in response.data
    
    def test_add_item(self, auth_client):
        """Test adding new item."""
        response = auth_client.post('/inventory/add', data={
            'item_code': 'ROUTE001',
            'name': 'Route Test Item',
            'price': '15.99',
            'quantity': '50',
            'category': 'Test'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        # Should redirect to list with success message


class TestSalesRoutes:
    """Tests for sales routes."""
    
    def test_new_sale_page(self, auth_client):
        """Test new sale page loads."""
        response = auth_client.get('/sales/')
        assert response.status_code == 200
        assert b'Sale' in response.data or b'Cart' in response.data
    
    def test_start_sale(self, auth_client):
        """Test starting new sale."""
        response = auth_client.post('/sales/start')
        assert response.status_code == 200
        
        data = response.get_json()
        assert data['success'] is True
        assert 'sale' in data


class TestEmployeeRoutes:
    """Tests for employee management routes."""
    
    def test_employee_list(self, auth_client):
        """Test employee list page."""
        response = auth_client.get('/employees/')
        assert response.status_code == 200
        assert b'Employee' in response.data
    
    def test_add_employee_page(self, auth_client):
        """Test add employee page loads."""
        response = auth_client.get('/employees/add')
        assert response.status_code == 200
        assert b'Add' in response.data
    
    def test_add_employee(self, auth_client):
        """Test adding new employee."""
        response = auth_client.post('/employees/add', data={
            'first_name': 'New',
            'last_name': 'Employee',
            'password': 'newpass123',
            'confirm_password': 'newpass123',
            'role': 'Cashier'
        }, follow_redirects=True)
        
        assert response.status_code == 200


class TestAPIRoutes:
    """Tests for API endpoints."""
    
    def test_inventory_search_api(self, auth_client):
        """Test inventory search API."""
        response = auth_client.get('/inventory/api/search?q=Test')
        assert response.status_code == 200
        
        data = response.get_json()
        assert isinstance(data, list)
    
    def test_inventory_get_item_api(self, auth_client):
        """Test get item by code API."""
        response = auth_client.get('/inventory/api/T001')
        assert response.status_code == 200
        
        data = response.get_json()
        assert 'item_code' in data
    
    def test_inventory_get_invalid_item_api(self, auth_client):
        """Test get non-existent item API."""
        response = auth_client.get('/inventory/api/INVALID')
        assert response.status_code == 404

