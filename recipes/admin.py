from django.contrib import admin
from .models import Recipe, RecipeCategory, DietaryTag, RecipeIngredient

@admin.register(RecipeCategory)
class RecipeCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(DietaryTag)
class DietaryTagAdmin(admin.ModelAdmin):
    list_display = ['name']

class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'is_published', 'base_price', 'created_at']
    list_filter = ['is_published', 'category', 'difficulty', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [RecipeIngredientInline]
    readonly_fields = ['created_at', 'updated_at']