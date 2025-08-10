# permissions.py

from rest_framework import permissions

class IsUserProfileOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of a profile to view or edit it.
    """
    def has_object_permission(self, request, view, obj):
       
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the profile.
        return obj.user == request.user

class IsUserAddressOwner(permissions.BasePermission):
   
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user == request.user

class IsSellerOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow sellers or admins to access a view.
    """
    def has_permission(self, request, view):
       
        if not request.user.is_authenticated:
            return False

        
        return request.user.role in ['seller', 'admin']

class IsBuyer(permissions.BasePermission):
    """
    Custom permission to only allow buyers to access a view.
    """
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
    


