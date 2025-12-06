"""
Rental Routes
==============
Handles rental transaction views and returns.
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from flask_login import login_required, current_user
from app.services.rental_service import RentalService
from app.services.inventory_service import InventoryService

rentals_bp = Blueprint('rentals', __name__)


@rentals_bp.route('/')
@login_required
def rental_dashboard():
    """Rental management dashboard."""
    active_rentals = RentalService.get_active_rentals()
    overdue_rentals = RentalService.get_overdue_rentals()
    
    return render_template('rentals/dashboard.html',
                         active_rentals=active_rentals,
                         overdue_rentals=overdue_rentals)


@rentals_bp.route('/new', methods=['GET', 'POST'])
@login_required
def new_rental():
    """Create new rental."""
    if request.method == 'POST':
        customer_phone = request.form.get('customer_phone', '').strip()
        customer_name = request.form.get('customer_name', '').strip()
        
        if not customer_phone:
            flash('Customer phone is required.', 'error')
            return render_template('rentals/new_rental.html')
        
        rental = RentalService.create_rental(
            customer_phone=customer_phone,
            employee_id=current_user.id,
            customer_name=customer_name if customer_name else None
        )
        
        session['current_rental_id'] = rental.id
        return redirect(url_for('rentals.add_items'))
    
    return render_template('rentals/new_rental.html')


@rentals_bp.route('/add-items')
@login_required
def add_items():
    """Add items to rental."""
    rental_id = session.get('current_rental_id')
    if not rental_id:
        flash('No active rental. Please start a new rental.', 'error')
        return redirect(url_for('rentals.new_rental'))
    
    rental = RentalService.get_rental(rental_id)
    if not rental:
        session.pop('current_rental_id', None)
        flash('Rental not found.', 'error')
        return redirect(url_for('rentals.new_rental'))
    
    # Get rentable items
    items = InventoryService.get_all_items()
    rentable_items = [i for i in items if i.is_rentable and i.quantity > 0]
    
    return render_template('rentals/add_items.html',
                         rental=rental,
                         items=rentable_items)


@rentals_bp.route('/api/add-item', methods=['POST'])
@login_required
def api_add_item():
    """API to add item to rental."""
    rental_id = session.get('current_rental_id')
    if not rental_id:
        return jsonify({'success': False, 'message': 'No active rental'}), 400
    
    data = request.get_json()
    item_code = data.get('item_code', '').strip()
    quantity = data.get('quantity', 1)
    
    try:
        quantity = int(quantity)
    except ValueError:
        return jsonify({'success': False, 'message': 'Invalid quantity'}), 400
    
    success, message, rental_item = RentalService.add_item_to_rental(
        rental_id, item_code, quantity
    )
    
    if success:
        rental = RentalService.get_rental(rental_id)
        return jsonify({
            'success': True,
            'message': message,
            'rental': rental.to_dict()
        })
    
    return jsonify({'success': False, 'message': message}), 400


@rentals_bp.route('/complete', methods=['POST'])
@login_required
def complete_rental():
    """Complete rental transaction."""
    rental_id = session.get('current_rental_id')
    if not rental_id:
        flash('No active rental.', 'error')
        return redirect(url_for('rentals.new_rental'))
    
    success, message, rental = RentalService.complete_rental(rental_id)
    
    if success:
        session.pop('current_rental_id', None)
        flash(message, 'success')
        return redirect(url_for('rentals.view_rental', rental_id=rental.id))
    
    flash(message, 'error')
    return redirect(url_for('rentals.add_items'))


@rentals_bp.route('/<int:rental_id>')
@login_required
def view_rental(rental_id):
    """View rental details."""
    rental = RentalService.get_rental(rental_id)
    if not rental:
        flash('Rental not found.', 'error')
        return redirect(url_for('rentals.rental_dashboard'))
    
    return render_template('rentals/view.html', rental=rental)


@rentals_bp.route('/<int:rental_id>/return', methods=['GET', 'POST'])
@login_required
def process_return(rental_id):
    """Process rental return."""
    rental = RentalService.get_rental(rental_id)
    if not rental:
        flash('Rental not found.', 'error')
        return redirect(url_for('rentals.rental_dashboard'))
    
    if rental.status == 'returned':
        flash('Rental already returned.', 'info')
        return redirect(url_for('rentals.view_rental', rental_id=rental_id))
    
    if request.method == 'POST':
        # Get items to return (if partial return)
        item_ids = request.form.getlist('item_ids')
        item_ids = [int(i) for i in item_ids] if item_ids else None
        
        success, message = RentalService.process_return(rental_id, item_ids)
        
        if success:
            flash(message, 'success')
        else:
            flash(message, 'error')
        
        return redirect(url_for('rentals.view_rental', rental_id=rental_id))
    
    return render_template('rentals/return.html', rental=rental)


@rentals_bp.route('/search')
@login_required
def search_rentals():
    """Search rentals by phone."""
    phone = request.args.get('phone', '').strip()
    rentals = []
    
    if phone:
        rentals = RentalService.get_rentals_by_phone(phone)
    
    return render_template('rentals/search.html',
                         phone=phone,
                         rentals=rentals)

