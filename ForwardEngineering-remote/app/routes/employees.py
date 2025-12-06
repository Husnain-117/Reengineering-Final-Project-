"""
Employee Management Routes
===========================
Handles employee CRUD operations (Admin only).
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.services.employee_service import EmployeeService

employees_bp = Blueprint('employees', __name__)


def admin_required(f):
    """Decorator to require admin access."""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            flash('Access denied. Admin privileges required.', 'error')
            return redirect(url_for('main.dashboard'))
        return f(*args, **kwargs)
    return decorated_function


@employees_bp.route('/')
@login_required
@admin_required
def list_employees():
    """List all employees."""
    employees = EmployeeService.get_all_employees()
    return render_template('employees/list.html', employees=employees)


@employees_bp.route('/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_employee():
    """Add new employee."""
    if request.method == 'POST':
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        role = request.form.get('role', 'Cashier')
        
        # Validation
        if not first_name or not last_name:
            flash('First and last name are required.', 'error')
            return render_template('employees/add.html')
        
        if not password or len(password) < 4:
            flash('Password must be at least 4 characters.', 'error')
            return render_template('employees/add.html')
        
        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return render_template('employees/add.html')
        
        success, employee, message = EmployeeService.create_employee(
            first_name=first_name,
            last_name=last_name,
            password=password,
            role=role,
            admin_id=current_user.id
        )
        
        if success:
            flash(message, 'success')
            return redirect(url_for('employees.list_employees'))
        else:
            flash(message, 'error')
    
    return render_template('employees/add.html')


@employees_bp.route('/<int:employee_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_employee(employee_id):
    """Edit employee."""
    employee = EmployeeService.get_employee_by_id(employee_id)
    if not employee:
        flash('Employee not found.', 'error')
        return redirect(url_for('employees.list_employees'))
    
    if request.method == 'POST':
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        password = request.form.get('password', '')
        role = request.form.get('role', employee.role)
        
        update_data = {
            'first_name': first_name,
            'last_name': last_name,
            'role': role
        }
        
        if password:
            if len(password) < 4:
                flash('Password must be at least 4 characters.', 'error')
                return render_template('employees/edit.html', employee=employee)
            update_data['password'] = password
        
        success, employee, message = EmployeeService.update_employee(
            employee_id,
            admin_id=current_user.id,
            **update_data
        )
        
        if success:
            flash(message, 'success')
            return redirect(url_for('employees.list_employees'))
        else:
            flash(message, 'error')
    
    return render_template('employees/edit.html', employee=employee)


@employees_bp.route('/<int:employee_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_employee(employee_id):
    """Delete employee."""
    success, message = EmployeeService.delete_employee(employee_id, current_user.id)
    
    if success:
        flash(message, 'success')
    else:
        flash(message, 'error')
    
    return redirect(url_for('employees.list_employees'))

