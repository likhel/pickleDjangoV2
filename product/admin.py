from django.contrib import admin
from .models import ProductCategory, Product


class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category_type', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('category_type',)
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "seller",
        "price",
        "stock",
        "available",
        "created_at",
    ]
    list_filter = ["available", "categories__name", "categories__category_type"]
    search_fields = ["name", "description", "ingredients"]
    prepopulated_fields = {"slug": ("name",)}
    ordering = ["-created_at"]
    filter_horizontal = ('categories',)
    raw_id_fields = ('seller',)


# Register ProductCategory with its own admin
admin.site.register(ProductCategory, ProductCategoryAdmin)
