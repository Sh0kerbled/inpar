from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

app_name = 'api'

router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet, basename='category')
router.register(r'products', views.ProductViewSet, basename='product')
router.register(r'orders', views.OrderViewSet, basename='order')

urlpatterns = [
    path('auth/login/', views.admin_login, name='admin-login'),
    path('auth/refresh/', views.admin_refresh_token, name='token-refresh'),
    path('auth/me/', views.admin_info, name='admin-info'),
    
    path('exchange-rate/', views.get_exchange_rate, name='exchange-rate'),
    
    path('products/import-excel/', views.ProductViewSet.as_view({'post': 'import_excel'}), name='product-import-excel'),
    path('products/clear-uncategorized/', views.ProductViewSet.as_view({'post': 'clear_uncategorized'}), name='product-clear-uncategorized'),
    path('products/bulk-delete/', views.ProductViewSet.as_view({'post': 'bulk_delete'}), name='product-bulk-delete'),
    path('products/bulk-set-category/', views.ProductViewSet.as_view({'post': 'bulk_set_category'}), name='product-bulk-set-category'),
    path('products/export-template/', views.ProductViewSet.as_view({'get': 'export_template'}), name='product-export-template'),

    path('', include(router.urls)),
    path('health/', views.health_check, name='health-check'),
]
