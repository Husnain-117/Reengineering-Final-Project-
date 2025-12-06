"""
Authentication Routes
======================
Handles login, logout, and authentication-related views.
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.services.auth_service import AuthService

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login."""
    # Redirect if already logged in
    if current_user.is_authenticated:
        if current_user.is_admin:
            return redirect(url_for('main.admin_dashboard'))
        return redirect(url_for('main.cashier_dashboard'))
    
    if request.method == 'POST':
        employee_id = request.form.get('employee_id', '').strip()
        password = request.form.get('password', '')
        
        if not employee_id or not password:
            flash('Please enter both employee ID and password.', 'error')
            return render_template('auth/login.html')
        
        success, employee, message = AuthService.authenticate(employee_id, password)
        
        if success:
            AuthService.login(employee)
            flash(f'Welcome, {employee.full_name}!', 'success')
            
            # Redirect based on role
            if employee.is_admin:
                return redirect(url_for('main.admin_dashboard'))
            return redirect(url_for('main.cashier_dashboard'))
        else:
            flash(message, 'error')
    
    return render_template('auth/login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    """Handle user logout."""
    AuthService.logout(current_user)
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))


@auth_bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    """Handle password change."""
    if request.method == 'POST':
        old_password = request.form.get('old_password', '')
        new_password = request.form.get('new_password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        if new_password != confirm_password:
            flash('New passwords do not match.', 'error')
            return render_template('auth/change_password.html')
        
        if len(new_password) < 4:
            flash('Password must be at least 4 characters.', 'error')
            return render_template('auth/change_password.html')
        
        success, message = AuthService.change_password(
            current_user, old_password, new_password
        )
        
        if success:
            flash(message, 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash(message, 'error')
    
    return render_template('auth/change_password.html')

