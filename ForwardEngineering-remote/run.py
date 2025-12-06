#!/usr/bin/env python3
"""
POS System Application Entry Point
====================================
Run this file to start the development server.

Usage:
    python run.py

For production, use:
    gunicorn -w 4 -b 0.0.0.0:5000 'app:create_app("production")'
"""

import os
from app import create_app, db
from app.models import Employee, Item

# Create the application
app = create_app(os.environ.get('FLASK_ENV', 'development'))


def init_db():
    """Initialize database with sample data if empty."""
    with app.app_context():
        # Check if any employees exist
        if Employee.query.count() == 0:
            print("Initializing database with default admin user...")
            
            # Create default admin
            admin = Employee(
                employee_id='110001',
                first_name='Admin',
                last_name='User',
                password='admin123',
                role='Admin'
            )
            db.session.add(admin)
            
            # Create sample cashier
            cashier = Employee(
                employee_id='110002',
                first_name='John',
                last_name='Cashier',
                password='cashier123',
                role='Cashier'
            )
            db.session.add(cashier)
            
            db.session.commit()
            print("Default users created:")
            print("  Admin - ID: 110001, Password: admin123")
            print("  Cashier - ID: 110002, Password: cashier123")
        
        # Check if any items exist
        if Item.query.count() == 0:
            print("Adding sample items...")
            
            sample_items = [
                ('1000', 'Potato', 1.0, 249, 'Grocery'),
                ('1001', 'PlasticCup', 0.5, 376, 'Supplies'),
                ('1002', 'SkirtSteak', 15.0, 1055, 'Meat'),
                ('1003', 'PotatoChips', 1.2, 168, 'Snacks'),
                ('1004', 'Curry', 2.3, 500, 'Spices'),
                ('1005', 'Tomato', 0.8, 150, 'Grocery'),
                ('1006', 'Pineapple', 2.0, 201, 'Fruits'),
                ('1007', 'Apple', 0.6, 200, 'Fruits'),
            ]
            
            for code, name, price, qty, category in sample_items:
                item = Item(
                    item_code=code,
                    name=name,
                    price=price,
                    quantity=qty,
                    category=category
                )
                db.session.add(item)
            
            # Add some rentable items
            rentable_items = [
                ('R1000', 'TheoryOfEverything', 30.0, 249, True),
                ('R1001', 'AdventuresOfTomSawyer', 40.5, 391, True),
                ('R1002', 'PrideAndPrejudice', 30.0, 995, True),
            ]
            
            for code, name, price, qty, rentable in rentable_items:
                item = Item(
                    item_code=code,
                    name=name,
                    price=price,
                    quantity=qty,
                    category='Movies',
                    is_rentable=rentable
                )
                db.session.add(item)
            
            db.session.commit()
            print(f"Added {len(sample_items) + len(rentable_items)} sample items")


if __name__ == '__main__':
    init_db()
    print("\n" + "="*50)
    print("SG Technologies POS System")
    print("="*50)
    print("Starting development server...")
    print("Open http://127.0.0.1:5000 in your browser")
    print("="*50 + "\n")
    app.run(debug=True, host='0.0.0.0', port=5000)

