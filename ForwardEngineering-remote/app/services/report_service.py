"""
Report Service
===============
Handles report generation and analytics.

New Feature (not in Legacy):
- Sales reports by date range
- Employee performance metrics
- Inventory status reports
- Rental analytics
"""

from datetime import datetime, timedelta
from sqlalchemy import func
from app import db
from app.models.employee import Employee
from app.models.item import Item
from app.models.sale import Sale, SaleItem
from app.models.rental import Rental
from app.models.activity_log import ActivityLog


class ReportService:
    """Service class for report generation."""
    
    @staticmethod
    def get_daily_sales_summary(date=None):
        """
        Get sales summary for a specific date.
        
        Args:
            date: Date to report on (default: today)
        
        Returns:
            dict: Sales summary data
        """
        if date is None:
            date = datetime.utcnow().date()
        
        start_datetime = datetime.combine(date, datetime.min.time())
        end_datetime = datetime.combine(date, datetime.max.time())
        
        sales = Sale.query.filter(
            Sale.status == 'completed',
            Sale.created_at >= start_datetime,
            Sale.created_at <= end_datetime
        ).all()
        
        total_sales = len(sales)
        total_revenue = sum(sale.total for sale in sales)
        total_tax = sum(sale.tax_amount for sale in sales)
        
        return {
            'date': date.isoformat(),
            'total_transactions': total_sales,
            'total_revenue': round(total_revenue, 2),
            'total_tax': round(total_tax, 2),
            'average_transaction': round(total_revenue / total_sales, 2) if total_sales > 0 else 0
        }
    
    @staticmethod
    def get_sales_report(start_date, end_date=None):
        """
        Get sales report for date range.
        
        Args:
            start_date: Start date
            end_date: End date (default: same as start)
        
        Returns:
            dict: Sales report data
        """
        if end_date is None:
            end_date = start_date
        
        start_datetime = datetime.combine(start_date, datetime.min.time())
        end_datetime = datetime.combine(end_date, datetime.max.time())
        
        sales = Sale.query.filter(
            Sale.status == 'completed',
            Sale.created_at >= start_datetime,
            Sale.created_at <= end_datetime
        ).order_by(Sale.created_at).all()
        
        # Group by day
        daily_totals = {}
        for sale in sales:
            day = sale.created_at.date().isoformat()
            if day not in daily_totals:
                daily_totals[day] = {'count': 0, 'revenue': 0}
            daily_totals[day]['count'] += 1
            daily_totals[day]['revenue'] += sale.total
        
        return {
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat(),
            'total_transactions': len(sales),
            'total_revenue': round(sum(s.total for s in sales), 2),
            'daily_breakdown': daily_totals,
            'transactions': [s.to_dict() for s in sales]
        }
    
    @staticmethod
    def get_top_selling_items(limit=10, days=30):
        """
        Get top selling items.
        
        Args:
            limit: Number of items to return
            days: Days to look back
        
        Returns:
            list: Top selling items with quantities
        """
        start_date = datetime.utcnow() - timedelta(days=days)
        
        results = db.session.query(
            Item.id,
            Item.item_code,
            Item.name,
            func.sum(SaleItem.quantity).label('total_quantity'),
            func.sum(SaleItem.line_total).label('total_revenue')
        ).join(SaleItem).join(Sale).filter(
            Sale.status == 'completed',
            Sale.created_at >= start_date
        ).group_by(Item.id).order_by(
            func.sum(SaleItem.quantity).desc()
        ).limit(limit).all()
        
        return [{
            'item_id': r[0],
            'item_code': r[1],
            'name': r[2],
            'total_quantity': r[3],
            'total_revenue': round(r[4], 2)
        } for r in results]
    
    @staticmethod
    def get_employee_performance(employee_id=None, days=30):
        """
        Get employee performance metrics.
        
        Args:
            employee_id: Specific employee (None for all)
            days: Days to analyze
        
        Returns:
            dict or list: Performance metrics
        """
        start_date = datetime.utcnow() - timedelta(days=days)
        
        query = db.session.query(
            Employee.id,
            Employee.employee_id,
            Employee.first_name,
            Employee.last_name,
            func.count(Sale.id).label('total_sales'),
            func.sum(Sale.total).label('total_revenue')
        ).outerjoin(Sale, (Sale.employee_id == Employee.id) & (Sale.status == 'completed') & (Sale.created_at >= start_date)
        ).filter(Employee.is_active == True)
        
        if employee_id:
            query = query.filter(Employee.id == employee_id)
        
        results = query.group_by(Employee.id).all()
        
        return [{
            'employee_id': r[0],
            'employee_code': r[1],
            'name': f"{r[2]} {r[3]}",
            'total_sales': r[4] or 0,
            'total_revenue': round(r[5] or 0, 2)
        } for r in results]
    
    @staticmethod
    def get_inventory_status():
        """
        Get inventory status report.
        
        Returns:
            dict: Inventory status summary
        """
        total_items = Item.query.filter_by(is_active=True).count()
        
        low_stock_items = Item.query.filter(
            Item.is_active == True,
            Item.quantity <= Item.min_stock_level,
            Item.quantity > 0
        ).all()
        
        out_of_stock = Item.query.filter(
            Item.is_active == True,
            Item.quantity <= 0
        ).all()
        
        total_value = db.session.query(
            func.sum(Item.price * Item.quantity)
        ).filter(Item.is_active == True).scalar() or 0
        
        return {
            'total_items': total_items,
            'low_stock_count': len(low_stock_items),
            'out_of_stock_count': len(out_of_stock),
            'total_inventory_value': round(total_value, 2),
            'low_stock_items': [i.to_dict() for i in low_stock_items],
            'out_of_stock_items': [i.to_dict() for i in out_of_stock]
        }
    
    @staticmethod
    def get_rental_status():
        """
        Get rental status report.
        
        Returns:
            dict: Rental status summary
        """
        active_rentals = Rental.query.filter_by(status='active').count()
        overdue_rentals = Rental.query.filter_by(status='overdue').count()
        
        overdue_list = Rental.query.filter_by(status='overdue').all()
        
        return {
            'active_rentals': active_rentals,
            'overdue_rentals': overdue_rentals,
            'overdue_list': [r.to_dict() for r in overdue_list]
        }
    
    @staticmethod
    def get_activity_log(days=7, action=None, limit=100):
        """
        Get activity log entries.
        
        Args:
            days: Days to look back
            action: Filter by action type
            limit: Maximum entries to return
        
        Returns:
            list: Activity log entries
        """
        start_date = datetime.utcnow() - timedelta(days=days)
        
        query = ActivityLog.query.filter(ActivityLog.created_at >= start_date)
        
        if action:
            query = query.filter_by(action=action)
        
        logs = query.order_by(ActivityLog.created_at.desc()).limit(limit).all()
        
        return [log.to_dict() for log in logs]

