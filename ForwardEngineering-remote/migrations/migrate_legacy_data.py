"""
Legacy Data Migration Script
=============================
Migrates data from legacy .txt files to the new normalized database.

Migration Strategy:
1. Parse legacy text files with their specific formats
2. Transform data to match new schema
3. Validate data integrity
4. Insert into new database with proper relationships

Legacy File Formats:
- employeeDatabase.txt: "110001 Admin Harry Larry password"
- itemDatabase.txt: "1000 Potato 1.0 249"
- rentalDatabase.txt: "1000 TheoryOfEverything 30.0 249"
- userDatabase.txt: "Phone rentedItem1ID,rentedItem1Date,returned1Bool ..."
"""

import os
import sys
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import Employee, Item, Rental, RentalItem


# Legacy file paths (relative to project root)
LEGACY_BASE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '..', 'Database')


def parse_employee_file(filepath):
    """
    Parse legacy employee database file.
    
    Format: "110001 Admin Harry Larry password"
    Fields: employee_id, role, first_name, last_name, password
    """
    employees = []
    
    if not os.path.exists(filepath):
        print(f"Warning: Employee file not found: {filepath}")
        return employees
    
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            parts = line.split(' ')
            if len(parts) >= 5:
                employee = {
                    'employee_id': parts[0],
                    'role': parts[1],
                    'first_name': parts[2],
                    'last_name': parts[3],
                    'password': parts[4]
                }
                employees.append(employee)
    
    return employees


def parse_item_file(filepath):
    """
    Parse legacy item database file.
    
    Format: "1000 Potato 1.0 249"
    Fields: item_code, name, price, quantity
    """
    items = []
    
    if not os.path.exists(filepath):
        print(f"Warning: Item file not found: {filepath}")
        return items
    
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            parts = line.split(' ')
            if len(parts) >= 4:
                item = {
                    'item_code': parts[0],
                    'name': parts[1],
                    'price': float(parts[2]),
                    'quantity': int(parts[3])
                }
                items.append(item)
    
    return items


def parse_rental_item_file(filepath):
    """
    Parse legacy rental database file.
    
    Format: "1000 TheoryOfEverything 30.0 249"
    Fields: item_code, name, price, quantity
    
    These are rentable items (DVDs, movies, etc.)
    """
    items = []
    
    if not os.path.exists(filepath):
        print(f"Warning: Rental item file not found: {filepath}")
        return items
    
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            parts = line.split(' ')
            if len(parts) >= 4:
                item = {
                    'item_code': f"R{parts[0]}",  # Prefix with R to distinguish from regular items
                    'name': parts[1],
                    'price': float(parts[2]),
                    'quantity': int(parts[3]),
                    'is_rentable': True
                }
                items.append(item)
    
    return items


def parse_rental_transactions(filepath):
    """
    Parse legacy user/rental database file.
    
    Format: "Phone rentedItem1ID,rentedItem1Date,returned1Bool ..."
    Example: "6096515668 1000,6/30/09,true 1022,6/31/11,true"
    
    Note: This file structure is complex and denormalized.
    We extract active rentals (returned=false) for migration.
    """
    rentals = []
    
    if not os.path.exists(filepath):
        print(f"Warning: User database file not found: {filepath}")
        return rentals
    
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('Phone'):  # Skip header
                continue
            
            parts = line.split(' ')
            if len(parts) >= 1:
                phone = parts[0]
                
                # Parse rental items (if any)
                if len(parts) > 1:
                    rental_items = []
                    for i in range(1, len(parts)):
                        item_data = parts[i].split(',')
                        if len(item_data) >= 3:
                            rental_item = {
                                'item_id': item_data[0],
                                'date': item_data[1],
                                'is_returned': item_data[2].lower() == 'true'
                            }
                            rental_items.append(rental_item)
                    
                    # Only include rentals with unreturned items
                    unreturned_items = [r for r in rental_items if not r['is_returned']]
                    if unreturned_items:
                        rentals.append({
                            'phone': phone,
                            'items': unreturned_items
                        })
    
    return rentals


def migrate_employees(employees):
    """Migrate employee data to new database."""
    count = 0
    for emp_data in employees:
        # Check if already exists
        existing = Employee.query.filter_by(employee_id=emp_data['employee_id']).first()
        if existing:
            print(f"  Skipping existing employee: {emp_data['employee_id']}")
            continue
        
        employee = Employee(
            employee_id=emp_data['employee_id'],
            first_name=emp_data['first_name'],
            last_name=emp_data['last_name'],
            password=emp_data['password'],  # Will be hashed by model
            role=emp_data['role']
        )
        db.session.add(employee)
        count += 1
    
    db.session.commit()
    return count


def migrate_items(items):
    """Migrate item data to new database."""
    count = 0
    for item_data in items:
        # Check if already exists
        existing = Item.query.filter_by(item_code=item_data['item_code']).first()
        if existing:
            print(f"  Skipping existing item: {item_data['item_code']}")
            continue
        
        item = Item(
            item_code=item_data['item_code'],
            name=item_data['name'],
            price=item_data['price'],
            quantity=item_data['quantity'],
            is_rentable=item_data.get('is_rentable', False)
        )
        db.session.add(item)
        count += 1
    
    db.session.commit()
    return count


def run_migration():
    """Run complete migration from legacy files to new database."""
    print("=" * 60)
    print("LEGACY DATA MIGRATION")
    print("=" * 60)
    print(f"Migration started at: {datetime.now()}")
    print(f"Legacy data path: {LEGACY_BASE}")
    print()
    
    # Create app context
    app = create_app('development')
    
    with app.app_context():
        # Create all tables
        db.create_all()
        print("Database tables created successfully.")
        print()
        
        # Migrate Employees
        print("Migrating Employees...")
        emp_file = os.path.join(LEGACY_BASE, 'employeeDatabase.txt')
        employees = parse_employee_file(emp_file)
        print(f"  Found {len(employees)} employees in legacy file")
        emp_count = migrate_employees(employees)
        print(f"  Migrated {emp_count} employees")
        print()
        
        # Migrate Regular Items
        print("Migrating Regular Items...")
        item_file = os.path.join(LEGACY_BASE, 'itemDatabase.txt')
        items = parse_item_file(item_file)
        print(f"  Found {len(items)} items in legacy file")
        item_count = migrate_items(items)
        print(f"  Migrated {item_count} items")
        print()
        
        # Migrate Rental Items
        print("Migrating Rental Items...")
        rental_item_file = os.path.join(LEGACY_BASE, 'rentalDatabase.txt')
        rental_items = parse_rental_item_file(rental_item_file)
        print(f"  Found {len(rental_items)} rental items in legacy file")
        rental_item_count = migrate_items(rental_items)
        print(f"  Migrated {rental_item_count} rental items")
        print()
        
        # Summary
        print("=" * 60)
        print("MIGRATION SUMMARY")
        print("=" * 60)
        print(f"Total Employees migrated: {emp_count}")
        print(f"Total Regular Items migrated: {item_count}")
        print(f"Total Rental Items migrated: {rental_item_count}")
        print(f"Migration completed at: {datetime.now()}")
        print()
        
        # Verify migration
        print("Verification:")
        print(f"  Employees in database: {Employee.query.count()}")
        print(f"  Items in database: {Item.query.count()}")
        print(f"  Rentals in database: {Rental.query.count()}")


if __name__ == '__main__':
    run_migration()

