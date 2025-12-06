"""
Sale and SaleItem Models
=========================
Represents sales transactions with proper normalization.

Legacy System Issues Addressed:
- Flat file records → Normalized Sale + SaleItem tables
- No transaction tracking → Proper transaction with items
- Tax calculated inline → Stored subtotal, tax, total
- No refund support → Refund tracking added
- No cashier tracking → Linked to Employee

Database Design:
- One-to-Many: Sale has many SaleItems
- Proper foreign key relationships
- Transaction integrity through relationships
"""

from datetime import datetime
from app import db


class Sale(db.Model):
    """
    Sale transaction model.
    
    Represents a complete sales transaction with header information.
    Individual items are stored in SaleItem (normalized design).
    
    Attributes:
        id: Primary key
        transaction_id: Business transaction identifier
        employee_id: Foreign key to cashier
        subtotal: Pre-tax total
        tax_rate: Applied tax rate
        tax_amount: Calculated tax
        total: Final total (subtotal + tax)
        payment_method: Cash, Card, etc.
        status: completed, refunded, voided
        created_at: Transaction timestamp
    """
    
    __tablename__ = 'sales'
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True)
    
    # Transaction identifier
    transaction_id = db.Column(db.String(50), unique=True, nullable=False, index=True)
    
    # Foreign key to Employee (cashier who processed the sale)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    
    # Financial details
    subtotal = db.Column(db.Float, nullable=False, default=0.0)
    tax_rate = db.Column(db.Float, nullable=False, default=0.06)
    tax_amount = db.Column(db.Float, nullable=False, default=0.0)
    total = db.Column(db.Float, nullable=False, default=0.0)
    
    # Payment information
    payment_method = db.Column(db.String(20), default='Cash')
    amount_paid = db.Column(db.Float, default=0.0)
    change_given = db.Column(db.Float, default=0.0)
    
    # Transaction status
    status = db.Column(db.String(20), default='completed')  # completed, refunded, voided
    
    # Notes
    notes = db.Column(db.Text, nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    items = db.relationship('SaleItem', backref='sale', lazy='dynamic', cascade='all, delete-orphan')
    
    def __init__(self, transaction_id, employee_id, tax_rate=0.06):
        """Initialize sale transaction."""
        self.transaction_id = transaction_id
        self.employee_id = employee_id
        self.tax_rate = tax_rate
    
    def calculate_totals(self):
        """Calculate subtotal, tax, and total from sale items."""
        self.subtotal = sum(item.line_total for item in self.items)
        self.tax_amount = self.subtotal * self.tax_rate
        self.total = self.subtotal + self.tax_amount
    
    def process_payment(self, amount_paid, payment_method='Cash'):
        """Process payment for the sale."""
        self.payment_method = payment_method
        self.amount_paid = amount_paid
        self.change_given = max(0, amount_paid - self.total)
        self.status = 'completed'
    
    def to_dict(self):
        """Serialize sale to dictionary."""
        return {
            'id': self.id,
            'transaction_id': self.transaction_id,
            'employee_id': self.employee_id,
            'subtotal': round(self.subtotal, 2),
            'tax_rate': self.tax_rate,
            'tax_amount': round(self.tax_amount, 2),
            'total': round(self.total, 2),
            'payment_method': self.payment_method,
            'amount_paid': round(self.amount_paid, 2),
            'change_given': round(self.change_given, 2),
            'status': self.status,
            'items': [item.to_dict() for item in self.items],
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<Sale {self.transaction_id}: ${self.total:.2f}>'


class SaleItem(db.Model):
    """
    Sale item model (line items for a sale).
    
    Represents individual items within a sale transaction.
    This is the normalized junction between Sale and Item.
    
    Attributes:
        id: Primary key
        sale_id: Foreign key to Sale
        item_id: Foreign key to Item
        quantity: Quantity purchased
        unit_price: Price at time of sale
        line_total: quantity * unit_price
    """
    
    __tablename__ = 'sale_items'
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True)
    
    # Foreign Keys
    sale_id = db.Column(db.Integer, db.ForeignKey('sales.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)
    
    # Line item details
    quantity = db.Column(db.Integer, nullable=False, default=1)
    unit_price = db.Column(db.Float, nullable=False)  # Price at time of sale
    
    # Calculated total for this line
    line_total = db.Column(db.Float, nullable=False)
    
    def __init__(self, sale_id, item_id, quantity, unit_price):
        """Initialize sale item."""
        self.sale_id = sale_id
        self.item_id = item_id
        self.quantity = quantity
        self.unit_price = unit_price
        self.line_total = quantity * unit_price
    
    def to_dict(self):
        """Serialize sale item to dictionary."""
        return {
            'id': self.id,
            'item_id': self.item_id,
            'item_name': self.item.name if self.item else None,
            'item_code': self.item.item_code if self.item else None,
            'quantity': self.quantity,
            'unit_price': round(self.unit_price, 2),
            'line_total': round(self.line_total, 2)
        }
    
    def __repr__(self):
        return f'<SaleItem {self.item_id} x {self.quantity}>'

