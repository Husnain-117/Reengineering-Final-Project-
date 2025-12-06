"""
Rental Service
===============
Handles rental transaction operations.

Improvements over Legacy:
- Proper customer tracking
- Due date management
- Overdue detection
- Individual item return tracking
"""

import uuid
from datetime import datetime
from flask import current_app
from app import db
from app.models.item import Item
from app.models.rental import Rental, RentalItem
from app.models.activity_log import ActivityLog


class RentalService:
    """Service class for rental operations."""
    
    @staticmethod
    def generate_rental_id():
        """Generate unique rental ID."""
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        unique = str(uuid.uuid4())[:8].upper()
        return f"RENT-{timestamp}-{unique}"
    
    @staticmethod
    def create_rental(customer_phone, employee_id, customer_name=None, due_days=7):
        """
        Create a new rental transaction.
        
        Args:
            customer_phone: Customer's phone number
            employee_id: Processing employee's ID
            customer_name: Optional customer name
            due_days: Number of days until due
        
        Returns:
            Rental: New rental object
        """
        tax_rate = current_app.config.get('TAX_RATE', 0.06)
        
        rental = Rental(
            rental_id=RentalService.generate_rental_id(),
            customer_phone=customer_phone,
            employee_id=employee_id,
            due_days=due_days,
            tax_rate=tax_rate
        )
        rental.customer_name = customer_name
        
        db.session.add(rental)
        db.session.commit()
        
        return rental
    
    @staticmethod
    def add_item_to_rental(rental_id, item_code, quantity=1):
        """
        Add an item to a rental.
        
        Args:
            rental_id: Rental's primary key
            item_code: Item's business code
            quantity: Quantity to rent
        
        Returns:
            tuple: (success: bool, message: str, rental_item: RentalItem or None)
        """
        rental = Rental.query.get(rental_id)
        if not rental:
            return False, "Rental not found", None
        
        if rental.status not in ['active', 'in_progress']:
            rental.status = 'active'
        
        # Find item (must be rentable)
        item = Item.query.filter_by(item_code=item_code, is_active=True).first()
        if not item:
            return False, f"Item {item_code} not found", None
        
        if not item.is_rentable:
            return False, f"Item {item.name} is not available for rental", None
        
        # Check stock
        if item.quantity < quantity:
            return False, f"Insufficient stock. Available: {item.quantity}", None
        
        # Check if item already in rental
        existing = RentalItem.query.filter_by(
            rental_id=rental_id, 
            item_id=item.id,
            is_returned=False
        ).first()
        
        if existing:
            new_qty = existing.quantity + quantity
            if item.quantity < new_qty:
                return False, f"Insufficient stock for {new_qty} items", None
            existing.quantity = new_qty
            existing.line_total = new_qty * existing.unit_price
        else:
            rental_item = RentalItem(
                rental_id=rental_id,
                item_id=item.id,
                quantity=quantity,
                unit_price=item.price
            )
            db.session.add(rental_item)
        
        rental.calculate_totals()
        db.session.commit()
        
        return True, "Item added to rental", existing or rental_item
    
    @staticmethod
    def complete_rental(rental_id):
        """
        Complete a rental transaction (items go out).
        
        Args:
            rental_id: Rental's primary key
        
        Returns:
            tuple: (success: bool, message: str, rental: Rental or None)
        """
        rental = Rental.query.get(rental_id)
        if not rental:
            return False, "Rental not found", None
        
        # Update inventory for all items
        for rental_item in rental.items:
            item = rental_item.item
            if item.quantity < rental_item.quantity:
                return False, f"Insufficient stock for {item.name}", None
            
            item.update_quantity(rental_item.quantity, 'subtract')
        
        rental.calculate_totals()
        rental.status = 'active'
        
        ActivityLog.log(
            action=ActivityLog.ACTION_RENTAL,
            employee_id=rental.employee_id,
            entity_type='rental',
            entity_id=rental.id,
            description=f"Created rental {rental.rental_id} for {rental.customer_phone}"
        )
        
        db.session.commit()
        return True, "Rental completed successfully", rental
    
    @staticmethod
    def process_return(rental_id, item_ids=None):
        """
        Process return for a rental.
        
        Args:
            rental_id: Rental's primary key
            item_ids: List of item IDs to return (None for all)
        
        Returns:
            tuple: (success: bool, message: str)
        """
        rental = Rental.query.get(rental_id)
        if not rental:
            return False, "Rental not found"
        
        if rental.status == 'returned':
            return False, "Rental already returned"
        
        # Get items to return
        items_to_return = rental.items
        if item_ids:
            items_to_return = [i for i in rental.items if i.item_id in item_ids]
        
        # Return items to inventory
        for rental_item in items_to_return:
            if not rental_item.is_returned:
                rental_item.item.update_quantity(rental_item.quantity, 'add')
                rental_item.mark_returned()
        
        # Update rental status
        rental.process_return()
        
        ActivityLog.log(
            action=ActivityLog.ACTION_RETURN,
            employee_id=rental.employee_id,
            entity_type='rental',
            entity_id=rental.id,
            description=f"Processed return for rental {rental.rental_id}"
        )
        
        db.session.commit()
        return True, f"Return processed. Status: {rental.status}"
    
    @staticmethod
    def get_rental(rental_id):
        """Get rental by ID."""
        return Rental.query.get(rental_id)
    
    @staticmethod
    def get_rentals_by_phone(phone):
        """Get all rentals for a customer phone."""
        return Rental.query.filter_by(customer_phone=phone)\
            .order_by(Rental.created_at.desc()).all()
    
    @staticmethod
    def get_active_rentals():
        """Get all active (not returned) rentals."""
        return Rental.query.filter(
            Rental.status.in_(['active', 'overdue'])
        ).order_by(Rental.due_date).all()
    
    @staticmethod
    def get_overdue_rentals():
        """Get all overdue rentals."""
        now = datetime.utcnow()
        return Rental.query.filter(
            Rental.status != 'returned',
            Rental.due_date < now
        ).order_by(Rental.due_date).all()
    
    @staticmethod
    def update_overdue_status():
        """Update status for overdue rentals."""
        now = datetime.utcnow()
        overdue_rentals = Rental.query.filter(
            Rental.status == 'active',
            Rental.due_date < now
        ).all()
        
        for rental in overdue_rentals:
            rental.status = 'overdue'
        
        db.session.commit()
        return len(overdue_rentals)

