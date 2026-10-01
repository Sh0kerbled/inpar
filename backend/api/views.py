from rest_framework import viewsets, status, filters
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.db.models import Q, Min, Max
from django.views.decorators.csrf import csrf_exempt
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.parsers import MultiPartParser, FormParser
from django.http import HttpResponse

from .models import Category, Product, Order
from .serializers import (
    CategorySerializer, ProductListSerializer, ProductDetailSerializer,
    ProductCreateUpdateSerializer, OrderSerializer, OrderAdminSerializer
)
from .utils import get_usd_to_kzt_rate
from .excel_service import import_products_from_excel, generate_excel_template


@api_view(['POST'])
@permission_classes([AllowAny])
def admin_login(request):
    """
    Admin login endpoint
    POST /api/auth/login/
    {
        "username": "admin",
        "password": "password"
    }
    Returns:
    {
        "access": "token",
        "refresh": "token",
        "user": { id, username, email, is_staff }
    }
    """
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({
            'error': 'Username and password are required'
        }, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=username, password=password)

    if not user:
        return Response({
            'error': 'Invalid credentials'
        }, status=status.HTTP_401_UNAUTHORIZED)

    if not user.is_staff:
        return Response({
            'error': 'Only admins can login here'
        }, status=status.HTTP_403_FORBIDDEN)

    refresh = RefreshToken.for_user(user)

    return Response({
        'access': str(refresh.access_token),
        'refresh': str(refresh),
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'is_staff': user.is_staff
        }
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def admin_refresh_token(request):
    """
    Refresh admin token
    POST /api/auth/refresh/
    {
        "refresh": "refresh_token"
    }
    """
    refresh_token = request.data.get('refresh')

    if not refresh_token:
        return Response({
            'error': 'Refresh token is required'
        }, status=status.HTTP_400_BAD_REQUEST)

    try:
        refresh = RefreshToken(refresh_token)
        return Response({
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'error': 'Invalid refresh token'
        }, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def admin_info(request):
    """
    Get current admin info
    Requires JWT token in Authorization header
    """
    user = request.user
    return Response({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'is_staff': user.is_staff,
        'date_joined': user.date_joined
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """Health check endpoint"""
    return Response({
        'status': 'ok',
        'message': 'Backend is running'
    }, status=status.HTTP_200_OK)


class CategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing categories
    - List: available to everyone
    - Create/Update/Delete: only for admin
    """
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    filterset_fields = ['is_active']
    search_fields = ['name', 'description']

    def get_permissions(self):
        """Allow anyone to list and retrieve, but only admin can modify"""
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated, IsAdminUser]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """If not admin, only show active categories"""
        if self.request.user and self.request.user.is_staff:
            return Category.objects.all()
        return Category.objects.filter(is_active=True)


class ProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing products with search, filter and sort
    - List/Retrieve: available to everyone
    - Create/Update/Delete: only for admin
    """
    queryset = Product.objects.filter(is_active=True).select_related('category')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'is_active']
    search_fields = ['name', 'sku', 'description']
    ordering_fields = ['price_usd', 'wholesale_price_usd', 'name', 'created_at', 'stock_quantity']
    ordering = ['-created_at']

    def get_permissions(self):
        """Allow anyone to list and retrieve, but only admin can modify"""
        if self.action in ['list', 'retrieve', 'search', 'price_range']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated, IsAdminUser]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """Filter by price range and category"""
        queryset = Product.objects.select_related('category')

        if not (self.request.user and self.request.user.is_staff):
            queryset = queryset.filter(is_active=True)

        category_param = self.request.query_params.get('category')
        if category_param in ['null', 'none', 'uncategorized', 'without']:
            queryset = queryset.filter(Q(category__isnull=True) | Q(category__name='Без категории'))
        elif category_param:
            queryset = queryset.filter(category_id=category_param)

        price_min = self.request.query_params.get('price_min')
        price_max = self.request.query_params.get('price_max')

        if price_min:
            queryset = queryset.filter(price_usd__gte=float(price_min))
        if price_max:
            queryset = queryset.filter(price_usd__lte=float(price_max))

        return queryset

    def get_serializer_class(self):
        """Use different serializers based on action"""
        if self.action == 'list':
            return ProductListSerializer
        elif self.action == 'retrieve':
            return ProductDetailSerializer
        else:  # create, update, partial_update, destroy
            return ProductCreateUpdateSerializer
    
    def perform_create(self, serializer):
        """Override create to ensure proper permissions"""
        serializer.save(is_active=True)
    
    def perform_update(self, serializer):
        """Override update to ensure proper permissions"""
        serializer.save()
    
    def perform_destroy(self, instance):
        """Override destroy to ensure proper permissions"""
        instance.delete()

    @action(detail=False, methods=['post'], url_path='import-excel', parser_classes=[MultiPartParser, FormParser], permission_classes=[IsAuthenticated, IsAdminUser])
    def import_excel(self, request):
        """
        Upload and import products from an Excel (.xlsx) file
        """
        file_obj = request.FILES.get('file')
        if not file_obj:
            return Response({'error': 'Файл Excel не предоставлен'}, status=status.HTTP_400_BAD_REQUEST)
        
        default_category_id = request.data.get('category') or request.data.get('category_id')
        currency = request.data.get('currency', 'KZT')
        result = import_products_from_excel(file_obj, default_category_id=default_category_id, currency=currency)
        
        if not result.get('success'):
            return Response(result, status=status.HTTP_400_BAD_REQUEST)
        return Response(result, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='clear-uncategorized', permission_classes=[IsAuthenticated, IsAdminUser])
    def clear_uncategorized(self, request):
        """
        Delete all products that have no category or are in 'Без категории'
        Useful for cleaning up erroneous test imports.
        """
        qs = Product.objects.filter(Q(category__isnull=True) | Q(category__name='Без категории'))
        count = qs.count()
        qs.delete()
        return Response({'success': True, 'deleted': count})

    @action(detail=False, methods=['post'], url_path='bulk-delete', permission_classes=[IsAuthenticated, IsAdminUser])
    def bulk_delete(self, request):
        """
        Delete products by IDs list or all products
        Body: { "ids": [1, 2, 3] } OR { "all": true }
        """
        delete_all = request.data.get('all', False)
        if delete_all:
            count = Product.objects.all().count()
            Product.objects.all().delete()
            return Response({'success': True, 'deleted': count})
        
        ids = request.data.get('ids', [])
        if not ids:
            return Response({'error': 'Не указаны ID товаров для удаления'}, status=status.HTTP_400_BAD_REQUEST)
        
        qs = Product.objects.filter(id__in=ids)
        count = qs.count()
        qs.delete()
        return Response({'success': True, 'deleted': count})

    @action(detail=False, methods=['post'], url_path='bulk-set-category', permission_classes=[IsAuthenticated, IsAdminUser])
    def bulk_set_category(self, request):
        """
        Assign category to multiple products at once
        Body: { "ids": [1, 2, 3], "category_id": 5 }
        """
        ids = request.data.get('ids', [])
        category_id = request.data.get('category_id')
        
        if not ids:
            return Response({'error': 'Не указаны ID товаров'}, status=status.HTTP_400_BAD_REQUEST)
        
        category = None
        if category_id:
            category = Category.objects.filter(id=category_id).first()
            if not category:
                return Response({'error': 'Категория не найдена'}, status=status.HTTP_404_NOT_FOUND)
        
        updated = Product.objects.filter(id__in=ids).update(category=category)
        return Response({'success': True, 'updated': updated})

    @action(detail=False, methods=['get'], url_path='export-template', permission_classes=[IsAuthenticated, IsAdminUser])
    def export_template(self, request):
        """
        Download blank/sample Excel template for product import
        """
        content = generate_excel_template()
        response = HttpResponse(
            content,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename="inpar_products_template.xlsx"'
        return response

    @action(detail=False, methods=['get'])
    def search(self, request):
        """
        Dynamic search endpoint
        Query params: q (search string), category, price_min, price_max
        Used for real-time search suggestions with minimal data
        """
        query = request.query_params.get('q', '').strip()
        category_id = request.query_params.get('category')

        if len(query) < 2:
            return Response({'results': []})

        results = Product.objects.filter(is_active=True).filter(
            Q(name__icontains=query) | Q(sku__icontains=query) | Q(description__icontains=query)
        ).select_related('category')

        if category_id:
            results = results.filter(category_id=category_id)

        results = results[:10]
        serializer = ProductListSerializer(results, many=True)

        return Response({
            'count': len(results),
            'results': serializer.data
        })

    @action(detail=False, methods=['get'])
    def price_range(self, request):
        """
        Get min and max price for filtering
        """
        products = Product.objects.filter(is_active=True).aggregate(
            min_price=Min('price_usd'),
            max_price=Max('price_usd')
        )
        return Response(products)


class OrderViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling customer orders
    - Create: anyone (customer inquiry)
    - List/Update/Destroy: only admin
    - Retrieve: anyone (but should be protected in production)
    """
    queryset = Order.objects.all()

    def get_permissions(self):
        """
        Allow anyone to create an order (customer inquiry)
        But only admin can list, retrieve, update, delete
        """
        if self.action == 'create':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated, IsAdminUser]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        """Use different serializers for admin and customers"""
        if self.request.user and self.request.user.is_staff:
            return OrderAdminSerializer
        return OrderSerializer

    def get_queryset(self):
        """Admins see all orders, customers see none"""
        if self.request.user and self.request.user.is_staff:
            return Order.objects.select_related('product').all()
        return Order.objects.none()

    def create(self, request, *args, **kwargs):
        """Create order and return confirmation"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response({
            'success': True,
            'message': 'Your order has been created. We will contact you soon.',
            'order_id': serializer.data.get('id')
        }, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_exchange_rate(request):
    """
    Get current USD to KZT exchange rate
    GET /api/exchange-rate/
    Returns:
    {
        "rate": 460.0,
        "currency_from": "USD",
        "currency_to": "KZT"
    }
    """
    rate = get_usd_to_kzt_rate()
    return Response({
        'rate': float(rate),
        'currency_from': 'USD',
        'currency_to': 'KZT'
    })
