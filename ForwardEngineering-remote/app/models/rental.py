"""
Rental and RentalItem Models
=============================
Represents rental transactions with proper normalization.

Legacy System Issues Addressed:
- Complex inline format in userDatabase.txt → Normalized tables
- Phone number as identifier → Proper customer tracking
- Boolean return status only → Full rental lifecycle
- No due dates → Due date tracking added
- Data redundancy → Eliminated through normalization

Database Design:
- Rental (header) + RentalItem (details) pattern
- Proper status tracking (active, returned, overdue)
- Foreign key relationships
"""

from datetime import datetime, timedelta
from app import db


class Rental(db.Model):
    """
    Rental transaction model.
    
    Represents a rental transaction header.
    Individual rented items tracked in RentalItem.
    
    Attributes:
        id: Primary key
        rental_id: Business rental identifier
        customer_phone: Customer phone number
        customer_name: Optional customer name
        employee_id: Foreign key to processing employee
        subtotal: Pre-tax rental total
        tax_amount: Calculated tax
        total: Final rental total
        status: active, returned, overdue, partial_return
        rental_date: When rental started
        due_date: When items should be returned
        return_date: Actual return date
    """
    
    __tablename__ = 'rentals'
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True)
    
    # Rental identifier
    rental_id = db.Column(db.String(50), unique=True, nullable=False, index=True)
    
    # Customer information (was just phone in legacy)
    customer_phone = db.Column(db.String(20), nullable=False, index=True)
    customer_name = db.Column(db.String(100), nullable=True)
    
    # Foreign key to Employee
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    
    # Financial details
    subtotal = db.Column(db.Float, nullable=False, default=0.0)
    tax_rate = db.Column(db.Float, nullable=False, default=0.06)
    tax_amount = db.Column(db.Float, nullable=False, default=0.0)
    total = db.Column(db.Float, nullable=False, default=0.0)
    deposit = db.Column(db.Float, default=0.0)
    
    # Rental dates
    rental_date = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.DateTime, nullable=True)
    return_date = db.Column(db.DateTime, nullable=True)
    
    # Status: active, returned, overdue, partial_return
    status = db.Column(db.String(20), default='active')
    
    # Notes
    notes = db.Column(db.Text, nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    items = db.relationship('RentalItem', backref='rental', lazy='dynamic', cascade='all, delete-orphan')
    
    def __init__(self, rental_id, customer_phone, employee_id, due_days=7, tax_rate=0.06):
        """Initialize rental transaction."""
        self.rental_id = rental_id
        self.customer_phone = customer_phone
        self.employee_id = employee_id
        self.tax_rate = tax_rate
        self.rental_date = datetime.utcnow()
        self.due_date = self.rental_date + timedelta(days=due_days)
    
    @property
    def is_overdue(self):
        """Check if rental is overdue."""
        if self.status == 'returned':
            return False
        return datetime.utcnow() > self.due_date if self.due_date else False
    
    def calculate_totals(self):
        """Calculate subtotal, tax, and total from rental items."""
        self.subtotal = sum(item.line_total for item in self.items)
        self.tax_amount = self.subtotal * self.tax_rate
        self.total = self.subtotal + self.tax_amount
    
    def process_return(self):
        """Mark rental as returned."""
        self.return_date = datetime.utcnow()
        # Check if all items are returned
        all_returned = all(item.is_returned for item in self.items)
        self.status = 'returned' if all_returned else 'partial_return'
    
    def check_and_update_status(self):
        """Update status based on current state."""
        if self.status not in ['returned']:
            if self.is_overdue:
                self.status = 'overdue'
    
    def to_dict(self):
        """Serialize rental to dictionary."""
        return {
            'id': self.id,
            'rental_id': self.rental_id,
            'customer_phone': self.customer_phone,
            'customer_name': self.customer_name,
            'employee_id': self.employee_id,
            'subtotal': round(self.subtotal, 2),
            'tax_amount': round(self.tax_amount, 2),
            'total': round(self.total, 2),
            'deposit': round(self.deposit, 2),
            'status': self.status,
            'is_overdue': self.is_overdue,
            'rental_date': self.rental_date.isoformat() if self.rental_date else None,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'return_date': self.return_date.isoformat() if self.return_date else None,
            'items': [item.to_dict() for item in self.items],
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<Rental {self.rental_id}: {self.customer_phone} ({self.status})>'


class RentalItem(db.Model):
    """
    Rental item model (line items for a rental).
    
    Represents individual items within a rental transaction.
    Tracks individual return status for each item.
    
    Attributes:
        id: Primary key
        rental_id: Foreign key to Rental
        item_id: Foreign key to Item
        quantity: Quantity rented
        unit_price: Rental price at time of rental
        line_total: quantity * unit_price
        is_returned: Whether this item has been returned
        return_date: When item was returned
    """
    
    __tablename__ = 'rental_items'
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True)
    
    # Foreign Keys
    rental_id = db.Column(db.Integer, db.ForeignKey('rentals.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)
    
    # Line item details
    quantity = db.Column(db.Integer, nullable=False, default=1)
    unit_price = db.Column(db.Float, nullable=False)
    line_total = db.Column(db.Float, nullable=False)
    
    # Return tracking
    is_returned = db.Column(db.Boolean, default=False)
    return_date = db.Column(db.DateTime, nullable=True)
    
    def __init__(self, rental_id, item_id, quantity, unit_price):
        """Initialize rental item."""
        self.rental_id = rental_id
        self.item_id = item_id
        self.quantity = quantity
        self.unit_price = unit_price
        self.line_total = quantity * unit_price
    
    def mark_returned(self):
        """Mark item as returned."""
        self.is_returned = True
        self.return_date = datetime.utcnow()
    
    def to_dict(self):
        """Serialize rental item to dictionary."""
        return {
            'id': self.id,
            'item_id': self.item_id,
            'item_name': self.item.name if self.item else None,
            'item_code': self.item.item_code if self.item else None,
            'quantity': self.quantity,
            'unit_price': round(self.unit_price, 2),
            'line_total': round(self.line_total, 2),
            'is_returned': self.is_returned,
            'return_date': self.return_date.isoformat() if self.return_date else None
        }
    
    def __repr__(self):
        return f'<RentalItem {self.item_id} x {self.quantity} (returned: {self.is_returned})>'

