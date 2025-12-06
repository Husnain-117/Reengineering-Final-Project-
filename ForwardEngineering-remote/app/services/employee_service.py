"""
Employee Service
=================
Handles employee management operations.

Improvements over Legacy:
- Secure password handling
- Input validation
- Audit logging
- Soft delete support
"""

from app import db
from app.models.employee import Employee
from app.models.activity_log import ActivityLog


class EmployeeService:
    """Service class for employee management operations."""
    
    @staticmethod
    def generate_employee_id():
        """Generate next employee ID."""
        last_employee = Employee.query.order_by(Employee.employee_id.desc()).first()
        if last_employee:
            try:
                last_id = int(last_employee.employee_id)
                return str(last_id + 1)
            except ValueError:
                pass
        return "110001"  # Starting ID like legacy system
    
    @staticmethod
    def get_all_employees(include_inactive=False):
        """Get all employees."""
        query = Employee.query
        if not include_inactive:
            query = query.filter_by(is_active=True)
        return query.order_by(Employee.employee_id).all()
    
    @staticmethod
    def get_employee_by_id(employee_id):
        """Get employee by primary key."""
        return Employee.query.get(employee_id)
    
    @staticmethod
    def get_employee_by_code(employee_code):
        """Get employee by business ID (e.g., '110001')."""
        return Employee.query.filter_by(
            employee_id=employee_code,
            is_active=True
        ).first()
    
    @staticmethod
    def create_employee(first_name, last_name, password, role='Cashier', 
                       admin_id=None):
        """
        Create a new employee.
        
        Args:
            first_name: Employee's first name
            last_name: Employee's last name
            password: Initial password
            role: 'Admin' or 'Cashier'
            admin_id: ID of admin creating the employee
        
        Returns:
            tuple: (success: bool, employee: Employee or None, message: str)
        """
        # Validate role
        if role not in ['Admin', 'Cashier']:
            return False, None, "Invalid role. Must be 'Admin' or 'Cashier'"
        
        # Generate employee ID
        employee_id = EmployeeService.generate_employee_id()
        
        employee = Employee(
            employee_id=employee_id,
            first_name=first_name,
            last_name=last_name,
            password=password,
            role=role
        )
        
        db.session.add(employee)
        db.session.commit()
        
        # Log activity
        if admin_id:
            ActivityLog.log(
                action=ActivityLog.ACTION_EMPLOYEE_CREATE,
                employee_id=admin_id,
                entity_type='employee',
                entity_id=employee.id,
                description=f"Created employee: {employee.full_name} ({role})"
            )
        
        return True, employee, f"Employee created with ID: {employee_id}"
    
    @staticmethod
    def update_employee(employee_pk, admin_id=None, **kwargs):
        """
        Update an employee.
        
        Args:
            employee_pk: Employee's primary key
            admin_id: ID of admin making the update
            **kwargs: Fields to update
        
        Returns:
            tuple: (success: bool, employee: Employee or None, message: str)
        """
        employee = Employee.query.get(employee_pk)
        if not employee:
            return False, None, "Employee not found"
        
        # Update allowed fields
        if 'first_name' in kwargs:
            employee.first_name = kwargs['first_name']
        if 'last_name' in kwargs:
            employee.last_name = kwargs['last_name']
        if 'role' in kwargs:
            if kwargs['role'] not in ['Admin', 'Cashier']:
                return False, None, "Invalid role"
            employee.role = kwargs['role']
        if 'password' in kwargs and kwargs['password']:
            employee.set_password(kwargs['password'])
        
        db.session.commit()
        
        # Log activity
        if admin_id:
            ActivityLog.log(
                action=ActivityLog.ACTION_EMPLOYEE_UPDATE,
                employee_id=admin_id,
                entity_type='employee',
                entity_id=employee.id,
                description=f"Updated employee: {employee.full_name}"
            )
        
        return True, employee, "Employee updated successfully"
    
    @staticmethod
    def delete_employee(employee_pk, admin_id=None):
        """
        Soft delete an employee.
        
        Args:
            employee_pk: Employee's primary key
            admin_id: ID of admin deleting
        
        Returns:
            tuple: (success: bool, message: str)
        """
        employee = Employee.query.get(employee_pk)
        if not employee:
            return False, "Employee not found"
        
        # Prevent self-deletion
        if admin_id and employee.id == admin_id:
            return False, "Cannot delete your own account"
        
        employee.is_active = False
        db.session.commit()
        
        # Log activity
        if admin_id:
            ActivityLog.log(
                action=ActivityLog.ACTION_EMPLOYEE_DELETE,
                employee_id=admin_id,
                entity_type='employee',
                entity_id=employee.id,
                description=f"Deleted employee: {employee.full_name}"
            )
        
        return True, "Employee deleted successfully"
    
    @staticmethod
    def get_employees_by_role(role):
        """Get employees by role."""
        return Employee.query.filter_by(
            role=role,
            is_active=True
        ).order_by(Employee.last_name).all()

