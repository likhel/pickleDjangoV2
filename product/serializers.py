from rest_framework import serializers
from .models import Product, ProductCategory

class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ["id", "name", "slug", "category_type"]

class ProductReadSerializer(serializers.ModelSerializer):
    """
    Serializer class for reading products
    """
    seller = serializers.CharField(source="seller.get_full_name", read_only=True)
    categories = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')

    class Meta:
        model = Product
        fields = [
            "id",
            "seller",
            "categories",
            "slug",
            "description",
            "ingredients",
            "price",
            "image",
            "stock",
            "available",
            "expiration_date",
            "created_at",
            "updated_at",
        ]
        read_only_fields = (
            "seller",
            "categories",
            "created_at",
            "updated_at",
        )

class ProductWriteSerializer(serializers.ModelSerializer):
    
    seller = serializers.HiddenField(default=serializers.CurrentUserDefault())
    categories = serializers.PrimaryKeyRelatedField(queryset=ProductCategory.objects.all(), many=True)

    class Meta:
        model = Product
        fields = [
            "seller",
            "categories",
            "name",
            "slug",
            "description",
            "ingredients",
            "price",
            "image",
            "stock",
            "available",
            "expiration_date",
        ]


    def create(self, validated_data):
        categories_data = validated_data.pop('categories')
        product = Product.objects.create(**validated_data)
        product.categories.set(categories_data)
        return product

    def update(self, instance, validated_data):
        if 'categories' in validated_data:
            categories_data = validated_data.pop('categories')
            instance.categories.set(categories_data)

        return super().update(instance, validated_data)

