"""
Seed script to populate the database with dummy data for testing and screenshots.
"""
import os
import sys
from datetime import datetime, timedelta
import random

# Add the app to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models.employee import Employee
from app.models.item import Item
from app.models.sale import Sale, SaleItem
from app.models.rental import Rental, RentalItem
from app.models.activity_log import ActivityLog

def seed_database():
    """Seed the database with comprehensive dummy data."""
    app = create_app()
    
    with app.app_context():
        # Clear existing data
        print("🗑️  Clearing existing data...")
        db.drop_all()
        db.create_all()
        
        # ========== EMPLOYEES ==========
        print("👥 Creating employees...")
        employees = [
            Employee(
                employee_id='110001',
                first_name='Harry',
                last_name='Larry',
                role='Admin',
                password='admin123'
            ),
            Employee(
                employee_id='110002',
                first_name='Debra',
                last_name='Cooper',
                role='Cashier',
                password='cashier123'
            ),
            Employee(
                employee_id='110003',
                first_name='Clayton',
                last_name='Watson',
                role='Admin',
                password='admin456'
            ),
            Employee(
                employee_id='110004',
                first_name='Sarah',
                last_name='Johnson',
                role='Cashier',
                password='cashier456'
            ),
            Employee(
                employee_id='110005',
                first_name='Michael',
                last_name='Brown',
                role='Cashier',
                password='cashier789'
            ),
        ]
        
        for emp in employees:
            db.session.add(emp)
        db.session.commit()
        print(f"   ✅ Created {len(employees)} employees")
        
        # ========== ITEMS (Grocery/General Store) ==========
        print("📦 Creating inventory items...")
        items_data = [
            # Produce
            ('1001', 'Potato', 'Fresh Idaho potatoes - 1 lb', 'Produce', 1.49, 250),
            ('1002', 'Tomato', 'Vine-ripened tomatoes - each', 'Produce', 0.79, 180),
            ('1003', 'Onion', 'Yellow onions - 1 lb', 'Produce', 1.29, 200),
            ('1004', 'Carrot', 'Fresh carrots - 1 lb bundle', 'Produce', 1.99, 150),
            ('1005', 'Apple', 'Gala apples - each', 'Produce', 0.89, 300),
            ('1006', 'Banana', 'Fresh bananas - 1 lb', 'Produce', 0.59, 400),
            ('1007', 'Orange', 'Navel oranges - each', 'Produce', 0.99, 220),
            ('1008', 'Lettuce', 'Iceberg lettuce - head', 'Produce', 2.49, 80),
            
            # Meat
            ('2001', 'Chicken Breast', 'Boneless skinless - per lb', 'Meat', 5.99, 100),
            ('2002', 'Ground Beef', '80/20 ground beef - per lb', 'Meat', 6.49, 85),
            ('2003', 'Skirt Steak', 'Premium cut - per lb', 'Meat', 12.99, 45),
            ('2004', 'Pork Chops', 'Center cut - per lb', 'Meat', 4.99, 60),
            ('2005', 'Salmon Fillet', 'Atlantic salmon - per lb', 'Meat', 11.99, 40),
            
            # Dairy
            ('3001', 'Milk', 'Whole milk - 1 gallon', 'Dairy', 4.29, 120),
            ('3002', 'Eggs', 'Large eggs - dozen', 'Dairy', 3.99, 150),
            ('3003', 'Butter', 'Unsalted butter - 1 lb', 'Dairy', 5.49, 90),
            ('3004', 'Cheese', 'Cheddar cheese - 8 oz block', 'Dairy', 4.99, 110),
            ('3005', 'Yogurt', 'Greek yogurt - 32 oz', 'Dairy', 6.99, 75),
            
            # Bakery
            ('4001', 'Bread', 'White bread - loaf', 'Bakery', 2.99, 100),
            ('4002', 'Bagels', 'Plain bagels - 6 pack', 'Bakery', 4.49, 60),
            ('4003', 'Croissants', 'Butter croissants - 4 pack', 'Bakery', 5.99, 40),
            ('4004', 'Muffins', 'Blueberry muffins - 4 pack', 'Bakery', 4.99, 55),
            
            # Beverages
            ('5001', 'Cola', 'Coca-Cola - 2 liter', 'Beverages', 2.49, 200),
            ('5002', 'Orange Juice', 'Fresh squeezed - 64 oz', 'Beverages', 5.99, 80),
            ('5003', 'Water', 'Spring water - 24 pack', 'Beverages', 4.99, 150),
            ('5004', 'Coffee', 'Ground coffee - 12 oz', 'Beverages', 8.99, 90),
            ('5005', 'Tea', 'Green tea bags - 20 count', 'Beverages', 4.49, 70),
            
            # Snacks
            ('6001', 'Chips', 'Potato chips - 10 oz bag', 'Snacks', 3.99, 180),
            ('6002', 'Cookies', 'Chocolate chip - 12 oz', 'Snacks', 4.49, 120),
            ('6003', 'Crackers', 'Saltine crackers - 16 oz', 'Snacks', 3.49, 100),
            ('6004', 'Nuts', 'Mixed nuts - 16 oz', 'Snacks', 9.99, 65),
            
            # Household
            ('7001', 'Paper Towels', 'Roll - 2 pack', 'Household', 5.99, 90),
            ('7002', 'Dish Soap', 'Liquid dish soap - 24 oz', 'Household', 3.99, 110),
            ('7003', 'Trash Bags', 'Kitchen bags - 30 count', 'Household', 8.99, 75),
            ('7004', 'Laundry Detergent', 'Liquid detergent - 100 oz', 'Household', 12.99, 50),
            
            # Low stock items (for alerts)
            ('8001', 'Special Sauce', 'House special sauce - 8 oz', 'Specialty', 6.99, 5),
            ('8002', 'Truffle Oil', 'Italian truffle oil - 4 oz', 'Specialty', 24.99, 3),
            ('8003', 'Saffron', 'Premium saffron - 1 gram', 'Specialty', 15.99, 8),
        ]
        
        items = []
        for item_data in items_data:
            item = Item(
                item_code=item_data[0],
                name=item_data[1],
                category=item_data[3],
                price=item_data[4],
                quantity=item_data[5]
            )
            item.description = item_data[2]
            item.min_stock_level = 10
            items.append(item)
            db.session.add(item)
        db.session.commit()
        print(f"   ✅ Created {len(items)} inventory items")
        
        # ========== RENTAL ITEMS (DVDs/Equipment) ==========
        print("🎬 Creating rental items...")
        rental_items_data = [
            ('R001', 'The Theory of Everything', 'DVD - Biography/Drama', 'DVD Rentals', 3.99, 15),
            ('R002', 'Inception', 'DVD - Sci-Fi/Action', 'DVD Rentals', 3.99, 12),
            ('R003', 'The Dark Knight', 'DVD - Action/Crime', 'DVD Rentals', 3.99, 10),
            ('R004', 'Interstellar', 'DVD - Sci-Fi/Adventure', 'DVD Rentals', 4.99, 8),
            ('R005', 'Avengers: Endgame', 'DVD - Action/Superhero', 'DVD Rentals', 4.99, 20),
            ('R006', 'Frozen II', 'DVD - Animation/Family', 'DVD Rentals', 3.99, 18),
            ('R007', 'Joker', 'DVD - Drama/Thriller', 'DVD Rentals', 4.99, 7),
            ('R008', 'Parasite', 'DVD - Drama/Thriller', 'DVD Rentals', 4.99, 6),
        ]
        
        rental_items = []
        for item_data in rental_items_data:
            item = Item(
                item_code=item_data[0],
                name=item_data[1],
                category=item_data[3],
                price=item_data[4],
                quantity=item_data[5],
                is_rentable=True
            )
            item.description = item_data[2]
            item.min_stock_level = 5
            rental_items.append(item)
            db.session.add(item)
        db.session.commit()
        print(f"   ✅ Created {len(rental_items)} rental items")
        
        # Refresh items list
        all_items = Item.query.filter_by(is_rentable=False).all()
        
        # ========== SALES ==========
        print("💰 Creating sales history...")
        sales_created = 0
        
        # Get cashiers
        cashiers = [e for e in employees if e.role == 'Cashier']
        
        # Create sales for the past 30 days
        for days_ago in range(30, -1, -1):
            now = datetime.now()
            sale_date = now - timedelta(days=days_ago)
            num_sales = random.randint(3, 8)
            
            for sale_num in range(num_sales):
                # Random cashier
                cashier = random.choice(cashiers)
                
                # Create sale using the proper constructor
                trans_id = f'SALE-{sale_date.strftime("%Y%m%d")}-{random.randint(1000, 9999):04d}'
                sale = Sale(
                    transaction_id=trans_id,
                    employee_id=cashier.id
                )
                sale.created_at = sale_date + timedelta(hours=random.randint(8, 20), minutes=random.randint(0, 59))
                db.session.add(sale)
                db.session.flush()
                
                # Add 2-6 items to the sale
                num_items = random.randint(2, 6)
                selected_items = random.sample(all_items, min(num_items, len(all_items)))
                
                subtotal = 0
                for item in selected_items:
                    qty = random.randint(1, 3)
                    line_total = item.price * qty
                    subtotal += line_total
                    
                    sale_item = SaleItem(
                        sale_id=sale.id,
                        item_id=item.id,
                        quantity=qty,
                        unit_price=item.price
                    )
                    db.session.add(sale_item)
                
                # Calculate totals
                sale.subtotal = subtotal
                sale.tax_amount = round(subtotal * 0.06, 2)
                sale.total = round(subtotal + sale.tax_amount, 2)
                sale.payment_method = random.choice(['Cash', 'Credit Card', 'Debit Card'])
                sale.amount_paid = sale.total + random.choice([0, 0.03, 0.50, 1.00])
                sale.change_given = round(sale.amount_paid - sale.total, 2)
                sale.status = 'completed'
                
                sales_created += 1
        
        db.session.commit()
        print(f"   ✅ Created {sales_created} sales transactions")
        
        # ========== RENTALS ==========
        print("📀 Creating rentals...")
        rental_db_items = Item.query.filter_by(is_rentable=True).all()
        
        rentals_data = [
            # Active rentals
            ('609-651-5668', 'John Smith', 'active', 0),
            ('728-294-1912', 'Maria Garcia', 'active', -2),
            ('555-123-4567', 'Robert Johnson', 'active', -5),
            # Overdue rentals
            ('555-987-6543', 'Emily Davis', 'overdue', -10),
            ('555-456-7890', 'James Wilson', 'overdue', -8),
            # Returned rentals
            ('555-111-2222', 'Patricia Brown', 'returned', -15),
            ('555-333-4444', 'Michael Taylor', 'returned', -20),
            ('555-555-6666', 'Linda Anderson', 'returned', -12),
        ]
        
        rentals_created = 0
        for rental_data in rentals_data:
            phone, name, status, days_offset = rental_data
            now = datetime.now()
            rental_date = now + timedelta(days=days_offset)
            
            cashier = random.choice(cashiers)
            
            rental = Rental(
                rental_id=f'RENT-{rental_date.strftime("%Y%m%d")}-{random.randint(1000, 9999):04d}',
                customer_phone=phone,
                employee_id=cashier.id,
                due_days=7
            )
            rental.customer_name = name
            rental.rental_date = rental_date
            rental.due_date = rental_date + timedelta(days=7)
            rental.status = status
            
            if status == 'returned':
                rental.return_date = rental.due_date - timedelta(days=random.randint(1, 3))
            
            db.session.add(rental)
            db.session.flush()
            
            # Add 1-3 rental items
            num_items = random.randint(1, 3)
            selected_items = random.sample(rental_db_items, min(num_items, len(rental_db_items)))
            
            subtotal = 0
            for item in selected_items:
                qty = 1
                line_total = item.price * qty
                subtotal += line_total
                
                rental_item = RentalItem(
                    rental_id=rental.id,
                    item_id=item.id,
                    quantity=qty,
                    unit_price=item.price
                )
                if status == 'returned':
                    rental_item.is_returned = True
                    rental_item.return_date = rental.return_date
                db.session.add(rental_item)
            
            rental.subtotal = subtotal
            rental.tax_amount = round(subtotal * 0.06, 2)
            rental.total = round(subtotal + rental.tax_amount, 2)
            rental.deposit = 10.00
            
            rentals_created += 1
        
        db.session.commit()
        print(f"   ✅ Created {rentals_created} rentals")
        
        # ========== ACTIVITY LOGS ==========
        print("📋 Creating activity logs...")
        actions = [
            ('login', 'User logged in'),
            ('logout', 'User logged out'),
            ('sale_completed', 'Completed sale transaction'),
            ('item_added', 'Added new item to inventory'),
            ('item_updated', 'Updated item details'),
            ('rental_created', 'Created new rental'),
            ('rental_returned', 'Processed rental return'),
        ]
        
        logs_created = 0
        for days_ago in range(7, -1, -1):
            now = datetime.now()
            log_date = now - timedelta(days=days_ago)
            num_logs = random.randint(10, 25)
            
            for _ in range(num_logs):
                emp = random.choice(employees)
                action, desc = random.choice(actions)
                
                log = ActivityLog(
                    employee_id=emp.id,
                    action=action,
                    entity_type='system',
                    description=f'{emp.first_name} {emp.last_name}: {desc}',
                    ip_address=f'192.168.1.{random.randint(1, 254)}'
                )
                log.created_at = log_date + timedelta(hours=random.randint(8, 20), minutes=random.randint(0, 59))
                db.session.add(log)
                logs_created += 1
        
        db.session.commit()
        print(f"   ✅ Created {logs_created} activity logs")
        
        # ========== SUMMARY ==========
        print("\n" + "="*60)
        print("🎉 DATABASE SEEDED SUCCESSFULLY!")
        print("="*60)
        print("\n📊 Data Summary:")
        print(f"   • Employees: {Employee.query.count()}")
        print(f"   • Items (Regular): {Item.query.filter_by(is_rentable=False).count()}")
        print(f"   • Items (Rentable): {Item.query.filter_by(is_rentable=True).count()}")
        print(f"   • Sales: {Sale.query.count()}")
        print(f"   • Rentals: {Rental.query.count()}")
        print(f"   • Activity Logs: {ActivityLog.query.count()}")
        
        print("\n" + "="*60)
        print("🔐 LOGIN CREDENTIALS")
        print("="*60)
        print("\n👔 ADMIN ACCOUNTS:")
        print("   ┌────────────────────────────────────────────┐")
        print("   │  Employee ID   │  Name           │ Password│")
        print("   ├────────────────────────────────────────────┤")
        print("   │  110001        │  Harry Larry    │ admin123│")
        print("   │  110003        │  Clayton Watson │ admin456│")
        print("   └────────────────────────────────────────────┘")
        
        print("\n💵 CASHIER ACCOUNTS:")
        print("   ┌────────────────────────────────────────────┐")
        print("   │  Employee ID   │  Name           │ Password│")
        print("   ├────────────────────────────────────────────┤")
        print("   │  110002        │  Debra Cooper   │cashier123│")
        print("   │  110004        │  Sarah Johnson  │cashier456│")
        print("   │  110005        │  Michael Brown  │cashier789│")
        print("   └────────────────────────────────────────────┘")
        
        print("\n" + "="*60)
        print("📸 SCREENSHOT GUIDE")
        print("="*60)
        print("""
🌐 Access: http://127.0.0.1:5000

📱 ADMIN FEATURES (Login as 110001 / admin123):
   1. Dashboard → Shows sales stats, low stock alerts
   2. Employees → Add/Edit/Delete employees
   3. Inventory → Manage all products
   4. Reports → Sales, Inventory, Activity reports
   5. Rentals → Manage DVD rentals

💳 CASHIER FEATURES (Login as 110002 / cashier123):
   1. Dashboard → Quick access to POS
   2. New Sale → Process customer purchases
   3. Rentals → Create/Return rentals
   4. View Inventory (read-only)

📦 SAMPLE ITEM CODES FOR TESTING SALES:
   • 1001 - Potato ($1.49)
   • 2001 - Chicken Breast ($5.99)
   • 3001 - Milk ($4.29)
   • 5001 - Cola ($2.49)
   • 6001 - Chips ($3.99)
""")

if __name__ == '__main__':
    seed_database()
