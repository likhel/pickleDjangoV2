from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedSimpleRouter

from .views import OrderViewSet, OrderItemViewSet

# Create a router for the OrderViewSet
router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='order')

# Create a nested router for OrderItemViewSet
# This will create URLs like /orders/{order_pk}/items/
orders_router = NestedSimpleRouter(router, r'orders', lookup='order')
orders_router.register(r'items', OrderItemViewSet, basename='order-item')

urlpatterns = [
    path('', include(router.urls)), # Include the main order router URLs
    path('', include(orders_router.urls)), # Include the nested order item router URLs
]
