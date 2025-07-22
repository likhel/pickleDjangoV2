from rest_framework import permissions, viewsets, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.pagination import PageNumberPagination
from .models import Product, ProductCategory
from .serializers import ProductReadSerializer, ProductWriteSerializer, ProductCategorySerializer
from .permissions import IsSellerOrReadOnly

class ProductCategoryViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    permission_classes = (permissions.AllowAny,)


class ProductPagination(PageNumberPagination):
    page_size = 10  
    page_size_query_param = 'page_size'
    max_page_size = 100


class ProductViewSet(viewsets.ModelViewSet):
    """
    CRUD products
    """

    queryset = Product.objects.all()
    pagination_class = ProductPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description', 'ingredients']  
    ordering_fields = ['name', 'price', 'created_at'] 

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return ProductWriteSerializer

        return ProductReadSerializer

    def get_permissions(self):
        if self.action in ["create"]:
            self.permission_classes = [permissions.IsAuthenticated]
        elif self.action in ["update", "partial_update", "destroy"]:
            self.permission_classes = [IsSellerOrReadOnly]
        else:
            self.permission_classes = [permissions.AllowAny]

        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)
