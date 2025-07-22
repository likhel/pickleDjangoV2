# permissions.py

from rest_framework import permissions

class IsUserProfileOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of a profile to view or edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the profile.
        return obj.user == request.user

class IsUserAddressOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an address to view or edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the address.
        return obj.user == request.user

class IsSellerOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow sellers or admins to access a view.
    """
    def has_permission(self, request, view):
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return False

        # Check if the user's role is 'seller' or 'admin'
        return request.user.role in ['seller', 'admin']

class IsBuyer(permissions.BasePermission):
    """
    Custom permission to only allow buyers to access a view.
    """
    def has_permission(self, request, view):
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return False

        # Check if the user's role is 'buyer'
        return request.user.role == 'buyer'

class IsProductOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of a product to edit or delete it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request (handled by IsSellerOrAdmin or similar)
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions (PUT, PATCH, DELETE) are only allowed to the product owner
        return obj.seller == request.user
    
class IsSellerProfileOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of a seller profile to view or edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request that can view seller profiles (e.g., IsSellerOrAdmin)
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions (PUT, PATCH, DELETE) are only allowed to the seller profile owner
        return obj.user == request.user
    


