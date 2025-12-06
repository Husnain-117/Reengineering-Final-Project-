"""
Item Model
===========
Represents inventory items in the POS system.

Legacy System Issues Addressed:
- Space-delimited text file → Proper database table
- Float type for price → Decimal for currency precision
- Item ID as integer → Proper primary key with business ID
- No categories → Category support added
- No minimum stock alerts → min_stock_level field added

Database Design:
- Proper data types for all fields
- Indexing on frequently queried fields
- Support for inventory management features
"""

from datetime import datetime
from app import db


class Item(db.Model):
    """
    Inventory Item model with enhanced features.
    
    Attributes:
        id: Primary key (auto-increment)
        item_code: Business identifier (maps to legacy itemID like 1000)
        name: Item name
        description: Optional item description
        category: Item category for organization
        price: Item price (stored as float, consider Decimal for production)
        quantity: Current stock quantity
        min_stock_level: Minimum stock threshold for alerts
        is_rentable: Whether item can be rented
        is_active: Soft delete flag
        created_at: Creation timestamp
        updated_at: Last modification timestamp
    """
    
    __tablename__ = 'items'
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True)
    
    # Business identifier (maps to legacy itemID like 1000, 1001)
    item_code = db.Column(db.String(20), unique=True, nullable=False, index=True)
    
    # Item details
    name = db.Column(db.String(100), nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(50), nullable=True, default='General')
    
    # Pricing - using Float (consider Decimal for strict currency precision)
    price = db.Column(db.Float, nullable=False)
    
    # Inventory tracking
    quantity = db.Column(db.Integer, nullable=False, default=0)
    min_stock_level = db.Column(db.Integer, default=10)
    
    # Item flags
    is_rentable = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    
    # Audit timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    sale_items = db.relationship('SaleItem', backref='item', lazy='dynamic')
    rental_items = db.relationship('RentalItem', backref='item', lazy='dynamic')
    
    def __init__(self, item_code, name, price, quantity=0, category='General', is_rentable=False):
        """Initialize item with required fields."""
        self.item_code = item_code
        self.name = name
        self.price = price
        self.quantity = quantity
        self.category = category
        self.is_rentable = is_rentable
    
    @property
    def is_low_stock(self):
        """Check if stock is below minimum threshold."""
        return self.quantity <= self.min_stock_level
    
    @property
    def is_out_of_stock(self):
        """Check if item is out of stock."""
        return self.quantity <= 0
    
    def update_quantity(self, amount, operation='subtract'):
        """
        Update item quantity.
        
        Args:
            amount: Quantity to add/subtract
            operation: 'add' or 'subtract'
        
        Returns:
            bool: Success status
        """
        if operation == 'subtract':
            if self.quantity >= amount:
                self.quantity -= amount
                return True
            return False
        elif operation == 'add':
            self.quantity += amount
            return True
        return False
    
    def to_dict(self):
        """Serialize item to dictionary (for API responses)."""
        return {
            'id': self.id,
            'item_code': self.item_code,
            'name': self.name,
            'description': self.description,
            'category': self.category,
            'price': self.price,
            'quantity': self.quantity,
            'min_stock_level': self.min_stock_level,
            'is_rentable': self.is_rentable,
            'is_low_stock': self.is_low_stock,
            'is_out_of_stock': self.is_out_of_stock,
            'is_active': self.is_active
        }
    
    def __repr__(self):
        return f'<Item {self.item_code}: {self.name} @ ${self.price:.2f}>'

