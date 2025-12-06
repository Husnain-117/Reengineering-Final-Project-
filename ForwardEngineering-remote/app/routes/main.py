"""
Main Routes
============
Handles main navigation and dashboard views.
"""

from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from app.services.report_service import ReportService
from app.services.inventory_service import InventoryService
from app.services.rental_service import RentalService

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """Redirect to login or dashboard."""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return redirect(url_for('auth.login'))


@main_bp.route('/dashboard')
@login_required
def dashboard():
    """Redirect to appropriate dashboard based on role."""
    if current_user.is_admin:
        return redirect(url_for('main.admin_dashboard'))
    return redirect(url_for('main.cashier_dashboard'))


@main_bp.route('/admin')
@login_required
def admin_dashboard():
    """Admin dashboard with overview statistics."""
    if not current_user.is_admin:
        return redirect(url_for('main.cashier_dashboard'))
    
    # Get dashboard data
    daily_summary = ReportService.get_daily_sales_summary()
    inventory_status = ReportService.get_inventory_status()
    rental_status = ReportService.get_rental_status()
    recent_activity = ReportService.get_activity_log(days=1, limit=10)
    
    return render_template('main/admin_dashboard.html',
                         daily_summary=daily_summary,
                         inventory_status=inventory_status,
                         rental_status=rental_status,
                         recent_activity=recent_activity)


@main_bp.route('/cashier')
@login_required
def cashier_dashboard():
    """Cashier dashboard for POS operations."""
    # Get low stock alerts
    low_stock = InventoryService.get_low_stock_items()
    
    return render_template('main/cashier_dashboard.html',
                         low_stock_count=len(low_stock))

