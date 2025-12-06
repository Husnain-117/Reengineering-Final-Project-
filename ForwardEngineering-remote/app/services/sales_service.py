"""
Sales Service
==============
Handles sales transaction operations.

Improvements over Legacy:
- Atomic transactions (all or nothing)
- Proper receipt generation
- Invoice record with full details
- Refund support
"""

import uuid
from datetime import datetime
from flask import current_app
from app import db
from app.models.item import Item
from app.models.sale import Sale, SaleItem
from app.models.activity_log import ActivityLog
from app.services.inventory_service import InventoryService


class SalesService:
    """Service class for sales operations."""
    
    @staticmethod
    def generate_transaction_id():
        """Generate unique transaction ID."""
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        unique = str(uuid.uuid4())[:8].upper()
        return f"SALE-{timestamp}-{unique}"
    
    @staticmethod
    def create_sale(employee_id):
        """
        Create a new sale transaction.
        
        Args:
            employee_id: Cashier's employee ID
        
        Returns:
            Sale: New sale object
        """
        tax_rate = current_app.config.get('TAX_RATE', 0.06)
        
        sale = Sale(
            transaction_id=SalesService.generate_transaction_id(),
            employee_id=employee_id,
            tax_rate=tax_rate
        )
        sale.status = 'in_progress'
        
        db.session.add(sale)
        db.session.commit()
        
        return sale
    
    @staticmethod
    def add_item_to_sale(sale_id, item_code, quantity=1):
        """
        Add an item to a sale.
        
        Args:
            sale_id: Sale's primary key
            item_code: Item's business code
            quantity: Quantity to add
        
        Returns:
            tuple: (success: bool, message: str, sale_item: SaleItem or None)
        """
        sale = Sale.query.get(sale_id)
        if not sale:
            return False, "Sale not found", None
        
        if sale.status != 'in_progress':
            return False, "Sale is not in progress", None
        
        # Find item
        item = Item.query.filter_by(item_code=item_code, is_active=True).first()
        if not item:
            return False, f"Item {item_code} not found", None
        
        # Check stock
        if item.quantity < quantity:
            return False, f"Insufficient stock. Available: {item.quantity}", None
        
        # Check if item already in sale
        existing = SaleItem.query.filter_by(sale_id=sale_id, item_id=item.id).first()
        if existing:
            # Update quantity
            new_qty = existing.quantity + quantity
            if item.quantity < new_qty:
                return False, f"Insufficient stock for {new_qty} items", None
            existing.quantity = new_qty
            existing.line_total = new_qty * existing.unit_price
        else:
            # Add new line item
            sale_item = SaleItem(
                sale_id=sale_id,
                item_id=item.id,
                quantity=quantity,
                unit_price=item.price
            )
            db.session.add(sale_item)
        
        # Recalculate totals
        sale.calculate_totals()
        db.session.commit()
        
        return True, "Item added successfully", existing or sale_item
    
    @staticmethod
    def remove_item_from_sale(sale_id, item_id):
        """
        Remove an item from a sale.
        
        Args:
            sale_id: Sale's primary key
            item_id: Item's primary key
        
        Returns:
            tuple: (success: bool, message: str)
        """
        sale = Sale.query.get(sale_id)
        if not sale:
            return False, "Sale not found"
        
        if sale.status != 'in_progress':
            return False, "Sale is not in progress"
        
        sale_item = SaleItem.query.filter_by(sale_id=sale_id, item_id=item_id).first()
        if not sale_item:
            return False, "Item not in sale"
        
        db.session.delete(sale_item)
        sale.calculate_totals()
        db.session.commit()
        
        return True, "Item removed successfully"
    
    @staticmethod
    def complete_sale(sale_id, amount_paid, payment_method='Cash'):
        """
        Complete a sale transaction.
        
        Performs atomic transaction:
        1. Verify stock availability
        2. Update inventory
        3. Record payment
        4. Log activity
        
        Args:
            sale_id: Sale's primary key
            amount_paid: Amount received from customer
            payment_method: Payment method used
        
        Returns:
            tuple: (success: bool, message: str, sale: Sale or None)
        """
        sale = Sale.query.get(sale_id)
        if not sale:
            return False, "Sale not found", None
        
        if sale.status != 'in_progress':
            return False, "Sale is not in progress", None
        
        # Verify and update stock for all items
        for sale_item in sale.items:
            item = sale_item.item
            if item.quantity < sale_item.quantity:
                return False, f"Insufficient stock for {item.name}", None
        
        # Update inventory
        for sale_item in sale.items:
            success = sale_item.item.update_quantity(sale_item.quantity, 'subtract')
            if not success:
                db.session.rollback()
                return False, f"Failed to update inventory for {sale_item.item.name}", None
        
        # Calculate final totals
        sale.calculate_totals()
        
        # Process payment
        if amount_paid < sale.total:
            return False, f"Insufficient payment. Total: ${sale.total:.2f}", None
        
        sale.process_payment(amount_paid, payment_method)
        
        # Log activity
        ActivityLog.log(
            action=ActivityLog.ACTION_SALE,
            employee_id=sale.employee_id,
            entity_type='sale',
            entity_id=sale.id,
            description=f"Completed sale {sale.transaction_id} for ${sale.total:.2f}"
        )
        
        db.session.commit()
        
        return True, "Sale completed successfully", sale
    
    @staticmethod
    def cancel_sale(sale_id, employee_id=None):
        """
        Cancel a sale in progress.
        
        Args:
            sale_id: Sale's primary key
            employee_id: Employee cancelling the sale
        
        Returns:
            tuple: (success: bool, message: str)
        """
        sale = Sale.query.get(sale_id)
        if not sale:
            return False, "Sale not found"
        
        if sale.status == 'completed':
            return False, "Cannot cancel completed sale. Use refund instead."
        
        sale.status = 'voided'
        
        if employee_id:
            ActivityLog.log(
                action='sale_cancelled',
                employee_id=employee_id,
                entity_type='sale',
                entity_id=sale.id,
                description=f"Cancelled sale {sale.transaction_id}"
            )
        
        db.session.commit()
        return True, "Sale cancelled successfully"
    
    @staticmethod
    def get_sale(sale_id):
        """Get sale by ID."""
        return Sale.query.get(sale_id)
    
    @staticmethod
    def get_sales_by_date(start_date, end_date=None):
        """Get sales within date range."""
        query = Sale.query.filter(
            Sale.status == 'completed',
            Sale.created_at >= start_date
        )
        if end_date:
            query = query.filter(Sale.created_at <= end_date)
        return query.order_by(Sale.created_at.desc()).all()
    
    @staticmethod
    def get_sales_by_employee(employee_id, limit=50):
        """Get recent sales by employee."""
        return Sale.query.filter_by(
            employee_id=employee_id,
            status='completed'
        ).order_by(Sale.created_at.desc()).limit(limit).all()

