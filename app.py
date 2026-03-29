from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from flask_babel import Babel, gettext, ngettext, lazy_gettext
import mysql.connector
from mysql.connector import Error
from datetime import datetime
import os
from dotenv import load_dotenv
from barcode import Code128
from barcode.writer import ImageWriter
from io import BytesIO
import base64

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = 'inventory-management-secret-key-2024'
app.config['BABEL_DEFAULT_LOCALE'] = 'en'
app.config['BABEL_DEFAULT_TIMEZONE'] = 'UTC'
app.config['BABEL_TRANSLATION_DIRECTORIES'] = 'translations'
app.config['LANGUAGES'] = {
    'en': 'English',
    'hi': 'हिंदी',
    'mr': 'मराठी'
}

def get_locale():
    """Select the best language for the user"""
    # First, try to get language from URL parameter
    if request.args.get('lang'):
        return request.args.get('lang')
    
    # Then try to get from cookie
    if request.cookies.get('lang'):
        return request.cookies.get('lang')
    
    # Try to match browser language preferences
    return request.accept_languages.best_match(app.config['LANGUAGES'].keys()) or 'en'

babel = Babel(app, locale_selector=get_locale)

@app.context_processor
def inject_languages():
    """Make language configuration available to all templates"""
    return {
        'languages': app.config['LANGUAGES'],
        'current_language': get_locale()
    }

# --- MYSQL CONFIGURATION ---
db_config = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', 'Urus@0657'),
    'database': os.getenv('DB_NAME', 'inventory_management'),
    'port': int(os.getenv('DB_PORT', 3306)),
    'ssl_disabled': False,
    'autocommit': True
}

BARCODE_DIR = 'static/barcodes'

def get_db_connection():
    """Create MySQL database connection"""
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def generate_barcode(sku):
    """Generate barcode as base64 PNG (no file writing - works on Vercel)"""
    try:
        if not sku or sku.strip() == '':
            print("Error: SKU cannot be empty")
            return None
        
        print(f"Generating barcode for SKU: {sku}")
        
        # Generate barcode as PNG in memory (no file system access needed)
        buffer = BytesIO()
        code = Code128(sku, writer=ImageWriter())
        code.write(buffer, options={'write_text': True})
        buffer.seek(0)
        
        # Convert to base64
        barcode_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        barcode_data = f'data:image/png;base64,{barcode_base64}'
        
        print(f"✓ Barcode generated successfully for SKU: {sku}")
        return barcode_data
            
    except Exception as e:
        print(f"Error generating barcode for SKU {sku}: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return None

# ==================== ROUTES ====================

@app.route('/set_language/<language>')
def set_language(language):
    """Set the user's language preference"""
    if language in app.config['LANGUAGES']:
        response = redirect(request.referrer or url_for('admin_dashboard'))
        response.set_cookie('lang', language, max_age=31536000)  # 1 year
        return response
    return redirect(request.referrer or url_for('admin_dashboard'))

@app.route('/')
def index():
    return redirect(url_for('admin_dashboard'))

@app.route('/admin')
def admin_dashboard():
    """Admin Dashboard - Inventory Management & Reports"""
    return render_template('admin_dashboard.html')

@app.route('/employee')
def employee_dashboard():
    """Employee Dashboard - Daily Operations"""
    return render_template('employee_dashboard.html')

@app.route('/add_category', methods=['POST'])
def add_category():
    category_name = request.form.get('category_name', '').strip()
    if not category_name:
        return redirect(url_for('view_products'))
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute('SELECT id FROM category_table WHERE LOWER(name) = LOWER(%s)', (category_name,))
        if cursor.fetchone():
            return redirect(url_for('view_products'))
        
        created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute('INSERT INTO category_table (name, created_at) VALUES (%s, %s)', (category_name, created_at))
        conn.commit()
    finally:
        cursor.close()
        conn.close()
    return redirect(url_for('view_products'))

@app.route('/favicon.ico')
def favicon():
    return '', 204

@app.route('/products')
def view_products():
    conn = get_db_connection()
    if not conn:
        return "Error: Cannot connect to database. Please check your database credentials and server configuration.", 500
    
    try:
        cursor = conn.cursor(dictionary=True)
    
        category_id = request.args.get('category_id')
        search_query = request.args.get('search', '').strip()
        
        base_query = '''
            SELECT p.*, c.name as category_name 
            FROM product_table p
            LEFT JOIN category_table c ON p.category_id = c.id
            WHERE 1=1
        '''
        params = []
        
        if category_id:
            base_query += ' AND p.category_id = %s'
            params.append(category_id)
        
        if search_query:
            base_query += ' AND LOWER(p.name) LIKE LOWER(%s)'
            params.append(f'%{search_query}%')
        
        base_query += ' ORDER BY p.id DESC'
        
        cursor.execute(base_query, params)
        products = cursor.fetchall()
        
        cursor.execute('SELECT * FROM category_table ORDER BY name')
        categories = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return render_template('products.html', products=products, categories=categories, 
                               selected_category=category_id, search_query=search_query)
    except Exception as e:
        conn.close()
        return f"Database Error: {str(e)}", 500

@app.route('/products/add', methods=['POST'])
def add_product():
    sku = request.form.get('sku', '').strip()
    name = request.form.get('name', '').strip()
    category_id = request.form.get('category_id') or None
    price = float(request.form.get('price', 0))
    quantity = int(request.form.get('quantity', 0))
    shelf_number = request.form.get('shelf_number', '').strip()
    reorder_level = int(request.form.get('reorder_level', 0))
    
    # Generate barcode
    barcode_path = generate_barcode(sku)
    if not barcode_path:
        flash(gettext(f'Error: Failed to generate barcode for SKU "{sku}". Check the logs for details.'), 'error')
        return redirect(url_for('view_products'))
    
    created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    conn = get_db_connection()
    if not conn:
        flash(gettext('Error: Cannot connect to database'), 'error')
        return redirect(url_for('view_products'))
    
    cursor = conn.cursor()
    
    try:
        cursor.execute('INSERT INTO product_table (sku, name, category_id, price, quantity, shelf_number, reorder_level, barcode_path, created_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)', 
                       (sku, name, category_id, price, quantity, shelf_number, reorder_level, barcode_path, created_at))
        conn.commit()
        flash(gettext(f'Product "{name}" added successfully with barcode.'), 'success')
    except Error as e:
        conn.rollback()
        flash(gettext(f'Database error: {e}'), 'error')
    finally:
        cursor.close()
        conn.close()
    return redirect(url_for('view_products'))

@app.route('/products/edit/<int:id>', methods=['POST'])
def edit_product(id):
    sku = request.form['sku']
    name = request.form['name']
    category_id = request.form.get('category_id') or None
    price = float(request.form['price'])
    quantity = int(request.form['quantity'])
    shelf_number = request.form['shelf_number']
    reorder_level = int(request.form['reorder_level'])
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE product_table 
        SET sku = %s, name = %s, category_id = %s, price = %s, quantity = %s, 
            shelf_number = %s, reorder_level = %s
        WHERE id = %s
    ''', (sku, name, category_id, price, quantity, shelf_number, reorder_level, id))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('view_products'))

@app.route('/products/delete/<int:id>', methods=['POST'])
def delete_product(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM product_table WHERE id = %s', (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('view_products'))

@app.route('/products/get/<int:id>')
def get_product(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM product_table WHERE id = %s', (id,))
    product = cursor.fetchone()
    cursor.close()
    conn.close()
    return jsonify(product) if product else (jsonify({'error': 'Not found'}), 404)

@app.route('/scan')
def scan():
    return render_template('scan.html')

@app.route('/returns')
def returns():
    return render_template('returns.html')

@app.route('/stock-history')
def stock_history():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # We JOIN with product_table and category_table to get all the info
    cursor.execute('''
        SELECT sm.*, p.sku, p.name, c.name as category_name
        FROM stock_movement sm
        JOIN product_table p ON sm.product_id = p.id
        LEFT JOIN category_table c ON p.category_id = c.id
        ORDER BY sm.timestamp DESC
    ''')
    movements = cursor.fetchall()
    conn.close()
    
    return render_template('stock_history.html', movements=movements)

# --- FIX FOR BUY ---
@app.route('/products/buy/<int:id>', methods=['POST'])
def buy_product(id):
    quantity = int(request.form.get('buy_quantity', 0))
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 1. Update Product Quantity
    cursor.execute('UPDATE product_table SET quantity = quantity + %s WHERE id = %s', (quantity, id))
    
    # 2. Log the Movement (This is what fixes your empty page!)
    cursor.execute('INSERT INTO stock_movement (product_id, type, quantity) VALUES (%s, %s, %s)', 
                   (id, 'BUY', quantity))
    
    conn.commit()
    conn.close()
    return redirect(url_for('view_products'))

# --- FIX FOR SELL ---
@app.route('/products/sell/<int:id>', methods=['POST'])
def sell_product(id):
    quantity = int(request.form.get('sell_quantity', 0))
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 1. Update Product Quantity
    cursor.execute('UPDATE product_table SET quantity = quantity - %s WHERE id = %s', (quantity, id))
    
    # 2. Log the Movement
    cursor.execute('INSERT INTO stock_movement (product_id, type, quantity) VALUES (%s, %s, %s)', 
                   (id, 'SELL', quantity))
    
    conn.commit()
    conn.close()
    return redirect(url_for('view_products'))

# --- FIX FOR RETURN ---
@app.route('/products/return/<int:id>', methods=['POST'])
def return_product(id):
    quantity = int(request.form.get('return_quantity', 0))
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 1. Update Product Quantity
    cursor.execute('UPDATE product_table SET quantity = quantity + %s WHERE id = %s', (quantity, id))
    
    # 2. Log the Movement
    cursor.execute('INSERT INTO stock_movement (product_id, type, quantity) VALUES (%s, %s, %s)', 
                   (id, 'RETURN', quantity))
    
    conn.commit()
    conn.close()
    return redirect(url_for('view_products'))

if __name__ == '__main__':
    app.run(debug=True, port=5000, use_reloader=False)