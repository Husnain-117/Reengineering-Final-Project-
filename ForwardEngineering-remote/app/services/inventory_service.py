"""
Inventory Service
==================
Handles inventory management operations.

Improvements over Legacy:
- Database transactions (vs file overwrite)
- Low stock alerts
- Search and filtering capabilities
- Category management
"""

from app import db
from app.models.item import Item
from app.models.activity_log import ActivityLog


class InventoryService:
    """Service class for inventory operations."""
    
    @staticmethod
    def get_all_items(include_inactive=False):
        """
        Get all inventory items.
        
        Args:
            include_inactive: Include soft-deleted items
        
        Returns:
            list: List of Item objects
        """
        query = Item.query
        if not include_inactive:
            query = query.filter_by(is_active=True)
        return query.order_by(Item.name).all()
    
    @staticmethod
    def get_item_by_id(item_id):
        """Get item by primary key."""
        return Item.query.get(item_id)
    
    @staticmethod
    def get_item_by_code(item_code):
        """Get item by business code (e.g., '1000')."""
        return Item.query.filter_by(item_code=item_code, is_active=True).first()
    
    @staticmethod
    def search_items(query_string, category=None):
        """
        Search items by name or code.
        
        Args:
            query_string: Search term
            category: Optional category filter
        
        Returns:
            list: Matching Item objects
        """
        query = Item.query.filter(
            Item.is_active == True,
            (Item.name.ilike(f'%{query_string}%') | 
             Item.item_code.ilike(f'%{query_string}%'))
        )
        
        if category:
            query = query.filter_by(category=category)
        
        return query.order_by(Item.name).all()
    
    @staticmethod
    def create_item(item_code, name, price, quantity=0, category='General', 
                    is_rentable=False, employee_id=None):
        """
        Create a new inventory item.
        
        Args:
            item_code: Business identifier
            name: Item name
            price: Item price
            quantity: Initial quantity
            category: Item category
            is_rentable: Can item be rented
            employee_id: ID of creating employee (for logging)
        
        Returns:
            tuple: (success: bool, item: Item or None, message: str)
        """
        # Check for duplicate code
        existing = Item.query.filter_by(item_code=item_code).first()
        if existing:
            return False, None, f"Item code {item_code} already exists"
        
        item = Item(
            item_code=item_code,
            name=name,
            price=price,
            quantity=quantity,
            category=category,
            is_rentable=is_rentable
        )
        
        db.session.add(item)
        db.session.commit()
        
        # Log activity
        if employee_id:
            ActivityLog.log(
                action=ActivityLog.ACTION_ITEM_CREATE,
                employee_id=employee_id,
                entity_type='item',
                entity_id=item.id,
                description=f"Created item: {name}"
            )
        
        return True, item, "Item created successfully"
    
    @staticmethod
    def update_item(item_id, employee_id=None, **kwargs):
        """
        Update an existing item.
        
        Args:
            item_id: Item's primary key
            employee_id: ID of updating employee
            **kwargs: Fields to update
        
        Returns:
            tuple: (success: bool, item: Item or None, message: str)
        """
        item = Item.query.get(item_id)
        if not item:
            return False, None, "Item not found"
        
        # Update allowed fields
        allowed_fields = ['name', 'price', 'quantity', 'category', 
                         'description', 'min_stock_level', 'is_rentable']
        
        for field in allowed_fields:
            if field in kwargs:
                setattr(item, field, kwargs[field])
        
        db.session.commit()
        
        # Log activity
        if employee_id:
            ActivityLog.log(
                action=ActivityLog.ACTION_ITEM_UPDATE,
                employee_id=employee_id,
                entity_type='item',
                entity_id=item.id,
                description=f"Updated item: {item.name}"
            )
        
        return True, item, "Item updated successfully"
    
    @staticmethod
    def update_quantity(item_id, amount, operation='subtract', employee_id=None):
        """
        Update item quantity.
        
        Args:
            item_id: Item's primary key
            amount: Quantity to add/subtract
            operation: 'add' or 'subtract'
            employee_id: ID of employee making change
        
        Returns:
            tuple: (success: bool, message: str)
        """
        item = Item.query.get(item_id)
        if not item:
            return False, "Item not found"
        
        success = item.update_quantity(amount, operation)
        if not success:
            return False, "Insufficient stock"
        
        db.session.commit()
        return True, f"Quantity updated successfully. New quantity: {item.quantity}"
    
    @staticmethod
    def delete_item(item_id, employee_id=None):
        """
        Soft delete an item.
        
        Args:
            item_id: Item's primary key
            employee_id: ID of deleting employee
        
        Returns:
            tuple: (success: bool, message: str)
        """
        item = Item.query.get(item_id)
        if not item:
            return False, "Item not found"
        
        item.is_active = False
        db.session.commit()
        
        # Log activity
        if employee_id:
            ActivityLog.log(
                action=ActivityLog.ACTION_ITEM_DELETE,
                employee_id=employee_id,
                entity_type='item',
                entity_id=item.id,
                description=f"Deleted item: {item.name}"
            )
        
        return True, "Item deleted successfully"
    
    @staticmethod
    def get_low_stock_items():
        """Get items with quantity below minimum threshold."""
        return Item.query.filter(
            Item.is_active == True,
            Item.quantity <= Item.min_stock_level
        ).order_by(Item.quantity).all()
    
    @staticmethod
    def get_categories():
        """Get list of unique categories."""
        result = db.session.query(Item.category).filter(
            Item.is_active == True
        ).distinct().all()
        return [r[0] for r in result if r[0]]

