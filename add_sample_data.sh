#!/bin/bash

# Quick add sample products script

echo "Adding sample categories and products..."

docker-compose exec -T backend python manage.py shell <<'SHELL'
from api.models import Category, Product, ProductImage, ProductCharacteristic
import os

# Create categories
electronics = Category.objects.create(
    name="Electronics",
    description="Electronic devices and gadgets"
)

furniture = Category.objects.create(
    name="Furniture",
    description="Furniture for home and office"
)

clothing = Category.objects.create(
    name="Clothing",
    description="Clothes and accessories"
)

print("✓ Categories created")

# Create products
products_data = [
    {
        "name": "Laptop Pro",
        "description": "High performance laptop with 16GB RAM and SSD storage",
        "price": "1299.99",
        "category": electronics,
        "stock": 5,
        "characteristics": [
            {"name": "RAM", "value": "16GB"},
            {"name": "Storage", "value": "512GB SSD"},
            {"name": "Processor", "value": "Intel Core i7"},
            {"name": "Display", "value": "15.6 inch FHD"}
        ]
    },
    {
        "name": "Wireless Mouse",
        "description": "Comfortable wireless mouse with long battery life",
        "price": "29.99",
        "category": electronics,
        "stock": 50,
        "characteristics": [
            {"name": "Type", "value": "Wireless"},
            {"name": "Battery Life", "value": "18 months"},
            {"name": "DPI", "value": "1000-3200"}
        ]
    },
    {
        "name": "Office Chair",
        "description": "Ergonomic office chair with lumbar support",
        "price": "199.99",
        "category": furniture,
        "stock": 10,
        "characteristics": [
            {"name": "Material", "value": "Mesh"},
            {"name": "Max Weight", "value": "130kg"},
            {"name": "Height Adjustable", "value": "Yes"}
        ]
    },
    {
        "name": "T-Shirt",
        "description": "Comfortable cotton t-shirt",
        "price": "19.99",
        "category": clothing,
        "stock": 100,
        "characteristics": [
            {"name": "Material", "value": "100% Cotton"},
            {"name": "Sizes", "value": "XS-XXL"},
            {"name": "Colors", "value": "Black, White, Blue"}
        ]
    }
]

for prod_data in products_data:
    characteristics = prod_data.pop("characteristics")
    stock = prod_data.pop("stock")
    
    product = Product.objects.create(
        **prod_data,
        stock_quantity=stock,
        is_active=True
    )
    
    for char in characteristics:
        ProductCharacteristic.objects.create(
            product=product,
            **char
        )
    
    print(f"✓ Created product: {product.name}")

print("\n✅ Sample data added successfully!")
print("\nYou can now:")
print("1. Go to http://localhost:8000/admin/")
print("2. Add product images to existing products")
print("3. Test the API at http://localhost:8000/api/products/")
SHELL

echo ""
echo "Test the API:"
echo "  All products: curl http://localhost:8000/api/products/"
echo "  Search: curl 'http://localhost:8000/api/products/search/?q=laptop'"
echo "  Filters: curl 'http://localhost:8000/api/products/?category=1&price_max=500'"
echo "  Sort: curl 'http://localhost:8000/api/products/?ordering=price'"
