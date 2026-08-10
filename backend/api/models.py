from django.db import models


class BaseModel(models.Model):
    """Abstract base model with timestamps"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(BaseModel):
    """Product category"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(BaseModel):
    """Product model"""
    name = models.CharField(max_length=200)
    description = models.TextField()
    price_usd = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price in USD")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products')
    is_active = models.BooleanField(default=True)
    main_image = models.ImageField(upload_to='products/', blank=True, null=True)
    stock_quantity = models.IntegerField(default=0)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['category']),
            models.Index(fields=['price_usd']),
        ]

    def __str__(self):
        return self.name


class ProductImage(BaseModel):
    """Additional product images"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/images/')
    is_main = models.BooleanField(default=False)

    class Meta:
        ordering = ['is_main', 'created_at']

    def __str__(self):
        return f"Image for {self.product.name}"


class ProductCharacteristic(BaseModel):
    """Product characteristics/specifications"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='characteristics')
    name = models.CharField(max_length=100)  # e.g., "Material", "Size", "Color"
    value = models.CharField(max_length=255)  # e.g., "Leather", "M", "Black"

    class Meta:
        unique_together = ['product', 'name']
        ordering = ['name']

    def __str__(self):
        return f"{self.product.name} - {self.name}: {self.value}"


class Order(BaseModel):
    """Customer order/contact request"""
    STATUS_CHOICES = [
        ('new', 'New'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='orders')
    customer_name = models.CharField(max_length=150)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=20)
    customer_message = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    quantity = models.IntegerField(default=1)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order {self.id} - {self.customer_name}"
