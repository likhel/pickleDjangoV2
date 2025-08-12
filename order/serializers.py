from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from .models import Order, OrderItem
from product.serializers import ProductReadSerializer  
from user.serializers import AddressReadOnlySerializer  
from django.contrib.auth import get_user_model
from product.models import Product

User = get_user_model()

class OrderItemSerializer(serializers.ModelSerializer):
  

    product = ProductReadSerializer(read_only=True)
    price = serializers.SerializerMethodField()
    cost = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = (
            "id",
            "order",
            "product",
            "quantity",
            "price",
            "cost",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("order", "price", "cost") 
    def validate(self, validated_data):
        order_quantity = validated_data["quantity"]
        product = validated_data["product"]
        product_quantity = product.stock

        order_id = self.context["view"].kwargs.get("order_id")
        current_item = OrderItem.objects.filter(order__id=order_id, product=product)

        if order_quantity > product_quantity:
            error = {"quantity": _("Ordered quantity is more than the stock.")}
            raise serializers.ValidationError(error)

        if not self.instance and current_item.count() > 0:
            error = {"product": _("Product already exists in your order.")}
            raise serializers.ValidationError(error)
        
       
        request = self.context.get('request', None)
        if request and request.user == product.seller:
             error = _("Adding your own product to your order is not allowed")
             raise PermissionDenied(error)


        return validated_data

    def get_price(self, obj):
        return obj.product.price

    def get_cost(self, obj):
        return obj.cost


class OrderReadSerializer(serializers.ModelSerializer):
  

    buyer = serializers.CharField(source="buyer.username", read_only=True) 
    order_items = OrderItemSerializer(read_only=True, many=True)
    total_cost = serializers.SerializerMethodField(read_only=True)
    shipping_address = AddressReadOnlySerializer(read_only=True) 
    billing_address = AddressReadOnlySerializer(read_only=True) 


    class Meta:
        model = Order
        fields = (
            "id",
            "buyer",
            "shipping_address",
            "billing_address",
            "order_items",
            "total_cost",
            "status",
            "created_at",
            "updated_at",
        )

    def get_total_cost(self, obj):
        return obj.total_cost


class OrderWriteSerializer(serializers.ModelSerializer):


    buyer = serializers.HiddenField(default=serializers.CurrentUserDefault())
  
    order_items = serializers.ListField(child=serializers.DictField(), write_only=True)


    class Meta:
        model = Order
        fields = (
            "id",
            "buyer",
            "status",
            "order_items",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("status",)

    def create(self, validated_data):
        order_items_data = validated_data.pop("order_items")
        order = Order.objects.create(**validated_data)

        for item_data in order_items_data:
            product_id = item_data.get('product')
            quantity = item_data.get('quantity')

            if not product_id or not quantity:
                 raise serializers.ValidationError(_("Each item must have a product ID and quantity."))

            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                raise serializers.ValidationError(_(f"Product with ID {product_id} does not exist."))

          
            if quantity > product.stock:
                 raise serializers.ValidationError(_(f"Ordered quantity for product {product.name} is more than the stock."))

            request = self.context.get('request', None)
            if request and request.user == product.seller:
                 raise PermissionDenied(_("Adding your own product to your order is not allowed"))

            
            if OrderItem.objects.filter(order=order, product=product).exists():
                 raise serializers.ValidationError(_(f"Product {product.name} already exists in this order."))

            OrderItem.objects.create(order=order, product=product, quantity=quantity)

        return order

    def update(self, instance, validated_data):
        
        instance.status = validated_data.get('status', instance.status)
        instance.save()

        
        order_items_data = validated_data.get("order_items")
        if order_items_data:
           
            existing_items = {item.product.id: item for item in instance.order_items.all()}
            
            for item_data in order_items_data:
                product_id = item_data.get('product')
                quantity = item_data.get('quantity')

                if not product_id or not quantity:
                     raise serializers.ValidationError(_("Each item must have a product ID and quantity."))

                try:
                    product = Product.objects.get(id=product_id)
                except Product.DoesNotExist:
                    raise serializers.ValidationError(_(f"Product with ID {product_id} does not exist."))
                
                
                current_item_quantity = existing_items[product_id].quantity if product_id in existing_items else 0
                if quantity > product.stock + current_item_quantity:
                    raise serializers.ValidationError(_(f"Ordered quantity for product {product.name} is more than the stock."))

               
                request = self.context.get('request', None)
                if request and request.user == product.seller:
                     raise PermissionDenied(_("Adding your own product to your order is not allowed"))

                if product_id in existing_items:
                   
                    item = existing_items[product_id]
                    item.quantity = quantity
                    item.save()
                else:
                  
                    OrderItem.objects.create(order=instance, product=product, quantity=quantity)

               

         

        return instance
    

# def update(self, instance, validated_data):
#         # Update order fields
#         instance.status = validated_data.get('status', instance.status)
#         instance.save()

#         # Update or create order items
#         order_items_data = validated_data.get("order_items")
#         if order_items_data is not None:  # Check if order_items_data is provided
#             # Get existing order items and their product IDs
#             existing_items = {item.product.id: item for item in instance.order_items.all()}
#             existing_item_product_ids = set(existing_items.keys())

#             # Get product IDs from the update data
#             updated_item_product_ids = set()
#             for item_data in order_items_data:
#                 product_id = item_data.get('product')
#                 quantity = item_data.get('quantity')

#                 if not product_id or not quantity:
#                      raise serializers.ValidationError(_("Each item must have a product ID and quantity."))

#                 try:
#                     product = Product.objects.get(id=product_id)
#                 except Product.DoesNotExist:
#                     raise serializers.ValidationError(_(f"Product with ID {product_id} does not exist."))

#                 # Validate quantity against stock (considering existing quantity in the order)
#                 current_item_quantity = existing_items[product_id].quantity if product_id in existing_items else 0
#                 # Adjust validation for updates: new quantity cannot exceed stock + current quantity
#                 if quantity > product.stock + current_item_quantity - (item_data.get('quantity') if product_id in existing_items else 0):
#                      raise serializers.ValidationError(_(f"Ordered quantity for product {product.name} is more than the stock."))


#                 # Check if the user is trying to add their own product
#                 request = self.context.get('request', None)
#                 if request and request.user == product.seller:
#                      raise PermissionDenied(_("Adding your own product to your order is not allowed"))


#                 if product_id in existing_items:
#                     # Update existing item
#                     item = existing_items[product_id]
#                     item.quantity = quantity
#                     item.save()
#                 else:
#                     # Create new item
#                     OrderItem.objects.create(order=instance, product=product, quantity=quantity)

#                 updated_item_product_ids.add(product_id)

#             # Delete items not present in the update data
#             items_to_delete_product_ids = existing_item_product_ids - updated_item_product_ids
#             for product_id in items_to_delete_product_ids:
#                 existing_items[product_id].delete()


#         return instance

