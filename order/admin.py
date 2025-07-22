from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0 # Don't show extra blank forms

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'buyer', 'status', 'total_cost', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('buyer__username', 'id')
    inlines = [OrderItemInline]

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'quantity', 'cost')
    list_filter = ('order__status', 'product__category')
    search_fields = ('order__buyer__username', 'product__name')


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)

