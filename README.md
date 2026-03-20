# Product Management System - CRUD Application

## Features Implemented
- ✅ Add Product
- ✅ View Products (with low stock alerts)
- ✅ Edit Product (modal popup)
- ✅ Delete Product (with confirmation)

## Installation

### 1. Install Flask
```bash
pip install flask --break-system-packages
```

### 2. Run the Application
```bash
cd inventory_app
python3 app.py
```

### 3. Access the Application
Open your browser and go to:
```
http://localhost:5000
```

## How to Use

### Add Product
1. Fill in the form at the top of the page
2. Required fields: SKU, Name, Price, Quantity, Shelf Number, Reorder Level
3. Category is optional
4. Click "Add Product"

### View Products
- All products are displayed in a table
- Products with quantity ≤ reorder level show a warning (⚠️)
- Shows: ID, SKU, Name, Category, Price, Quantity, Shelf, Reorder Level

### Edit Product
1. Click "Edit" button on any product row
2. Modal popup appears with current product data
3. Modify fields as needed
4. Click "Update Product"

### Delete Product
1. Click "Delete" button on any product row
2. Confirm deletion in popup dialog
3. Product is permanently removed

## Database Structure

**PRODUCT TABLE (Core Table)**
- ID (Primary Key, Auto-increment)
- sku (Text)
- Name (Text)
- category_id (Integer, Foreign Key)
- price (Real/Float)
- quantity (Integer)
- shelf_number (Text)
- reorder_level (Integer)
- created_at (Timestamp)

**CATEGORY TABLE**
- id (Primary Key)
- name (Text)
- created_at (Timestamp)

## Notes
- Barcode functionality is NOT implemented (as per requirements)
- Low stock items highlighted in red with warning icon
- Delete action requires confirmation
- Edit uses AJAX for smooth user experience
