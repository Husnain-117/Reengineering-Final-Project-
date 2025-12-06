"""
POS System Application Factory
===============================
Implements the application factory pattern for Flask application creation.
This enables better testing, multiple instances, and cleaner configuration.

Architecture: Layered Architecture with Repository Pattern
- Presentation Layer: Routes/Views (Flask Blueprints)
- Business Logic Layer: Services
- Data Access Layer: Models with SQLAlchemy ORM
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from config import config

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

# Configure login manager
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'


def create_app(config_name='default'):
    """
    Application Factory Function
    
    Creates and configures the Flask application instance.
    Follows the Factory Pattern for flexible app creation.
    
    Args:
        config_name: Configuration to use (development/testing/production)
    
    Returns:
        Configured Flask application instance
    """
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    
    # Register blueprints (modular routing)
    from app.routes.auth import auth_bp
    from app.routes.main import main_bp
    from app.routes.inventory import inventory_bp
    from app.routes.sales import sales_bp
    from app.routes.employees import employees_bp
    from app.routes.rentals import rentals_bp
    from app.routes.reports import reports_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(inventory_bp, url_prefix='/inventory')
    app.register_blueprint(sales_bp, url_prefix='/sales')
    app.register_blueprint(employees_bp, url_prefix='/employees')
    app.register_blueprint(rentals_bp, url_prefix='/rentals')
    app.register_blueprint(reports_bp, url_prefix='/reports')
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app


@login_manager.user_loader
def load_user(user_id):
    """Load user for Flask-Login session management."""
    from app.models.employee import Employee
    return Employee.query.get(int(user_id))

