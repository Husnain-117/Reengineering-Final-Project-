"""
Reports Routes
===============
Handles report viewing (Admin only).
"""

from datetime import datetime, timedelta
from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from app.services.report_service import ReportService

reports_bp = Blueprint('reports', __name__)


def admin_required(f):
    """Decorator to require admin access."""
    from functools import wraps
    from flask import redirect, url_for, flash
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            flash('Access denied. Admin privileges required.', 'error')
            return redirect(url_for('main.dashboard'))
        return f(*args, **kwargs)
    return decorated_function


@reports_bp.route('/')
@login_required
@admin_required
def reports_dashboard():
    """Reports dashboard."""
    from app.models.sale import Sale
    from app.models.item import Item
    from app.models.employee import Employee
    from app.models.rental import Rental
    from app.models.activity_log import ActivityLog
    
    # Get counts
    sales_count = Sale.query.count()
    items_count = Item.query.filter_by(is_active=True).count()
    employees_count = Employee.query.filter_by(is_active=True).count()
    rentals_count = Rental.query.count()
    overdue_count = Rental.query.filter_by(status='overdue').count()
    
    # Calculate total revenue
    from sqlalchemy import func
    from app import db
    total_revenue = db.session.query(func.sum(Sale.total)).filter(Sale.status == 'completed').scalar() or 0
    
    # Low stock items
    low_stock_count = Item.query.filter(Item.quantity <= Item.min_stock_level, Item.is_active == True).count()
    
    # Recent activity (last 24 hours)
    from datetime import datetime, timedelta
    yesterday = datetime.utcnow() - timedelta(hours=24)
    activities_count = ActivityLog.query.filter(ActivityLog.created_at >= yesterday).count()
    recent_activities = ActivityLog.query.filter(ActivityLog.created_at >= yesterday).order_by(ActivityLog.created_at.desc()).limit(10).all()
    
    return render_template('reports/dashboard.html',
                         sales_count=sales_count,
                         total_revenue=total_revenue,
                         items_count=items_count,
                         low_stock_count=low_stock_count,
                         employees_count=employees_count,
                         activities_count=activities_count,
                         rentals_count=rentals_count,
                         overdue_count=overdue_count,
                         recent_activities=recent_activities)


@reports_bp.route('/sales')
@login_required
@admin_required
def sales_report():
    """Sales report with date filtering."""
    # Default to last 7 days
    end_date = datetime.utcnow().date()
    start_date = end_date - timedelta(days=7)
    
    # Parse date parameters
    start_str = request.args.get('start_date')
    end_str = request.args.get('end_date')
    
    if start_str:
        try:
            start_date = datetime.strptime(start_str, '%Y-%m-%d').date()
        except ValueError:
            pass
    
    if end_str:
        try:
            end_date = datetime.strptime(end_str, '%Y-%m-%d').date()
        except ValueError:
            pass
    
    report = ReportService.get_sales_report(start_date, end_date)
    
    return render_template('reports/sales.html',
                         report=report,
                         start_date=start_date,
                         end_date=end_date)


@reports_bp.route('/top-items')
@login_required
@admin_required
def top_items():
    """Top selling items report."""
    days = request.args.get('days', 30, type=int)
    limit = request.args.get('limit', 20, type=int)
    
    items = ReportService.get_top_selling_items(limit=limit, days=days)
    
    return render_template('reports/top_items.html',
                         items=items,
                         days=days)


@reports_bp.route('/employees')
@login_required
@admin_required
def employee_report():
    """Employee performance report."""
    from app.models.employee import Employee
    from app.models.sale import Sale
    from app.models.activity_log import ActivityLog
    from sqlalchemy import func
    from app import db
    
    days = request.args.get('days', 30, type=int)
    
    # Get all employees with their stats
    employees = Employee.query.filter_by(is_active=True).all()
    
    employee_stats = []
    for emp in employees:
        # Count sales for this employee
        sales_count = Sale.query.filter_by(employee_id=emp.id, status='completed').count()
        
        # Sum revenue for this employee
        revenue = db.session.query(func.sum(Sale.total)).filter(
            Sale.employee_id == emp.id, 
            Sale.status == 'completed'
        ).scalar() or 0
        
        # Recent activity count
        activity_count = ActivityLog.query.filter_by(employee_id=emp.id).count()
        
        employee_stats.append({
            'employee': emp,
            'sales_count': sales_count,
            'total_revenue': revenue,
            'activity_count': activity_count
        })
    
    return render_template('reports/employees.html',
                         employee_stats=employee_stats,
                         days=days)


@reports_bp.route('/inventory')
@login_required
@admin_required
def inventory_report():
    """Inventory status report."""
    status = ReportService.get_inventory_status()
    
    return render_template('reports/inventory.html', status=status)


@reports_bp.route('/rentals')
@login_required
@admin_required
def rental_report():
    """Rental status report."""
    status = ReportService.get_rental_status()
    
    return render_template('reports/rentals.html', status=status)


@reports_bp.route('/activity')
@login_required
@admin_required
def activity_log():
    """Activity log report."""
    days = request.args.get('days', 7, type=int)
    action = request.args.get('action', '')
    
    logs = ReportService.get_activity_log(days=days, action=action if action else None)
    
    return render_template('reports/activity.html',
                         logs=logs,
                         days=days,
                         action=action)


# API endpoints for charts/dashboards
@reports_bp.route('/api/daily-summary')
@login_required
def api_daily_summary():
    """API endpoint for daily summary."""
    summary = ReportService.get_daily_sales_summary()
    return jsonify(summary)


@reports_bp.route('/api/inventory-status')
@login_required
def api_inventory_status():
    """API endpoint for inventory status."""
    status = ReportService.get_inventory_status()
    return jsonify(status)

