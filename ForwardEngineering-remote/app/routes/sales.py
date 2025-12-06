"""
Sales Routes
=============
Handles sales transaction views and API endpoints.
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from flask_login import login_required, current_user
from app.services.sales_service import SalesService
from app.services.inventory_service import InventoryService

sales_bp = Blueprint('sales', __name__)


@sales_bp.route('/')
@login_required
def new_sale():
    """Start new sale transaction."""
    # Check for existing sale in session
    sale_id = session.get('current_sale_id')
    sale = None
    
    if sale_id:
        sale = SalesService.get_sale(sale_id)
        if sale and sale.status != 'in_progress':
            sale = None
            session.pop('current_sale_id', None)
    
    return render_template('sales/new_sale.html', sale=sale)


@sales_bp.route('/start', methods=['POST'])
@login_required
def start_sale():
    """Create new sale transaction."""
    sale = SalesService.create_sale(current_user.id)
    session['current_sale_id'] = sale.id
    
    return jsonify({
        'success': True,
        'sale': sale.to_dict()
    })


@sales_bp.route('/add-item', methods=['POST'])
@login_required
def add_item():
    """Add item to current sale."""
    sale_id = session.get('current_sale_id')
    if not sale_id:
        return jsonify({'success': False, 'message': 'No active sale'}), 400
    
    data = request.get_json()
    item_code = data.get('item_code', '').strip()
    quantity = data.get('quantity', 1)
    
    try:
        quantity = int(quantity)
    except ValueError:
        return jsonify({'success': False, 'message': 'Invalid quantity'}), 400
    
    success, message, sale_item = SalesService.add_item_to_sale(sale_id, item_code, quantity)
    
    if success:
        sale = SalesService.get_sale(sale_id)
        return jsonify({
            'success': True,
            'message': message,
            'sale': sale.to_dict()
        })
    
    return jsonify({'success': False, 'message': message}), 400


@sales_bp.route('/remove-item', methods=['POST'])
@login_required
def remove_item():
    """Remove item from current sale."""
    sale_id = session.get('current_sale_id')
    if not sale_id:
        return jsonify({'success': False, 'message': 'No active sale'}), 400
    
    data = request.get_json()
    item_id = data.get('item_id')
    
    success, message = SalesService.remove_item_from_sale(sale_id, item_id)
    
    if success:
        sale = SalesService.get_sale(sale_id)
        return jsonify({
            'success': True,
            'message': message,
            'sale': sale.to_dict()
        })
    
    return jsonify({'success': False, 'message': message}), 400


@sales_bp.route('/complete', methods=['POST'])
@login_required
def complete_sale():
    """Complete the sale transaction."""
    sale_id = session.get('current_sale_id')
    if not sale_id:
        return jsonify({'success': False, 'message': 'No active sale'}), 400
    
    data = request.get_json()
    amount_paid = data.get('amount_paid', 0)
    payment_method = data.get('payment_method', 'Cash')
    
    try:
        amount_paid = float(amount_paid)
    except ValueError:
        return jsonify({'success': False, 'message': 'Invalid payment amount'}), 400
    
    success, message, sale = SalesService.complete_sale(sale_id, amount_paid, payment_method)
    
    if success:
        session.pop('current_sale_id', None)
        return jsonify({
            'success': True,
            'message': message,
            'sale': sale.to_dict()
        })
    
    return jsonify({'success': False, 'message': message}), 400


@sales_bp.route('/cancel', methods=['POST'])
@login_required
def cancel_sale():
    """Cancel current sale."""
    sale_id = session.get('current_sale_id')
    if not sale_id:
        return jsonify({'success': False, 'message': 'No active sale'}), 400
    
    success, message = SalesService.cancel_sale(sale_id, current_user.id)
    
    if success:
        session.pop('current_sale_id', None)
        return jsonify({'success': True, 'message': message})
    
    return jsonify({'success': False, 'message': message}), 400


@sales_bp.route('/receipt/<int:sale_id>')
@login_required
def view_receipt(sale_id):
    """View sale receipt."""
    sale = SalesService.get_sale(sale_id)
    if not sale:
        flash('Sale not found.', 'error')
        return redirect(url_for('sales.new_sale'))
    
    return render_template('sales/receipt.html', sale=sale)


@sales_bp.route('/history')
@login_required
def sales_history():
    """View sales history."""
    sales = SalesService.get_sales_by_employee(current_user.id)
    return render_template('sales/history.html', sales=sales)

