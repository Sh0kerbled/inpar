from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, ProductImage, ProductCharacteristic, Order


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ['image', 'is_main']


class ProductCharacteristicInline(admin.TabularInline):
    model = ProductCharacteristic
    extra = 1
    fields = ['name', 'value']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price_usd', 'stock_quantity', 'is_active', 'created_at', 'image_preview']
    list_filter = ['is_active', 'category', 'price_usd', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at', 'main_image_preview']
    inlines = [ProductImageInline, ProductCharacteristicInline]

    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'description', 'category', 'is_active')
        }),
        ('Pricing & Stock', {
            'fields': ('price_usd', 'stock_quantity')
        }),
        ('Images', {
            'fields': ('main_image', 'main_image_preview')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def image_preview(self, obj):
        if obj.main_image:
            return format_html('<img src="{}" width="50" height="50" />', obj.main_image.url)
        return 'No image'
    image_preview.short_description = 'Preview'

    def main_image_preview(self, obj):
        if obj.main_image:
            return format_html('<img src="{}" width="300" />', obj.main_image.url)
        return 'No image'
    main_image_preview.short_description = 'Main Image'


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'is_main', 'created_at', 'image_preview']
    list_filter = ['is_main', 'product__category']
    search_fields = ['product__name']

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />', obj.image.url)
        return 'No image'
    image_preview.short_description = 'Preview'


@admin.register(ProductCharacteristic)
class ProductCharacteristicAdmin(admin.ModelAdmin):
    list_display = ['product', 'name', 'value']
    list_filter = ['product__category', 'name']
    search_fields = ['product__name', 'name', 'value']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_name', 'product', 'customer_email', 'status', 'quantity', 'created_at']
    list_filter = ['status', 'created_at', 'product__category']
    search_fields = ['customer_name', 'customer_email', 'customer_phone', 'product__name']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Order Info', {
            'fields': ('product', 'status', 'quantity')
        }),
        ('Customer Info', {
            'fields': ('customer_name', 'customer_email', 'customer_phone')
        }),
        ('Message', {
            'fields': ('customer_message',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
