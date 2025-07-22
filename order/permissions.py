from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from rest_framework.permissions import BasePermission, SAFE_METHODS 

from order.models import Order 


class IsOrderPending(BasePermission):
  

    message = _("Updating or deleting closed order is not allowed.")

    def has_object_permission(self, request, view, obj):
       
        if request.method in SAFE_METHODS:
            return True
       
        return obj.status == Order.PENDING 


class IsOrderItemByBuyerOrAdmin(BasePermission):
   
    message = _("You do not have permission to access this order item.") 
    def has_permission(self, request, view):
        
        if request.method in SAFE_METHODS:
            return request.user and request.user.is_authenticated
        
        
        order_id = view.kwargs.get("order_id")
        if not order_id: 
            return False
        try:
            order = get_object_or_404(Order, id=order_id)
            return order.buyer == request.user or request.user.is_staff
        except Order.DoesNotExist:
             return False 

    def has_object_permission(self, request, view, obj):
      
        return obj.order.buyer == request.user or request.user.is_staff


class IsOrderByBuyerOrAdmin(BasePermission):


    message = _("You do not have permission to access this order.")
    def has_permission(self, request, view):
       
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        
        return obj.buyer == request.user or request.user.is_staff


class IsOrderItemPending(BasePermission):
   

    message = _(
        "Creating, updating or deleting order items for a closed order is not allowed."
    )

    def has_permission(self, request, view):
      
        if request.method in SAFE_METHODS and view.action in ("list", "retrieve"):
             return True

        
        order_id = view.kwargs.get("order_id")
        if not order_id:
            return False
        try:
            order = get_object_or_404(Order, id=order_id)
            return order.status == Order.PENDING
        except Order.DoesNotExist:
            return False 


    def has_object_permission(self, request, view, obj):
       
        if view.action in ("retrieve",):
            return True
        
        return obj.order.status == Order.PENDING S
