from rest_framework import serializers
from .models import Wishlist
from product.serializers import ProductReadSerializer


class WishlistSerializer(serializers.ModelSerializer):
    """
    Serializer for Wishlist model
    """
    product = ProductReadSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Wishlist
        fields = ['id', 'product', 'product_id', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_product_id(self, value):
        """
        Validate that the product exists
        """
        from product.models import Product
        try:
            Product.objects.get(id=value)
        except Product.DoesNotExist:
            raise serializers.ValidationError("Product does not exist.")
        return value


class WishlistAddSerializer(serializers.Serializer):
    """
    Serializer for adding product to wishlist
    """
    product_id = serializers.IntegerField(required=True)

    def validate_product_id(self, value):
        """
        Validate that the product exists
        """
        from product.models import Product
        try:
            Product.objects.get(id=value)
        except Product.DoesNotExist:
            raise serializers.ValidationError("Product does not exist.")
        return value


