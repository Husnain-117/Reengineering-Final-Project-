"""
Activity Log Model
===================
Represents audit trail for system activities.

Legacy System Issues Addressed:
- employeeLogfile.txt was append-only text → Proper database table
- Limited information → Comprehensive activity tracking
- No structured querying → Full SQL query support

This model enables:
- Security auditing
- Activity monitoring
- Compliance reporting
"""

from datetime import datetime
from app import db


class ActivityLog(db.Model):
    """
    Activity log model for audit trail.
    
    Tracks all significant activities in the system:
    - Login/Logout events
    - Sales transactions
    - Inventory changes
    - Employee management actions
    
    Attributes:
        id: Primary key
        employee_id: Who performed the action
        action: Type of action (login, logout, sale, etc.)
        entity_type: What was affected (sale, rental, item, employee)
        entity_id: ID of affected entity
        description: Human-readable description
        ip_address: Client IP for security
        created_at: When action occurred
    """
    
    __tablename__ = 'activity_logs'
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True)
    
    # Who performed the action
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=True)
    
    # Action details
    action = db.Column(db.String(50), nullable=False, index=True)  # login, logout, sale, rental, etc.
    entity_type = db.Column(db.String(50), nullable=True)  # sale, rental, item, employee
    entity_id = db.Column(db.Integer, nullable=True)
    
    # Description
    description = db.Column(db.Text, nullable=True)
    
    # Additional context
    ip_address = db.Column(db.String(45), nullable=True)  # IPv6 compatible
    user_agent = db.Column(db.String(256), nullable=True)
    
    # Timestamp
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    # Action type constants
    ACTION_LOGIN = 'login'
    ACTION_LOGOUT = 'logout'
    ACTION_SALE = 'sale'
    ACTION_RENTAL = 'rental'
    ACTION_RETURN = 'return'
    ACTION_ITEM_CREATE = 'item_create'
    ACTION_ITEM_UPDATE = 'item_update'
    ACTION_ITEM_DELETE = 'item_delete'
    ACTION_EMPLOYEE_CREATE = 'employee_create'
    ACTION_EMPLOYEE_UPDATE = 'employee_update'
    ACTION_EMPLOYEE_DELETE = 'employee_delete'
    
    def __init__(self, action, employee_id=None, entity_type=None, entity_id=None, 
                 description=None, ip_address=None, user_agent=None):
        """Initialize activity log entry."""
        self.action = action
        self.employee_id = employee_id
        self.entity_type = entity_type
        self.entity_id = entity_id
        self.description = description
        self.ip_address = ip_address
        self.user_agent = user_agent
    
    @classmethod
    def log(cls, action, employee_id=None, entity_type=None, entity_id=None, 
            description=None, ip_address=None, user_agent=None):
        """
        Create and save a log entry.
        
        Factory method for convenient logging.
        """
        log_entry = cls(
            action=action,
            employee_id=employee_id,
            entity_type=entity_type,
            entity_id=entity_id,
            description=description,
            ip_address=ip_address,
            user_agent=user_agent
        )
        db.session.add(log_entry)
        db.session.commit()
        return log_entry
    
    def to_dict(self):
        """Serialize activity log to dictionary."""
        return {
            'id': self.id,
            'employee_id': self.employee_id,
            'employee_name': self.employee.full_name if self.employee else 'System',
            'action': self.action,
            'entity_type': self.entity_type,
            'entity_id': self.entity_id,
            'description': self.description,
            'ip_address': self.ip_address,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<ActivityLog {self.action} by Employee {self.employee_id} at {self.created_at}>'

