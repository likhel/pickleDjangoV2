# permissions.py

from rest_framework import permissions

class IsUserProfileOwner(permissions.BasePermission):
  
    def has_object_permission(self, request, view, obj):
        
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user == request.user

class IsUserAddressOwner(permissions.BasePermission):
   
    def has_object_permission(self, request, view, obj):
        
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user == request.user

class IsSellerOrAdmin(permissions.BasePermission):
   
    def has_permission(self, request, view):
      
        if not request.user.is_authenticated:
            return False

        return request.user.role in ['seller', 'admin']

class IsBuyer(permissions.BasePermission):
   
    def has_permission(self, request, view):
       
        if not request.user.is_authenticated:
            return False

       
        return request.user.role == 'buyer'

class IsProductOwner(permissions.BasePermission):
  
    def has_object_permission(self, request, view, obj):
        
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.seller == request.user
    
class IsSellerProfileOwner(permissions.BasePermission):
   
    def has_object_permission(self, request, view, obj):
       
        if request.method in permissions.SAFE_METHODS:
            return True

      
        return obj.user == request.user
    


