# API Endpoints Documentation

## Base URL

```
http://localhost:8000/api/
```

## Categories

### List Categories

```
GET /api/categories/
```

- **Permissions**: Public
- **Query Params**: None
- **Response**: List of active categories

### Get Category Detail

```
GET /api/categories/{id}/
```

- **Permissions**: Public

### Create Category (Admin Only)

```
POST /api/categories/
Content-Type: application/json

{
  "name": "Electronics",
  "description": "Electronic devices",
  "is_active": true
}
```

- **Permissions**: Admin
- **Auth**: Session/Basic Auth

### Update Category (Admin Only)

```
PATCH /api/categories/{id}/
Content-Type: application/json

{
  "name": "Updated Name"
}
```

### Delete Category (Admin Only)

```
DELETE /api/categories/{id}/
```

---

## Products

### List Products (with Filtering)

```
GET /api/products/
```

- **Permissions**: Public
- **Query Params**:
  - `category`: Filter by category ID
  - `price_min`: Minimum price
  - `price_max`: Maximum price
  - `search`: Search in name and description
  - `ordering`: `price` (asc), `-price` (desc), `name`, `-created_at`

**Example**:

```
GET /api/products/?category=1&price_min=100&price_max=500&ordering=price
```

### Get Product Detail

```
GET /api/products/{id}/
```

- **Permissions**: Public
- **Response**: Full product with images and characteristics

### Search Products (Dynamic)

```
GET /api/products/search/?q=laptop&category=1
```

- **Permissions**: Public
- **Query Params**:
  - `q`: Search query (min 2 characters)
  - `category`: Optional category filter
- **Response**: Limited results for quick suggestions

```json
{
  "count": 5,
  "results": [
    {
      "id": 1,
      "name": "Laptop Pro",
      "price": "999.99",
      "main_image": "...",
      "category": 1,
      "category_name": "Electronics"
    }
  ]
}
```

### Price Range

```
GET /api/products/price_range/
```

- **Permissions**: Public
- **Response**:

```json
{
  "min_price": "10.00",
  "max_price": "5000.00"
}
```

### Create Product (Admin Only)

```
POST /api/products/
Content-Type: application/json

{
  "name": "Laptop Pro",
  "description": "High performance laptop",
  "price": "999.99",
  "category": 1,
  "stock_quantity": 50,
  "is_active": true,
  "characteristics": [
    {"name": "Processor", "value": "Intel i7"},
    {"name": "RAM", "value": "16GB"}
  ]
}
```

- **Permissions**: Admin

### Update Product (Admin Only)

```
PATCH /api/products/{id}/
```

### Delete Product (Admin Only)

```
DELETE /api/products/{id}/
```

---

## Product Images

Images are managed through inlines in the admin panel or via the Product serializer.

---

## Orders (Customer Requests)

### Create Order (Public)

```
POST /api/orders/
Content-Type: application/json

{
  "product": 1,
  "customer_name": "John Doe",
  "customer_email": "john@example.com",
  "customer_phone": "+1234567890",
  "customer_message": "I'm interested in this product",
  "quantity": 2
}
```

- **Permissions**: Public
- **Response**:

```json
{
  "success": true,
  "message": "Your order has been created. We will contact you soon.",
  "order_id": 123
}
```

### List Orders (Admin Only)

```
GET /api/orders/
```

- **Permissions**: Admin
- **Response**: List of all orders with status

### Get Order Detail (Admin Only)

```
GET /api/orders/{id}/
```

### Update Order Status (Admin Only)

```
PATCH /api/orders/{id}/
Content-Type: application/json

{
  "status": "processing"
}
```

- **Status Values**: `new`, `processing`, `completed`, `cancelled`

### Delete Order (Admin Only)

```
DELETE /api/orders/{id}/
```

---

## Admin Authentication

### Create Superuser

```bash
docker-compose exec backend python manage.py createsuperuser
```

### Login

```
POST /admin/
```

- Use Django admin panel at `http://localhost:8000/admin/`

---

## Filter Examples

### Find cheap products in Electronics

```
GET /api/products/?category=1&price_max=100&ordering=price
```

### Find products by name (sorted by price descending)

```
GET /api/products/?search=phone&ordering=-price
```

### Dynamic search for laptops

```
GET /api/products/search/?q=laptop
```

---

## Error Responses

### 400 Bad Request

```json
{
  "detail": "Invalid query parameters"
}
```

### 401 Unauthorized

```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden

```json
{
  "detail": "You do not have permission to perform this action."
}
```

### 404 Not Found

```json
{
  "detail": "Not found."
}
```

---

## Quick Start

1. **Start Docker**:

```bash
docker-compose up -d
```

2. **Create superuser**:

```bash
docker-compose exec backend python manage.py createsuperuser
```

3. **Access admin**:

```
http://localhost:8000/admin/
```

4. **Create categories and products in admin panel**

5. **Test API**:

```bash
# Get all products
curl http://localhost:8000/api/products/

# Search for products
curl http://localhost:8000/api/products/search/?q=laptop

# Create order
curl -X POST http://localhost:8000/api/orders/ \
  -H "Content-Type: application/json" \
  -d '{
    "product": 1,
    "customer_name": "John",
    "customer_email": "john@example.com",
    "customer_phone": "+1234567890",
    "quantity": 1
  }'
```
