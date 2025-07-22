from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated 

from .models import Order, OrderItem
from .permissions import (
    IsOrderByBuyerOrAdmin,
    IsOrderItemByBuyerOrAdmin,
    IsOrderItemPending,
    IsOrderPending,
)
from .serializers import (
    OrderItemSerializer,
    OrderReadSerializer,
    OrderWriteSerializer,
)


class OrderItemViewSet(viewsets.ModelViewSet):
   

    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated, IsOrderItemByBuyerOrAdmin]

    def get_queryset(self):
        res = super().get_queryset()
        order_id = self.kwargs.get("order_pk")
      
        user = self.request.user
        if user.is_staff:
             return res.filter(order__id=order_id)
        return res.filter(order__id=order_id, order__buyer=user)


    def perform_create(self, serializer):
        order = get_object_or_404(Order, id=self.kwargs.get("order_id"))
        
        user = self.request.user
        if user.is_staff or order.buyer == user:
            serializer.save(order=order)
        else:
            from rest_framework.exceptions import PermissionDenied 
            raise PermissionDenied("You do not have permission to add items to this order.")


    def get_permissions(self):
        if self.action in ("create", "update", "partial_update", "destroy"):
            self.permission_classes += [IsOrderItemPending]

        return super().get_permissions()


class OrderViewSet(viewsets.ModelViewSet):
 
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated, IsOrderByBuyerOrAdmin]

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update", "destroy"):
            return OrderWriteSerializer

        return OrderReadSerializer

    def get_queryset(self):
        res = super().get_queryset()
        user = self.request.user
        
        if user.is_staff:
            return res
        return res.filter(buyer=user)

    def get_permissions(self):
        if self.action in ("update", "partial_update", "destroy"):
            self.permission_classes += [IsOrderPending]

        return super().get_permissions()
