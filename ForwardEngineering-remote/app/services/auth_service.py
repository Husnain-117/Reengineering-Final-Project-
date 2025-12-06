"""
Authentication Service
=======================
Handles user authentication and authorization.

Improvements over Legacy:
- Secure password verification (vs plain text comparison)
- Session-based authentication
- Activity logging for audit
- Role-based access control
"""

from flask import request
from flask_login import login_user, logout_user
from app import db
from app.models.employee import Employee
from app.models.activity_log import ActivityLog


class AuthService:
    """Service class for authentication operations."""
    
    @staticmethod
    def authenticate(employee_id, password):
        """
        Authenticate an employee.
        
        Args:
            employee_id: Employee's business ID (e.g., '110001')
            password: Plain text password to verify
        
        Returns:
            tuple: (success: bool, employee: Employee or None, message: str)
        """
        # Find employee by business ID
        employee = Employee.query.filter_by(
            employee_id=employee_id,
            is_active=True
        ).first()
        
        if not employee:
            return False, None, "Invalid credentials"
        
        # Verify password
        if not employee.check_password(password):
            return False, None, "Invalid credentials"
        
        # Log successful login
        ActivityLog.log(
            action=ActivityLog.ACTION_LOGIN,
            employee_id=employee.id,
            description=f"{employee.full_name} logged in",
            ip_address=request.remote_addr if request else None
        )
        
        return True, employee, "Login successful"
    
    @staticmethod
    def login(employee):
        """
        Log in an employee (create session).
        
        Args:
            employee: Employee object to log in
        
        Returns:
            bool: Success status
        """
        return login_user(employee, remember=True)
    
    @staticmethod
    def logout(employee):
        """
        Log out an employee (end session).
        
        Args:
            employee: Employee object to log out
        """
        if employee:
            # Log logout activity
            ActivityLog.log(
                action=ActivityLog.ACTION_LOGOUT,
                employee_id=employee.id,
                description=f"{employee.full_name} logged out",
                ip_address=request.remote_addr if request else None
            )
        
        logout_user()
    
    @staticmethod
    def is_admin(employee):
        """
        Check if employee has admin privileges.
        
        Args:
            employee: Employee object to check
        
        Returns:
            bool: True if admin, False otherwise
        """
        return employee and employee.is_admin
    
    @staticmethod
    def change_password(employee, old_password, new_password):
        """
        Change employee password.
        
        Args:
            employee: Employee object
            old_password: Current password for verification
            new_password: New password to set
        
        Returns:
            tuple: (success: bool, message: str)
        """
        if not employee.check_password(old_password):
            return False, "Current password is incorrect"
        
        employee.set_password(new_password)
        db.session.commit()
        
        # Log password change
        ActivityLog.log(
            action='password_change',
            employee_id=employee.id,
            description=f"{employee.full_name} changed password",
            ip_address=request.remote_addr if request else None
        )
        
        return True, "Password changed successfully"

