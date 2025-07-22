from rest_framework import serializers
from .models import Product, ProductCategory



class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = "__all__" 
class ProductReadSerializer(serializers.ModelSerializer):
  
    seller = serializers.CharField(source="seller.get_full_name", read_only=True)
    category = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "seller",
            "category",
            "name",
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
            "category",
            "created_at",
            "updated_at",
        )

class ProductWriteSerializer(serializers.ModelSerializer):
   
    seller = serializers.HiddenField(default=serializers.CurrentUserDefault())
    category = ProductCategorySerializer()

    class Meta:
        model = Product
        fields = [
            "seller",
            "category",
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
        category_data = validated_data.pop('category')
        category_instance, created = ProductCategory.objects.get_or_create(
            **category_data
        )
        product = Product.objects.create(
            category=category_instance, **validated_data
        )
        return product

    def update(self, instance, validated_data):
        if 'category' in validated_data:
            category_data = validated_data.pop('category')
            category_serializer = self.fields['category']
            category_instance = instance.category
            category_serializer.update(category_instance, category_data)

        return super().update(instance, validated_data)
