from rest_framework import serializers
from .models import Category, Product, ProductImage, ProductCharacteristic, Order
from .utils import get_usd_to_kzt_rate

class CategorySerializer(serializers.ModelSerializer):
    """Category serializer"""
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'image', 'is_active', 'created_at', 'updated_at']


class ProductCharacteristicSerializer(serializers.ModelSerializer):
    """Product characteristic serializer"""
    class Meta:
        model = ProductCharacteristic
        fields = ['id', 'name', 'value']


class ProductImageSerializer(serializers.ModelSerializer):
    """Product image serializer"""
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'is_main']


class ProductListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for product list (search results, category view)"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    price_kzt = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'price_usd', 'price_kzt', 'main_image', 'category_name', 'category', 'stock_quantity']
    
    def get_price_kzt(self, obj):
        """Calculate price in KZT based on exchange rate"""
        exchange_rate = get_usd_to_kzt_rate()
        price_kzt = obj.price_usd * exchange_rate
        return round(price_kzt, 2)


class ProductDetailSerializer(serializers.ModelSerializer):
    """Full product serializer with images and characteristics"""
    images = ProductImageSerializer(many=True, read_only=True)
    characteristics = ProductCharacteristicSerializer(many=True, read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    price_kzt = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'price_usd', 'price_kzt', 'category', 'category_name',
            'is_active', 'main_image', 'stock_quantity', 'images', 'characteristics',
            'created_at', 'updated_at'
        ]
    
    def get_price_kzt(self, obj):
        exchange_rate = get_usd_to_kzt_rate()
        return round(obj.price_usd * exchange_rate, 2)


class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for admin CRUD operations"""
    characteristics = ProductCharacteristicSerializer(many=True, required=False)
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'price_usd', 'category',
            'is_active', 'main_image', 'stock_quantity', 'characteristics',
            'created_at', 'updated_at'
        ]
    extra_kwargs = {
        'is_active': {
            'required': False,
            'default': True,
        },
    }

    def create(self, validated_data):
        characteristics_data = validated_data.pop('characteristics', [])
        product = Product.objects.create(**validated_data)
        
        for char_data in characteristics_data:
            ProductCharacteristic.objects.create(product=product, **char_data)
        
        return product

    def update(self, instance, validated_data):
        characteristics_data = validated_data.pop('characteristics', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if characteristics_data is not None:
            instance.characteristics.all().delete()
            for char_data in characteristics_data:
                ProductCharacteristic.objects.create(product=instance, **char_data)

        return instance


class OrderSerializer(serializers.ModelSerializer):
    """Order serializer for customer requests"""
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_price_usd = serializers.DecimalField(
        source='product.price_usd', max_digits=10, decimal_places=2, read_only=True
    )
    product_price_kzt = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            'id', 'product', 'product_name', 'product_price_usd', 'product_price_kzt', 'customer_name',
            'customer_email', 'customer_phone', 'customer_message', 'quantity',
            'status', 'created_at', 'updated_at'
        ]
    
    def get_product_price_kzt(self, obj):
        """Calculate price in KZT based on exchange rate"""
        exchange_rate = get_usd_to_kzt_rate()
        price_kzt = obj.product.price_usd * exchange_rate
        return round(price_kzt, 2)


class OrderAdminSerializer(serializers.ModelSerializer):
    """Order serializer for admin (with status management)"""
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_price_usd = serializers.DecimalField(
        source='product.price_usd', max_digits=10, decimal_places=2, read_only=True
    )
    product_price_kzt = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            'id', 'product', 'product_name', 'product_price_usd', 'product_price_kzt', 'customer_name',
            'customer_email', 'customer_phone', 'customer_message', 'quantity',
            'status', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'product_name', 'product_price_usd', 'product_price_kzt', 'created_at', 'updated_at']
    
    def get_product_price_kzt(self, obj):
        """Calculate price in KZT based on exchange rate"""
        exchange_rate = get_usd_to_kzt_rate()
        price_kzt = obj.product.price_usd * exchange_rate
        return round(price_kzt, 2)
