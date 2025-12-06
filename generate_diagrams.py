"""
Generate professional diagrams for the Software Reengineering Report
Run this script to create all missing diagrams in the images folder
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle, Circle
import numpy as np
import os

# Set the output directory
OUTPUT_DIR = "images"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Common styling
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 10

# Color palette (professional, not too flashy)
COLORS = {
    'legacy': '#E74C3C',      # Red for legacy
    'new': '#27AE60',         # Green for new/reengineered
    'ui': '#3498DB',          # Blue for UI layer
    'business': '#F39C12',    # Orange for business logic
    'data': '#9B59B6',        # Purple for data layer
    'database': '#1ABC9C',    # Teal for database
    'light_gray': '#ECF0F1',
    'dark_gray': '#2C3E50',
    'white': '#FFFFFF',
    'arrow': '#34495E'
}


def draw_box(ax, x, y, width, height, text, color, text_color='white', fontsize=9):
    """Draw a rounded rectangle box with text"""
    box = FancyBboxPatch((x, y), width, height,
                         boxstyle="round,pad=0.02,rounding_size=0.1",
                         facecolor=color, edgecolor='#2C3E50', linewidth=1.5)
    ax.add_patch(box)
    ax.text(x + width/2, y + height/2, text, ha='center', va='center',
            fontsize=fontsize, color=text_color, fontweight='bold', wrap=True)


def draw_arrow(ax, start, end, color='#34495E'):
    """Draw an arrow between two points"""
    ax.annotate('', xy=end, xytext=start,
                arrowprops=dict(arrowstyle='->', color=color, lw=2))


# =============================================================================
# 1. Legacy System Overview Diagram
# =============================================================================
def create_legacy_system_overview():
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis('off')
    ax.set_title('Legacy POS System Architecture', fontsize=14, fontweight='bold', pad=20)
    
    # Java Swing UI Layer
    draw_box(ax, 0.5, 4.5, 9, 1, 'Java Swing UI Layer', COLORS['ui'])
    
    # UI Components
    ui_components = ['Login\nInterface', 'Cashier\nInterface', 'Admin\nInterface', 'Transaction\nInterface']
    for i, comp in enumerate(ui_components):
        draw_box(ax, 0.8 + i*2.3, 3.3, 1.8, 0.9, comp, COLORS['light_gray'], COLORS['dark_gray'], 8)
    
    # Arrows from UI to Business
    for i in range(4):
        draw_arrow(ax, (1.7 + i*2.3, 3.3), (1.7 + i*2.3, 2.5))
    
    # Business Logic Layer
    draw_box(ax, 0.5, 1.5, 9, 1, 'Business Logic (Mixed Concerns)', COLORS['business'])
    
    # Business Components
    biz_components = ['POSSystem', 'POS/POR/POH', 'Inventory', 'Management']
    for i, comp in enumerate(biz_components):
        draw_box(ax, 0.8 + i*2.3, 0.5, 1.8, 0.7, comp, COLORS['light_gray'], COLORS['dark_gray'], 8)
    
    # Arrows to files
    for i in range(4):
        draw_arrow(ax, (1.7 + i*2.3, 0.5), (5, -0.3))
    
    # Text Files (Data Layer)
    draw_box(ax, 2.5, -1.2, 5, 0.8, '.txt Files (No Database)', COLORS['legacy'])
    
    # Problem annotations
    ax.text(9.5, 5, '[X] No separation\n    of concerns', fontsize=8, color=COLORS['legacy'])
    ax.text(9.5, 1.5, '[X] Scattered\n    file I/O', fontsize=8, color=COLORS['legacy'])
    ax.text(9.5, -0.8, '[X] Plaintext\n    passwords', fontsize=8, color=COLORS['legacy'])
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/legacy_system_overview.png', dpi=150, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("Created: legacy_system_overview.png")


# =============================================================================
# 2. Legacy Dependency Map
# =============================================================================
def create_legacy_dependency_map():
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.axis('off')
    ax.set_title('Legacy System Dependency Map', fontsize=14, fontweight='bold', pad=20)
    
    # UI Layer
    ax.text(6, 7.5, 'UI LAYER', ha='center', fontsize=11, fontweight='bold', color=COLORS['ui'])
    ui_items = [('Login_Interface', 1.5), ('Cashier_Interface', 4.5), 
                ('Admin_Interface', 7.5), ('Transaction_Interface', 10.5)]
    for name, x in ui_items:
        draw_box(ax, x-1, 6.5, 2, 0.7, name.replace('_', '\n'), COLORS['ui'], fontsize=7)
    
    # Business Layer
    ax.text(6, 5.5, 'BUSINESS LOGIC LAYER', ha='center', fontsize=11, fontweight='bold', color=COLORS['business'])
    biz_items = [('POSSystem', 1), ('PointOfSale', 3), ('POS', 5), ('POR', 7), ('POH', 9), ('Inventory', 11)]
    for name, x in biz_items:
        draw_box(ax, x-0.7, 4.5, 1.4, 0.6, name, COLORS['business'], fontsize=7)
    
    # More business
    biz2_items = [('Management', 3), ('EmployeeManagement', 6), ('Item', 9)]
    for name, x in biz2_items:
        draw_box(ax, x-1, 3.5, 2, 0.6, name, COLORS['business'], fontsize=7)
    
    # Data Layer
    ax.text(6, 2.5, 'DATA LAYER (.txt FILES)', ha='center', fontsize=11, fontweight='bold', color=COLORS['data'])
    data_items = [('itemDatabase.txt', 1.5), ('employeeDatabase.txt', 4.5),
                  ('userDatabase.txt', 7.5), ('saleInvoiceRecord.txt', 10.5)]
    for name, x in data_items:
        draw_box(ax, x-1.2, 1.5, 2.4, 0.6, name, COLORS['data'], fontsize=6)
    
    # Draw dependency arrows
    # Login -> POSSystem
    draw_arrow(ax, (1.5, 6.5), (1.3, 5.1))
    # Cashier -> Transaction
    draw_arrow(ax, (4.5, 6.5), (10.5, 6.5))
    # Transaction -> POS/POR/POH
    draw_arrow(ax, (10.5, 6.5), (5, 5.1))
    draw_arrow(ax, (10.5, 6.5), (7, 5.1))
    draw_arrow(ax, (10.5, 6.5), (9, 5.1))
    # Business to Data
    draw_arrow(ax, (5, 4.5), (1.5, 2.1))
    draw_arrow(ax, (11, 4.5), (1.5, 2.1))
    draw_arrow(ax, (3, 3.5), (7.5, 2.1))
    
    # Legend
    ax.text(0.5, 0.5, 'Arrows show dependencies (calls/uses)', fontsize=8, style='italic')
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/legacy_dependency_map.png', dpi=150, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("Created: legacy_dependency_map.png")


# =============================================================================
# 3. Legacy Class Diagram (Simplified UML)
# =============================================================================
def create_legacy_class_diagram():
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.set_title('Legacy System Class Diagram (Simplified)', fontsize=14, fontweight='bold', pad=20)
    
    def draw_class_box(ax, x, y, name, attributes, methods, color):
        """Draw a UML-style class box"""
        height = 0.4 + len(attributes)*0.25 + len(methods)*0.25
        # Class name section
        rect = FancyBboxPatch((x, y), 2.5, height, boxstyle="round,pad=0.02",
                              facecolor=COLORS['light_gray'], edgecolor=color, linewidth=2)
        ax.add_patch(rect)
        # Name
        ax.text(x+1.25, y+height-0.2, name, ha='center', va='center',
                fontsize=9, fontweight='bold', color=color)
        # Separator line
        ax.plot([x, x+2.5], [y+height-0.4, y+height-0.4], color=color, lw=1)
        # Attributes
        for i, attr in enumerate(attributes):
            ax.text(x+0.1, y+height-0.5-i*0.25, f'- {attr}', fontsize=7, color=COLORS['dark_gray'])
        # Separator
        sep_y = y+height-0.4-len(attributes)*0.25
        ax.plot([x, x+2.5], [sep_y, sep_y], color=color, lw=1)
        # Methods
        for i, method in enumerate(methods):
            ax.text(x+0.1, sep_y-0.15-i*0.25, f'+ {method}', fontsize=7, color=COLORS['dark_gray'])
        return y + height/2
    
    # UI Classes
    ax.text(2, 9.5, '<<Interface>>', ha='center', fontsize=8, style='italic')
    draw_class_box(ax, 0.5, 7.5, 'Login_Interface', ['username', 'password'], ['actionPerformed()'], COLORS['ui'])
    draw_class_box(ax, 3.5, 7.5, 'Cashier_Interface', ['buttons[]'], ['showOptions()'], COLORS['ui'])
    draw_class_box(ax, 6.5, 7.5, 'Admin_Interface', ['adminPanel'], ['manageEmployees()'], COLORS['ui'])
    draw_class_box(ax, 9.5, 7.5, 'Transaction_Interface', ['cart', 'total'], ['processTransaction()'], COLORS['ui'])
    
    # Business Classes
    draw_class_box(ax, 0.5, 4.5, 'POSSystem', ['username: static', 'role: static', 'employees: static'], ['logIn()', 'logOut()'], COLORS['business'])
    draw_class_box(ax, 4, 4.5, 'PointOfSale', ['inventory', 'cart'], ['startTransaction()', 'endPOS()'], COLORS['business'])
    draw_class_box(ax, 8, 4.5, 'Inventory', ['items: ArrayList'], ['loadItems()', 'saveItems()'], COLORS['business'])
    draw_class_box(ax, 11, 4.5, 'Management', ['rentals'], ['addRental()'], COLORS['business'])
    
    # Data Classes
    draw_class_box(ax, 2, 1.5, 'Employee', ['id', 'name', 'role', 'password'], ['getPassword()'], COLORS['data'])
    draw_class_box(ax, 6, 1.5, 'Item', ['id', 'name', 'price', 'quantity'], ['getPrice()'], COLORS['data'])
    
    # Arrows (simplified)
    draw_arrow(ax, (1.75, 7.5), (1.75, 6.5))
    draw_arrow(ax, (10.75, 7.5), (5.25, 6.5))
    draw_arrow(ax, (5.25, 4.5), (3.25, 3.2))
    draw_arrow(ax, (9.25, 4.5), (7.25, 3.2))
    
    # Notes
    ax.text(12.5, 8, 'Issues:\n• Tight coupling\n• No data layer\n• Static fields', 
            fontsize=8, color=COLORS['legacy'], bbox=dict(boxstyle='round', facecolor='#FADBD8'))
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/legacy_class_diagram.png', dpi=150, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("Created: legacy_class_diagram.png")


# =============================================================================
# 4. Code Restructuring Diagram
# =============================================================================
def create_code_restructuring():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    for ax in [ax1, ax2]:
        ax.set_xlim(0, 6)
        ax.set_ylim(0, 6)
        ax.axis('off')
    
    # BEFORE - Left side
    ax1.set_title('BEFORE (Legacy)', fontsize=12, fontweight='bold', color=COLORS['legacy'])
    
    # Monolithic structure
    draw_box(ax1, 0.5, 0.5, 5, 5, '', COLORS['light_gray'])
    ax1.text(3, 5.2, 'Monolithic Structure', ha='center', fontsize=10, fontweight='bold')
    
    # Mixed components inside
    draw_box(ax1, 1, 4, 1.5, 0.7, 'UI Code', COLORS['ui'], fontsize=8)
    draw_box(ax1, 3, 4, 1.5, 0.7, 'Business\nLogic', COLORS['business'], fontsize=8)
    draw_box(ax1, 1, 2.8, 1.5, 0.7, 'File I/O', COLORS['data'], fontsize=8)
    draw_box(ax1, 3, 2.8, 1.5, 0.7, 'Validation', COLORS['new'], fontsize=8)
    draw_box(ax1, 2, 1.5, 2, 0.7, 'Global State', COLORS['legacy'], fontsize=8)
    
    # Tangled arrows
    ax1.annotate('', xy=(3, 4), xytext=(1.5, 4), arrowprops=dict(arrowstyle='<->', color='gray', lw=1))
    ax1.annotate('', xy=(3, 2.8), xytext=(1.5, 2.8), arrowprops=dict(arrowstyle='<->', color='gray', lw=1))
    ax1.annotate('', xy=(2, 4), xytext=(2, 2.8), arrowprops=dict(arrowstyle='<->', color='gray', lw=1))
    ax1.annotate('', xy=(4, 4), xytext=(4, 2.8), arrowprops=dict(arrowstyle='<->', color='gray', lw=1))
    
    ax1.text(3, 0.3, '[X] High Coupling | [X] Hard to Test', ha='center', fontsize=9, color=COLORS['legacy'])
    
    # Arrow between diagrams
    fig.text(0.5, 0.5, '→', fontsize=40, ha='center', va='center', color=COLORS['arrow'])
    
    # AFTER - Right side
    ax2.set_title('AFTER (Reengineered)', fontsize=12, fontweight='bold', color=COLORS['new'])
    
    # Layered structure
    ax2.text(3, 5.5, 'Layered Architecture', ha='center', fontsize=10, fontweight='bold')
    
    # Presentation Layer
    draw_box(ax2, 0.5, 4.5, 5, 0.8, 'Presentation Layer (Routes + Templates)', COLORS['ui'], fontsize=8)
    
    # Business Layer
    draw_box(ax2, 0.5, 3.2, 5, 0.8, 'Service Layer (AuthService, SalesService)', COLORS['business'], fontsize=8)
    
    # Data Access Layer
    draw_box(ax2, 0.5, 1.9, 5, 0.8, 'Data Access Layer (SQLAlchemy Models)', COLORS['data'], fontsize=8)
    
    # Database
    draw_box(ax2, 0.5, 0.6, 5, 0.8, 'Database (SQLite/PostgreSQL)', COLORS['database'], fontsize=8)
    
    # Downward arrows only
    draw_arrow(ax2, (3, 4.5), (3, 4))
    draw_arrow(ax2, (3, 3.2), (3, 2.7))
    draw_arrow(ax2, (3, 1.9), (3, 1.4))
    
    ax2.text(3, 0.1, '[OK] Low Coupling | [OK] Testable | [OK] Maintainable', ha='center', fontsize=9, color=COLORS['new'])
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/code_restructuring.png', dpi=150, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("Created: code_restructuring.png")


# =============================================================================
# 5. Database ERD
# =============================================================================
def create_database_erd():
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.set_title('Database Entity-Relationship Diagram', fontsize=14, fontweight='bold', pad=20)
    
    def draw_entity(ax, x, y, name, fields, pk_count=1):
        """Draw an entity box with fields"""
        height = 0.4 + len(fields)*0.3
        width = 2.8
        # Entity box
        rect = FancyBboxPatch((x, y), width, height, boxstyle="round,pad=0.02",
                              facecolor=COLORS['light_gray'], edgecolor=COLORS['database'], linewidth=2)
        ax.add_patch(rect)
        # Name header
        header = FancyBboxPatch((x, y+height-0.4), width, 0.4, boxstyle="round,pad=0.02",
                                facecolor=COLORS['database'], edgecolor=COLORS['database'], linewidth=2)
        ax.add_patch(header)
        ax.text(x+width/2, y+height-0.2, name, ha='center', va='center',
                fontsize=10, fontweight='bold', color='white')
        # Fields
        for i, field in enumerate(fields):
            prefix = '[PK] ' if i < pk_count else '     '
            ax.text(x+0.1, y+height-0.6-i*0.3, prefix + field, fontsize=8, color=COLORS['dark_gray'])
        return (x + width/2, y + height/2)
    
    # Entities
    emp_center = draw_entity(ax, 0.5, 6, 'employees', ['id (PK)', 'employee_id', 'first_name', 'last_name', 'role', 'password_hash', 'is_active', 'created_at'])
    item_center = draw_entity(ax, 5.5, 6, 'items', ['id (PK)', 'item_code', 'name', 'category', 'price', 'quantity', 'is_rentable', 'is_active'])
    sale_center = draw_entity(ax, 10.5, 6, 'sales', ['id (PK)', 'transaction_id', 'employee_id (FK)', 'subtotal', 'tax_amount', 'total', 'status', 'created_at'])
    
    sale_item_center = draw_entity(ax, 5.5, 1.5, 'sale_items', ['id (PK)', 'sale_id (FK)', 'item_id (FK)', 'quantity', 'unit_price', 'line_total'])
    rental_center = draw_entity(ax, 0.5, 1.5, 'rentals', ['id (PK)', 'rental_id', 'customer_phone', 'employee_id (FK)', 'status', 'due_date'])
    activity_center = draw_entity(ax, 10.5, 1.5, 'activity_logs', ['id (PK)', 'employee_id (FK)', 'action', 'entity_type', 'description', 'created_at'])
    
    # Relationships
    # Employee to Sales (1:N)
    ax.annotate('', xy=(10.5, 7), xytext=(3.3, 7), arrowprops=dict(arrowstyle='->', color=COLORS['arrow'], lw=1.5))
    ax.text(6.5, 7.2, '1:N', fontsize=8, ha='center')
    
    # Sales to Sale_Items (1:N)
    ax.annotate('', xy=(8.3, 3), xytext=(12, 6), arrowprops=dict(arrowstyle='->', color=COLORS['arrow'], lw=1.5))
    ax.text(10.5, 4.5, '1:N', fontsize=8)
    
    # Items to Sale_Items (1:N)
    ax.annotate('', xy=(6.9, 4), xytext=(6.9, 6), arrowprops=dict(arrowstyle='->', color=COLORS['arrow'], lw=1.5))
    ax.text(7.1, 5, '1:N', fontsize=8)
    
    # Employee to Rentals
    ax.annotate('', xy=(1.9, 4), xytext=(1.9, 6), arrowprops=dict(arrowstyle='->', color=COLORS['arrow'], lw=1.5))
    ax.text(2.1, 5, '1:N', fontsize=8)
    
    # Employee to Activity
    ax.annotate('', xy=(10.5, 4), xytext=(3.3, 6.5), arrowprops=dict(arrowstyle='->', color=COLORS['arrow'], lw=1.5))
    ax.text(6, 5.5, '1:N', fontsize=8)
    
    # Legend
    ax.text(0.5, 0.3, '[PK] = Primary Key    FK = Foreign Key    1:N = One-to-Many Relationship', fontsize=9)
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/database_erd.png', dpi=150, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("Created: database_erd.png")


# =============================================================================
# 6. Architecture Comparison
# =============================================================================
def create_architecture_comparison():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 8))
    
    for ax in [ax1, ax2]:
        ax.set_xlim(0, 6)
        ax.set_ylim(0, 8)
        ax.axis('off')
    
    # Legacy Architecture
    ax1.set_title('Legacy Architecture', fontsize=12, fontweight='bold', color=COLORS['legacy'], pad=15)
    
    draw_box(ax1, 0.5, 6.5, 5, 1, 'Java Swing Desktop UI', COLORS['ui'])
    ax1.text(3, 6.2, '↓ Direct calls', ha='center', fontsize=8)
    draw_box(ax1, 0.5, 4.5, 5, 1.2, 'Business Logic\n(POSSystem, POS, Inventory)', COLORS['business'], fontsize=9)
    ax1.text(3, 4.2, '↓ FileReader/Writer', ha='center', fontsize=8)
    draw_box(ax1, 0.5, 2.5, 5, 1.2, '.txt Files\n(No Database)', COLORS['legacy'])
    
    # Issues
    issues = ['- Single machine only', '- No web access', '- Plaintext passwords', 
              '- No transactions', '- No test coverage']
    for i, issue in enumerate(issues):
        ax1.text(0.5, 1.8 - i*0.3, issue, fontsize=8, color=COLORS['legacy'])
    
    # Reengineered Architecture
    ax2.set_title('Reengineered Architecture', fontsize=12, fontweight='bold', color=COLORS['new'], pad=15)
    
    draw_box(ax2, 0.5, 6.5, 5, 0.8, 'Web Browser (Any Device)', COLORS['light_gray'], COLORS['dark_gray'])
    ax2.text(3, 6.2, '↓ HTTP/HTTPS', ha='center', fontsize=8)
    draw_box(ax2, 0.5, 5.2, 5, 0.8, 'Flask Routes (Blueprints)', COLORS['ui'])
    ax2.text(3, 4.9, '↓ Service calls', ha='center', fontsize=8)
    draw_box(ax2, 0.5, 3.9, 5, 0.8, 'Service Layer (Business Logic)', COLORS['business'])
    ax2.text(3, 3.6, '↓ ORM queries', ha='center', fontsize=8)
    draw_box(ax2, 0.5, 2.6, 5, 0.8, 'SQLAlchemy Models', COLORS['data'])
    ax2.text(3, 2.3, '↓ SQL', ha='center', fontsize=8)
    draw_box(ax2, 0.5, 1.3, 5, 0.8, 'SQLite / PostgreSQL', COLORS['database'])
    
    # Benefits
    benefits = ['[OK] Web accessible', '[OK] Bcrypt passwords', '[OK] ACID transactions', 
                '[OK] 89% test coverage', '[OK] Modular design']
    for i, benefit in enumerate(benefits):
        ax2.text(0.5, 0.8 - i*0.25, benefit, fontsize=8, color=COLORS['new'])
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/architecture_comparison.png', dpi=150, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("Created: architecture_comparison.png")


# =============================================================================
# 7. Reengineering Process Flow
# =============================================================================
def create_reengineering_flow():
    fig, ax = plt.subplots(1, 1, figsize=(14, 6))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 6)
    ax.axis('off')
    ax.set_title('Software Reengineering Process Flow', fontsize=14, fontweight='bold', pad=20)
    
    # Process boxes
    phases = [
        ('Inventory\nAnalysis', COLORS['ui']),
        ('Document\nRestructuring', COLORS['ui']),
        ('Reverse\nEngineering', COLORS['business']),
        ('Code\nRestructuring', COLORS['business']),
        ('Data\nRestructuring', COLORS['data']),
        ('Forward\nEngineering', COLORS['new'])
    ]
    
    box_width = 1.8
    start_x = 0.5
    y = 3
    
    for i, (phase, color) in enumerate(phases):
        x = start_x + i * 2.2
        draw_box(ax, x, y, box_width, 1.2, phase, color, fontsize=8)
        
        # Arrow to next
        if i < len(phases) - 1:
            draw_arrow(ax, (x + box_width, y + 0.6), (x + 2.2, y + 0.6))
    
    # Week labels below
    weeks = ['Week 1-2', 'Week 1-2', 'Week 3-4', 'Week 5-6', 'Week 5-6', 'Week 7-10']
    for i, week in enumerate(weeks):
        x = start_x + i * 2.2 + box_width/2
        ax.text(x, 2.5, week, ha='center', fontsize=8, style='italic')
    
    # Deliverables below
    deliverables = ['Asset\nInventory', 'Updated\nDocs', 'Smells\nIdentified', 'Refactoring\nPlan', 'New\nSchema', 'Flask\nWeb App']
    for i, deliv in enumerate(deliverables):
        x = start_x + i * 2.2 + box_width/2
        ax.text(x, 1.8, deliv, ha='center', fontsize=7, color=COLORS['dark_gray'])
    
    # Legend
    ax.text(0.5, 5.2, 'Analysis Phase', fontsize=9, color=COLORS['ui'], fontweight='bold')
    ax.text(4, 5.2, 'Restructuring Phase', fontsize=9, color=COLORS['business'], fontweight='bold')
    ax.text(8, 5.2, 'Implementation Phase', fontsize=9, color=COLORS['new'], fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/reengineering_flow.png', dpi=150, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("Created: reengineering_flow.png")


# =============================================================================
# 8. Testing Pyramid
# =============================================================================
def create_testing_pyramid():
    fig, ax = plt.subplots(1, 1, figsize=(10, 8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.axis('off')
    ax.set_title('Testing Pyramid', fontsize=14, fontweight='bold', pad=20)
    
    # Pyramid layers (bottom to top)
    # Unit Tests (base)
    triangle_unit = plt.Polygon([(1, 1), (9, 1), (7.5, 3), (2.5, 3)], 
                                 facecolor=COLORS['new'], edgecolor=COLORS['dark_gray'], linewidth=2)
    ax.add_patch(triangle_unit)
    ax.text(5, 2, 'Unit Tests\n60%', ha='center', va='center', fontsize=11, fontweight='bold', color='white')
    
    # Integration Tests (middle)
    triangle_int = plt.Polygon([(2.5, 3), (7.5, 3), (6.5, 5), (3.5, 5)], 
                                facecolor=COLORS['business'], edgecolor=COLORS['dark_gray'], linewidth=2)
    ax.add_patch(triangle_int)
    ax.text(5, 4, 'Integration\nTests 30%', ha='center', va='center', fontsize=10, fontweight='bold', color='white')
    
    # E2E Tests (top)
    triangle_e2e = plt.Polygon([(3.5, 5), (6.5, 5), (5, 7)], 
                                facecolor=COLORS['ui'], edgecolor=COLORS['dark_gray'], linewidth=2)
    ax.add_patch(triangle_e2e)
    ax.text(5, 5.8, 'E2E\n10%', ha='center', va='center', fontsize=9, fontweight='bold', color='white')
    
    # Annotations
    ax.text(9.5, 2, 'test_models.py\ntest_services.py\n• Fast execution\n• High coverage', fontsize=8, va='center')
    ax.text(9.5, 4, 'test_routes.py\n• HTTP testing\n• DB integration', fontsize=8, va='center')
    ax.text(9.5, 5.8, 'Manual/Selenium\n• Full workflow', fontsize=8, va='center')
    
    # Stats
    ax.text(5, 0.3, 'Total: 37 tests | Coverage: 89% | Duration: 2.45s', 
            ha='center', fontsize=10, fontweight='bold', color=COLORS['dark_gray'])
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/testing_pyramid.png', dpi=150, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("Created: testing_pyramid.png")


# =============================================================================
# 9. Dual Architecture Diagram
# =============================================================================
def create_dual_architecture():
    # Same as architecture_comparison but with different title
    create_architecture_comparison()
    # Copy the file with new name
    import shutil
    shutil.copy(f'{OUTPUT_DIR}/architecture_comparison.png', f'{OUTPUT_DIR}/dual_architecture.png')
    print("Created: dual_architecture.png")


# =============================================================================
# 10. Data Model Evolution
# =============================================================================
def create_data_model_evolution():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 8))
    
    for ax in [ax1, ax2]:
        ax.set_xlim(0, 6)
        ax.set_ylim(0, 8)
        ax.axis('off')
    
    # BEFORE - Text Files
    ax1.set_title('Legacy Data Model (.txt Files)', fontsize=12, fontweight='bold', color=COLORS['legacy'], pad=15)
    
    def draw_file(ax, x, y, name, content):
        draw_box(ax, x, y, 5, 1.5, '', COLORS['light_gray'])
        ax.text(x+2.5, y+1.3, name, ha='center', fontsize=9, fontweight='bold', color=COLORS['legacy'])
        ax.text(x+0.1, y+0.8, content, fontsize=7, family='monospace', color=COLORS['dark_gray'])
    
    draw_file(ax1, 0.5, 6, 'employeeDatabase.txt', '110001 Admin Harry Larry 1\n110002 Cashier John Smith pass')
    draw_file(ax1, 0.5, 4, 'itemDatabase.txt', '1000 Potato 1.0 249\n1001 Tomato 2.5 150')
    draw_file(ax1, 0.5, 2, 'userDatabase.txt', '6096515668 1000,6/30/09,true 1022...')
    
    ax1.text(3, 1.5, '[X] No normalization\n[X] Plaintext passwords\n[X] Repeating groups', 
             ha='center', fontsize=9, color=COLORS['legacy'])
    
    # Arrow
    fig.text(0.5, 0.5, '→', fontsize=40, ha='center', va='center', color=COLORS['new'])
    
    # AFTER - Normalized Tables
    ax2.set_title('Reengineered Data Model (SQL)', fontsize=12, fontweight='bold', color=COLORS['new'], pad=15)
    
    def draw_table(ax, x, y, name, fields):
        height = 0.3 + len(fields)*0.25
        draw_box(ax, x, y, 2.3, height, '', COLORS['light_gray'])
        ax.text(x+1.15, y+height-0.2, name, ha='center', fontsize=8, fontweight='bold', color=COLORS['database'])
        for i, field in enumerate(fields):
            ax.text(x+0.1, y+height-0.4-i*0.25, field, fontsize=6, color=COLORS['dark_gray'])
    
    draw_table(ax2, 0.3, 5.5, 'employees', ['id PK', 'employee_id', 'first_name', 'password_hash', 'role'])
    draw_table(ax2, 3.2, 5.5, 'items', ['id PK', 'item_code', 'name', 'price', 'quantity', 'is_rentable'])
    draw_table(ax2, 0.3, 3, 'rentals', ['id PK', 'rental_id', 'customer_phone', 'employee_id FK'])
    draw_table(ax2, 3.2, 3, 'rental_items', ['id PK', 'rental_id FK', 'item_id FK', 'is_returned'])
    draw_table(ax2, 1.5, 0.8, 'activity_logs', ['id PK', 'employee_id FK', 'action', 'timestamp'])
    
    # Relationship arrows
    draw_arrow(ax2, (2.6, 6), (3.2, 6))
    draw_arrow(ax2, (1.5, 5.5), (1.5, 4.5))
    draw_arrow(ax2, (4.4, 5.5), (4.4, 4.5))
    
    ax2.text(3, 0.3, '[OK] 3NF Normalized\n[OK] Foreign Keys\n[OK] Hashed Passwords', 
             ha='center', fontsize=9, color=COLORS['new'])
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/data_model_evolution.png', dpi=150, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("Created: data_model_evolution.png")


# =============================================================================
# 11. Refactoring Overview
# =============================================================================
def create_refactoring_overview():
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.axis('off')
    ax.set_title('Refactoring Types Overview', fontsize=14, fontweight='bold', pad=20)
    
    # Three columns for three types
    # Structural
    draw_box(ax, 0.5, 5.5, 3.5, 1, 'Structural\nRefactorings', COLORS['ui'])
    struct_items = ['AF-2: Repository Pattern', 'SA-1: File → Repository', 'HA-1: Thin Controller']
    for i, item in enumerate(struct_items):
        draw_box(ax, 0.7, 4.5 - i*0.9, 3.1, 0.7, item, COLORS['light_gray'], COLORS['dark_gray'], 8)
    
    # Behavioral
    draw_box(ax, 4.25, 5.5, 3.5, 1, 'Behavioral\nRefactorings', COLORS['business'])
    behav_items = ['AF-1: Login Workflow', 'SA-2: Late Fee Service', 'HA-2: Atomic Transactions']
    for i, item in enumerate(behav_items):
        draw_box(ax, 4.45, 4.5 - i*0.9, 3.1, 0.7, item, COLORS['light_gray'], COLORS['dark_gray'], 8)
    
    # Data/Security
    draw_box(ax, 8, 5.5, 3.5, 1, 'Data/Security\nRefactorings', COLORS['new'])
    data_items = ['AF-3: Data Normalization', 'SA-3: Unified Item Model', 'HA-3: Secure Auth']
    for i, item in enumerate(data_items):
        draw_box(ax, 8.2, 4.5 - i*0.9, 3.1, 0.7, item, COLORS['light_gray'], COLORS['dark_gray'], 8)
    
    # Team members at bottom
    ax.text(2.25, 1, 'Abdul Faheem\nAF-1, AF-2, AF-3', ha='center', fontsize=9, 
            bbox=dict(boxstyle='round', facecolor=COLORS['light_gray']))
    ax.text(6, 1, 'Sheryar Ali\nSA-1, SA-2, SA-3', ha='center', fontsize=9,
            bbox=dict(boxstyle='round', facecolor=COLORS['light_gray']))
    ax.text(9.75, 1, 'Husnain Akram\nHA-1, HA-2, HA-3', ha='center', fontsize=9,
            bbox=dict(boxstyle='round', facecolor=COLORS['light_gray']))
    
    # Total
    ax.text(6, 0.2, 'Total: 9 Major Refactorings (3 per team member)', ha='center', 
            fontsize=10, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/refactoring_overview.png', dpi=150, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print("Created: refactoring_overview.png")


# =============================================================================
# Main execution
# =============================================================================
if __name__ == '__main__':
    print("Generating diagrams for Software Reengineering Report...")
    print("=" * 50)
    
    create_legacy_system_overview()
    create_legacy_dependency_map()
    create_legacy_class_diagram()
    create_code_restructuring()
    create_database_erd()
    create_architecture_comparison()
    create_reengineering_flow()
    create_testing_pyramid()
    create_dual_architecture()
    create_data_model_evolution()
    create_refactoring_overview()
    
    print("=" * 50)
    print(f"All diagrams saved to: {OUTPUT_DIR}/")
    print("Done!")
