from django.contrib import admin
from .models import Ingredient

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ['name', 'default_unit', 'base_price_per_unit']
    list_filter = ['default_unit']
    search_fields = ['name']
    readonly_fields = ['created_at', 'updated_at']