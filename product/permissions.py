from rest_framework import permissions
from .models import Product

class IsSellerOrReadOnly(permissions.BasePermission):
    

    def has_permission(self, request, view):
       
        if request.method in permissions.SAFE_METHODS:
            return True

       
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
       
        if request.method in permissions.SAFE_METHODS:
            return True

   
        if isinstance(obj, Product):
            return obj.seller == request.user
    
        return False
