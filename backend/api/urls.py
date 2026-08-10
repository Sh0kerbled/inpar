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
    
    path('', include(router.urls)),
    path('health/', views.health_check, name='health-check'),
]
