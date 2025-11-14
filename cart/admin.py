from django.contrib import admin
from .models import Cart, CartItem, Order, OrderItem

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'order_number', 'user', 'status', 'total', 'created_at'
    ]
    list_filter = ['status', 'created_at']
    search_fields = ['order_number', 'user__username', 'user__email']
    date_hierarchy = 'created_at'

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = [
        'order', 'recipe', 'servings', 'quantity', 'price'
    ]
    list_filter = ['order__status']
    search_fields = ['order__order_number', 'recipe__name']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'item_count', 'total_items', 'created_at']
    search_fields = ['user__username', 'user__email']

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'recipe', 'servings', 'quantity', 'customized_price']
    search_fields = ['recipe__name', 'cart__user__username']
