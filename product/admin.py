from django.contrib import admin
from .models import ProductCategory, Product

admin.site.register(ProductCategory)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "seller",
        "category",
        "price",
        "stock",
        "available",
        "created_at",
        "updated_at",
    ]
    list_filter = ["available", "created_at", "updated_at", "category", "seller"]
    search_fields = ["name", "description", "ingredients"]
    prepopulated_fields = {"slug": ("name",)}
    date_hierarchy = "created_at"
    ordering = ["-created_at"]
