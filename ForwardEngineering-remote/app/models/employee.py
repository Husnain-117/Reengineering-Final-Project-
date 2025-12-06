"""
Employee Model
===============
Represents employees/users of the POS system.

Legacy System Issues Addressed:
- Plain text passwords → Secure hashed passwords (bcrypt)
- Space-delimited file → Proper database table
- No audit trail → Created/updated timestamps
- Name stored as single field → Separated first/last name

Database Normalization: 
- 1NF: Atomic values (no composite names)
- 2NF: No partial dependencies
- 3NF: No transitive dependencies
"""

from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db


class Employee(UserMixin, db.Model):
    """
    Employee model with proper authentication support.
    
    Attributes:
        id: Primary key (auto-increment)
        employee_id: Business identifier (like legacy username - 110001)
        first_name: Employee's first name
        last_name: Employee's last name
        role: Either 'Admin' or 'Cashier'
        password_hash: Securely hashed password
        is_active: Soft delete flag
        created_at: Account creation timestamp
        updated_at: Last modification timestamp
    """
    
    __tablename__ = 'employees'
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True)
    
    # Business identifier (maps to legacy 'username' like 110001)
    employee_id = db.Column(db.String(20), unique=True, nullable=False, index=True)
    
    # Personal information (normalized from single 'name' field)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    
    # Role-based access control
    role = db.Column(db.String(20), nullable=False, default='Cashier')
    
    # Security - hashed password (vs plain text in legacy)
    password_hash = db.Column(db.String(256), nullable=False)
    
    # Account status
    is_active = db.Column(db.Boolean, default=True)
    
    # Audit timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    sales = db.relationship('Sale', backref='cashier', lazy='dynamic')
    rentals = db.relationship('Rental', backref='processed_by', lazy='dynamic')
    activity_logs = db.relationship('ActivityLog', backref='employee', lazy='dynamic')
    
    def __init__(self, employee_id, first_name, last_name, password, role='Cashier'):
        """Initialize employee with secure password hashing."""
        self.employee_id = employee_id
        self.first_name = first_name
        self.last_name = last_name
        self.role = role
        self.set_password(password)
    
    def set_password(self, password):
        """Hash and set the password securely."""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify password against stored hash."""
        return check_password_hash(self.password_hash, password)
    
    @property
    def full_name(self):
        """Return combined first and last name."""
        return f"{self.first_name} {self.last_name}"
    
    @property
    def is_admin(self):
        """Check if employee has admin privileges."""
        return self.role == 'Admin'
    
    def to_dict(self):
        """Serialize employee to dictionary (for API responses)."""
        return {
            'id': self.id,
            'employee_id': self.employee_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'full_name': self.full_name,
            'role': self.role,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<Employee {self.employee_id}: {self.full_name} ({self.role})>'

