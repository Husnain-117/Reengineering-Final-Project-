"""
Inventory Routes
=================
Handles inventory management views and API endpoints.
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app.services.inventory_service import InventoryService

inventory_bp = Blueprint('inventory', __name__)


@inventory_bp.route('/')
@login_required
def list_items():
    """List all inventory items."""
    search = request.args.get('search', '')
    category = request.args.get('category', '')
    
    if search:
        items = InventoryService.search_items(search, category if category else None)
    else:
        items = InventoryService.get_all_items()
    
    categories = InventoryService.get_categories()
    
    return render_template('inventory/list.html',
                         items=items,
                         categories=categories,
                         search=search,
                         selected_category=category)


@inventory_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_item():
    """Add new inventory item."""
    if not current_user.is_admin:
        flash('Only administrators can add items.', 'error')
        return redirect(url_for('inventory.list_items'))
    
    if request.method == 'POST':
        item_code = request.form.get('item_code', '').strip()
        name = request.form.get('name', '').strip()
        price = request.form.get('price', 0)
        quantity = request.form.get('quantity', 0)
        category = request.form.get('category', 'General')
        is_rentable = request.form.get('is_rentable') == 'on'
        
        try:
            price = float(price)
            quantity = int(quantity)
        except ValueError:
            flash('Invalid price or quantity.', 'error')
            return render_template('inventory/add.html')
        
        success, item, message = InventoryService.create_item(
            item_code=item_code,
            name=name,
            price=price,
            quantity=quantity,
            category=category,
            is_rentable=is_rentable,
            employee_id=current_user.id
        )
        
        if success:
            flash(message, 'success')
            return redirect(url_for('inventory.list_items'))
        else:
            flash(message, 'error')
    
    return render_template('inventory/add.html')


@inventory_bp.route('/<int:item_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_item(item_id):
    """Edit inventory item."""
    if not current_user.is_admin:
        flash('Only administrators can edit items.', 'error')
        return redirect(url_for('inventory.list_items'))
    
    item = InventoryService.get_item_by_id(item_id)
    if not item:
        flash('Item not found.', 'error')
        return redirect(url_for('inventory.list_items'))
    
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        price = request.form.get('price', 0)
        quantity = request.form.get('quantity', 0)
        category = request.form.get('category', 'General')
        min_stock = request.form.get('min_stock_level', 10)
        is_rentable = request.form.get('is_rentable') == 'on'
        
        try:
            price = float(price)
            quantity = int(quantity)
            min_stock = int(min_stock)
        except ValueError:
            flash('Invalid numeric values.', 'error')
            return render_template('inventory/edit.html', item=item)
        
        success, item, message = InventoryService.update_item(
            item_id,
            employee_id=current_user.id,
            name=name,
            price=price,
            quantity=quantity,
            category=category,
            min_stock_level=min_stock,
            is_rentable=is_rentable
        )
        
        if success:
            flash(message, 'success')
            return redirect(url_for('inventory.list_items'))
        else:
            flash(message, 'error')
    
    return render_template('inventory/edit.html', item=item)


@inventory_bp.route('/<int:item_id>/delete', methods=['POST'])
@login_required
def delete_item(item_id):
    """Delete inventory item."""
    if not current_user.is_admin:
        flash('Only administrators can delete items.', 'error')
        return redirect(url_for('inventory.list_items'))
    
    success, message = InventoryService.delete_item(item_id, current_user.id)
    
    if success:
        flash(message, 'success')
    else:
        flash(message, 'error')
    
    return redirect(url_for('inventory.list_items'))


@inventory_bp.route('/low-stock')
@login_required
def low_stock():
    """View low stock items."""
    items = InventoryService.get_low_stock_items()
    return render_template('inventory/low_stock.html', items=items)


# API Endpoints for AJAX operations
@inventory_bp.route('/api/search')
@login_required
def api_search():
    """API endpoint for item search."""
    query = request.args.get('q', '')
    items = InventoryService.search_items(query)
    return jsonify([item.to_dict() for item in items])


@inventory_bp.route('/api/<item_code>')
@login_required
def api_get_item(item_code):
    """API endpoint to get item by code."""
    item = InventoryService.get_item_by_code(item_code)
    if item:
        return jsonify(item.to_dict())
    return jsonify({'error': 'Item not found'}), 404

