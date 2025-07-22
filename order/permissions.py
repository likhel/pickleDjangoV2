from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from rest_framework.permissions import BasePermission, SAFE_METHODS # Import SAFE_METHODS

from order.models import Order # Ensure this import is correct based on your project structure


class IsOrderPending(BasePermission):
    """
    Check the status of order is pending before updating/deleting instance
    """

    message = _("Updating or deleting closed order is not allowed.")

    def has_object_permission(self, request, view, obj):
        # Allow read operations (GET, HEAD, OPTIONS)
        if request.method in SAFE_METHODS:
            return True
        # Allow write operations only if the order status is pending
        return obj.status == Order.PENDING # Use the model constant for clarity


class IsOrderItemByBuyerOrAdmin(BasePermission):
    """
    Check if order item is owned by appropriate buyer or admin
    """

    message = _("You do not have permission to access this order item.") # Add a message for consistency

    def has_permission(self, request, view):
        # Allow safe methods (list) if authenticated, object-level check will handle ownership
        if request.method in SAFE_METHODS:
            return request.user and request.user.is_authenticated
        
        # For write methods (create, update, delete), check parent order ownership
        order_id = view.kwargs.get("order_id")
        if not order_id: # Should not happen with correct URL patterns, but good practice
            return False
        try:
            order = get_object_or_404(Order, id=order_id)
            return order.buyer == request.user or request.user.is_staff
        except Order.DoesNotExist:
             return False # Order must exist to have order items


    def has_object_permission(self, request, view, obj):
        # Object-level check for ownership/admin status
        return obj.order.buyer == request.user or request.user.is_staff


class IsOrderByBuyerOrAdmin(BasePermission):
    """
    Check if order is owned by appropriate buyer or admin
    """

    message = _("You do not have permission to access this order.") # Add a message for consistency

    def has_permission(self, request, view):
        # Allow access if authenticated
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Object-level check for ownership/admin status
        return obj.buyer == request.user or request.user.is_staff


class IsOrderItemPending(BasePermission):
    """
    Check the status of order is pending before creating, updating and deleting order items
    """

    message = _(
        "Creating, updating or deleting order items for a closed order is not allowed."
    )

    def has_permission(self, request, view):
        # Allow safe methods (list, retrieve) regardless of status, object-level check will handle retrieve status
        if request.method in SAFE_METHODS and view.action in ("list", "retrieve"):
             return True

        # For write methods (create, update, delete), check parent order status
        order_id = view.kwargs.get("order_id")
        if not order_id:
            return False
        try:
            order = get_object_or_404(Order, id=order_id)
            return order.status == Order.PENDING # Use the model constant
        except Order.DoesNotExist:
            return False # Order must exist to have order items to check status


    def has_object_permission(self, request, view, obj):
        # Allow retrieve regardless of status
        if view.action in ("retrieve",):
            return True
        # Allow write operations only if the order item's order status is pending
        return obj.order.status == Order.PENDING # Use the model constant
