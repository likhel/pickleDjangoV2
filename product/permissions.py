from rest_framework import permissions
from .models import Product

class IsSellerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow sellers to edit products,
    and allow anyone to read products.
    """

    def has_permission(self, request, view):
        # Allow read-only access to anyone
        if request.method in permissions.SAFE_METHODS:
            return True

        # Only allow authenticated users (potential sellers) to create products
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Allow read-only access for anyone
        if request.method in permissions.SAFE_METHODS:
            return True

        # Only allow the product's seller to update or delete it
        if isinstance(obj, Product):
            return obj.seller == request.user
    
        return False