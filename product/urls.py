from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, ProductCategoryViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'categories', ProductCategoryViewSet, basename='productcategory')

urlpatterns = [
    path('', include(router.urls)),
]