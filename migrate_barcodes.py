import sqlite3
import os
from barcode import Code128
from barcode.writer import SVGWriter

DATABASE = 'Inventery_management_2_0.db'
BARCODE_DIR = 'static/barcodes'

def generate_barcode(sku):
    """Generate barcode for product SKU"""
    try:
        # Create barcode using Code128 format (SVG format - no font issues)
        barcode_path = os.path.join(BARCODE_DIR, sku)
        code = Code128(sku, writer=SVGWriter())
        code.save(barcode_path)
        
        # Return relative path for storage
        return f'{BARCODE_DIR}/{sku}.svg'
    except Exception as e:
        print(f"Error generating barcode for SKU {sku}: {e}")
        return None

def migrate_barcodes():
    """Generate barcodes for all products that don't have one"""
    # Ensure barcode directory exists
    os.makedirs(BARCODE_DIR, exist_ok=True)
    
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Get all products without barcodes
    cursor.execute('''
        SELECT ID, sku FROM `PRODUCT TABLE (Core Table)` 
        WHERE barcode_path IS NULL OR barcode_path = ''
    ''')
    
    products = cursor.fetchall()
    
    if not products:
        print("✓ All products already have barcodes!")
        conn.close()
        return
    
    print(f"Generating barcodes for {len(products)} products...")
    
    for product_id, sku in products:
        barcode_path = generate_barcode(sku)
        
        if barcode_path:
            cursor.execute(
                'UPDATE `PRODUCT TABLE (Core Table)` SET barcode_path = ? WHERE ID = ?',
                (barcode_path, product_id)
            )
            print(f"✓ Generated barcode for SKU: {sku}")
        else:
            print(f"✗ Failed to generate barcode for SKU: {sku}")
    
    conn.commit()
    conn.close()
    
    print(f"✓ Migration complete! {len(products)} barcodes generated.")

if __name__ == '__main__':
    migrate_barcodes()
