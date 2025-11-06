#!/usr/bin/env python
import os
import django
import random
from decimal import Decimal

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blissbox.settings')
django.setup()

from recipes.models import Recipe, RecipeCategory, DietaryTag, RecipeIngredient
from ingredients.models import Ingredient
from django.contrib.auth.models import User

def create_comprehensive_data():
    print("Creating comprehensive Indian recipe data...")
    
    # Create additional categories
    categories_data = [
        {"name": "North Indian", "slug": "north-indian", "description": "Rich and flavorful North Indian cuisine"},
        {"name": "South Indian", "slug": "south-indian", "description": "Authentic South Indian dishes"},
        {"name": "Street Food", "slug": "street-food", "description": "Popular Indian street food"},
        {"name": "Festive Specials", "slug": "festive-specials", "description": "Special recipes for festivals"},
        {"name": "Quick Meals", "slug": "quick-meals", "description": "Fast and easy Indian recipes"},
        {"name": "Healthy Indian", "slug": "healthy-indian", "description": "Nutritious Indian dishes"},
    ]
    
    categories = {}
    for cat_data in categories_data:
        category, created = RecipeCategory.objects.get_or_create(
            slug=cat_data["slug"],
            defaults={
                "name": cat_data["name"],
                "description": cat_data["description"]
            }
        )
        categories[cat_data["slug"]] = category
        if created:
            print(f"Created category: {category.name}")
    
    # Create comprehensive ingredients with realistic Indian prices
    ingredients_data = [
        # Vegetables
        {"name": "Potato", "default_unit": "kg", "base_price_per_unit": Decimal("30.00"), "calories": 770, "protein_g": Decimal("20.0"), "carbs_g": Decimal("170.0"), "fat_g": Decimal("1.0")},
        {"name": "Onion", "default_unit": "kg", "base_price_per_unit": Decimal("40.00"), "calories": 400, "protein_g": Decimal("11.0"), "carbs_g": Decimal("93.0"), "fat_g": Decimal("1.0")},
        {"name": "Tomato", "default_unit": "kg", "base_price_per_unit": Decimal("35.00"), "calories": 180, "protein_g": Decimal("8.0"), "carbs_g": Decimal("38.0"), "fat_g": Decimal("2.0")},
        {"name": "Spinach", "default_unit": "g", "base_price_per_unit": Decimal("15.00"), "calories": 23, "protein_g": Decimal("2.9"), "carbs_g": Decimal("3.6"), "fat_g": Decimal("0.4")},
        {"name": "Cauliflower", "default_unit": "piece", "base_price_per_unit": Decimal("25.00"), "calories": 146, "protein_g": Decimal("11.0"), "carbs_g": Decimal("29.0"), "fat_g": Decimal("1.6")},
        {"name": "Green Peas", "default_unit": "kg", "base_price_per_unit": Decimal("80.00"), "calories": 810, "protein_g": Decimal("53.0"), "carbs_g": Decimal("145.0"), "fat_g": Decimal("4.0")},
        {"name": "Bell Pepper", "default_unit": "piece", "base_price_per_unit": Decimal("20.00"), "calories": 31, "protein_g": Decimal("1.0"), "carbs_g": Decimal("7.0"), "fat_g": Decimal("0.3")},
        {"name": "Carrot", "default_unit": "kg", "base_price_per_unit": Decimal("45.00"), "calories": 410, "protein_g": Decimal("9.0"), "carbs_g": Decimal("95.0"), "fat_g": Decimal("2.0")},
        {"name": "Green Beans", "default_unit": "kg", "base_price_per_unit": Decimal("60.00"), "calories": 347, "protein_g": Decimal("21.0"), "carbs_g": Decimal("78.0"), "fat_g": Decimal("1.2")},
        {"name": "Eggplant", "default_unit": "kg", "base_price_per_unit": Decimal("50.00"), "calories": 250, "protein_g": Decimal("9.8"), "carbs_g": Decimal("59.0"), "fat_g": Decimal("1.6")},
        
        # Proteins
        {"name": "Chicken Breast", "default_unit": "kg", "base_price_per_unit": Decimal("280.00"), "calories": 1650, "protein_g": Decimal("310.0"), "carbs_g": Decimal("0.0"), "fat_g": Decimal("35.0")},
        {"name": "Eggs", "default_unit": "dozen", "base_price_per_unit": Decimal("70.00"), "calories": 840, "protein_g": Decimal("72.0"), "carbs_g": Decimal("6.0"), "fat_g": Decimal("60.0")},
        {"name": "Paneer", "default_unit": "kg", "base_price_per_unit": Decimal("350.00"), "calories": 2650, "protein_g": Decimal("180.0"), "carbs_g": Decimal("50.0"), "fat_g": Decimal("220.0")},
        {"name": "Fish Fillet", "default_unit": "kg", "base_price_per_unit": Decimal("400.00"), "calories": 2060, "protein_g": Decimal("420.0"), "carbs_g": Decimal("0.0"), "fat_g": Decimal("44.0")},
        
        # Grains & Pulses
        {"name": "Basmati Rice", "default_unit": "kg", "base_price_per_unit": Decimal("120.00"), "calories": 3650, "protein_g": Decimal("68.0"), "carbs_g": Decimal("780.0"), "fat_g": Decimal("6.0")},
        {"name": "Wheat Flour", "default_unit": "kg", "base_price_per_unit": Decimal("35.00"), "calories": 3640, "protein_g": Decimal("130.0"), "carbs_g": Decimal("728.0"), "fat_g": Decimal("10.0")},
        {"name": "Toor Dal", "default_unit": "kg", "base_price_per_unit": Decimal("110.00"), "calories": 3430, "protein_g": Decimal("220.0"), "carbs_g": Decimal("630.0"), "fat_g": Decimal("15.0")},
        {"name": "Chana Dal", "default_unit": "kg", "base_price_per_unit": Decimal("90.00"), "calories": 3840, "protein_g": Decimal("250.0"), "carbs_g": Decimal("630.0"), "fat_g": Decimal("54.0")},
        {"name": "Moong Dal", "default_unit": "kg", "base_price_per_unit": Decimal("130.00"), "calories": 3470, "protein_g": Decimal("240.0"), "carbs_g": Decimal("630.0"), "fat_g": Decimal("12.0")},
        
        # Spices & Seasonings
        {"name": "Turmeric Powder", "default_unit": "g", "base_price_per_unit": Decimal("25.00"), "calories": 354, "protein_g": Decimal("7.8"), "carbs_g": Decimal("65.0"), "fat_g": Decimal("9.9")},
        {"name": "Cumin Seeds", "default_unit": "g", "base_price_per_unit": Decimal("45.00"), "calories": 375, "protein_g": Decimal("18.0"), "carbs_g": Decimal("44.0"), "fat_g": Decimal("22.0")},
        {"name": "Coriander Seeds", "default_unit": "g", "base_price_per_unit": Decimal("35.00"), "calories": 298, "protein_g": Decimal("12.0"), "carbs_g": Decimal("55.0"), "fat_g": Decimal("17.0")},
        {"name": "Garam Masala", "default_unit": "g", "base_price_per_unit": Decimal("80.00"), "calories": 379, "protein_g": Decimal("13.0"), "carbs_g": Decimal("63.0"), "fat_g": Decimal("15.0")},
        {"name": "Red Chili Powder", "default_unit": "g", "base_price_per_unit": Decimal("60.00"), "calories": 318, "protein_g": Decimal("12.0"), "carbs_g": Decimal("57.0"), "fat_g": Decimal("17.0")},
        {"name": "Mustard Seeds", "default_unit": "g", "base_price_per_unit": Decimal("40.00"), "calories": 508, "protein_g": Decimal("26.0"), "carbs_g": Decimal("28.0"), "fat_g": Decimal("36.0")},
        
        # Dairy & Oils
        {"name": "Ghee", "default_unit": "kg", "base_price_per_unit": Decimal("450.00"), "calories": 9000, "protein_g": Decimal("0.0"), "carbs_g": Decimal("0.0"), "fat_g": Decimal("1000.0")},
        {"name": "Vegetable Oil", "default_unit": "l", "base_price_per_unit": Decimal("120.00"), "calories": 8840, "protein_g": Decimal("0.0"), "carbs_g": Decimal("0.0"), "fat_g": Decimal("1000.0")},
        {"name": "Coconut Milk", "default_unit": "ml", "base_price_per_unit": Decimal("65.00"), "calories": 445, "protein_g": Decimal("4.6"), "carbs_g": Decimal("6.4"), "fat_g": Decimal("48.0")},
        
        # Nuts & Seeds
        {"name": "Cashew Nuts", "default_unit": "kg", "base_price_per_unit": Decimal("700.00"), "calories": 5530, "protein_g": Decimal("180.0"), "carbs_g": Decimal("300.0"), "fat_g": Decimal("440.0")},
        {"name": "Almonds", "default_unit": "kg", "base_price_per_unit": Decimal("800.00"), "calories": 5790, "protein_g": Decimal("210.0"), "carbs_g": Decimal("220.0"), "fat_g": Decimal("500.0")},
        {"name": "Raisins", "default_unit": "kg", "base_price_per_unit": Decimal("250.00"), "calories": 2990, "protein_g": Decimal("33.0"), "carbs_g": Decimal("790.0"), "fat_g": Decimal("0.5")},
        
        # Herbs & Aromatics
        {"name": "Ginger", "default_unit": "g", "base_price_per_unit": Decimal("20.00"), "calories": 80, "protein_g": Decimal("1.8"), "carbs_g": Decimal("18.0"), "fat_g": Decimal("0.8")},
        {"name": "Garlic", "default_unit": "g", "base_price_per_unit": Decimal("30.00"), "calories": 149, "protein_g": Decimal("6.4"), "carbs_g": Decimal("33.0"), "fat_g": Decimal("0.5")},
        {"name": "Green Chilies", "default_unit": "g", "base_price_per_unit": Decimal("25.00"), "calories": 40, "protein_g": Decimal("2.0"), "carbs_g": Decimal("9.5"), "fat_g": Decimal("0.2")},
        {"name": "Curry Leaves", "default_unit": "g", "base_price_per_unit": Decimal("10.00"), "calories": 23, "protein_g": Decimal("3.2"), "carbs_g": Decimal("2.2"), "fat_g": Decimal("0.6")},
        {"name": "Cilantro", "default_unit": "g", "base_price_per_unit": Decimal("15.00"), "calories": 23, "protein_g": Decimal("2.1"), "carbs_g": Decimal("3.7"), "fat_g": Decimal("0.5")},
    ]
    
    ingredients = {}
    for ing_data in ingredients_data:
        ingredient, created = Ingredient.objects.get_or_create(
            name=ing_data["name"],
            defaults={
                "base_price_per_unit": ing_data["base_price_per_unit"],
                "default_unit": ing_data["default_unit"],
                "calories": ing_data["calories"],
                "protein_g": ing_data["protein_g"],
                "carbs_g": ing_data["carbs_g"],
                "fat_g": ing_data["fat_g"],
                "description": f"Fresh {ing_data['name']} for cooking",
                "is_available": True
            }
        )
        ingredients[ing_data["name"]] = ingredient
        if created:
            print(f"Created ingredient: {ingredient.name} @ ₹{ingredient.base_price_per_unit}/{ingredient.default_unit}")
    
    # Create comprehensive Indian recipes with realistic prices
    recipes_data = [
        {
            "name": "Butter Chicken",
            "description": "Creamy and rich North Indian chicken curry with tender pieces of chicken in a tomato-based gravy",
            "category": "north-indian",
            "prep_time_minutes": 30,
            "cook_time_minutes": 45,
            "default_servings": 4,
            "min_servings": 2,
            "max_servings": 8,
            "difficulty": "medium",
            "base_price": Decimal("320.00"),
            "ingredients": [
                {"name": "Chicken Breast", "quantity": Decimal("0.8"), "unit": "kg"},
                {"name": "Tomato", "quantity": Decimal("0.5"), "unit": "kg"},
                {"name": "Onion", "quantity": Decimal("0.3"), "unit": "kg"},
                {"name": "Ginger", "quantity": Decimal("50"), "unit": "g"},
                {"name": "Garlic", "quantity": Decimal("30"), "unit": "g"},
                {"name": "Butter", "quantity": Decimal("100"), "unit": "g"},
                {"name": "Cream", "quantity": Decimal("200"), "unit": "ml"},
                {"name": "Garam Masala", "quantity": Decimal("20"), "unit": "g"},
                {"name": "Red Chili Powder", "quantity": Decimal("15"), "unit": "g"},
                {"name": "Cumin Seeds", "quantity": Decimal("10"), "unit": "g"},
                {"name": "Kasuri Methi", "quantity": Decimal("10"), "unit": "g"},
            ]
        },
        {
            "name": "Palak Paneer",
            "description": "Creamy spinach curry with soft paneer cubes, a popular North Indian vegetarian dish",
            "category": "north-indian",
            "prep_time_minutes": 20,
            "cook_time_minutes": 30,
            "default_servings": 4,
            "min_servings": 2,
            "max_servings": 6,
            "difficulty": "easy",
            "base_price": Decimal("280.00"),
            "ingredients": [
                {"name": "Paneer", "quantity": Decimal("0.4"), "unit": "kg"},
                {"name": "Spinach", "quantity": Decimal("0.8"), "unit": "kg"},
                {"name": "Onion", "quantity": Decimal("0.2"), "unit": "kg"},
                {"name": "Tomato", "quantity": Decimal("0.2"), "unit": "kg"},
                {"name": "Ginger", "quantity": Decimal("30"), "unit": "g"},
                {"name": "Garlic", "quantity": Decimal("20"), "unit": "g"},
                {"name": "Green Chilies", "quantity": Decimal("20"), "unit": "g"},
                {"name": "Cream", "quantity": Decimal("100"), "unit": "ml"},
                {"name": "Ghee", "quantity": Decimal("50"), "unit": "g"},
                {"name": "Garam Masala", "quantity": Decimal("15"), "unit": "g"},
                {"name": "Cumin Seeds", "quantity": Decimal("10"), "unit": "g"},
            ]
        },
        {
            "name": "Masala Dosa",
            "description": "Crispy rice crepe filled with spiced potato masala, served with chutney and sambar",
            "category": "south-indian",
            "prep_time_minutes": 45,
            "cook_time_minutes": 30,
            "default_servings": 4,
            "min_servings": 2,
            "max_servings": 8,
            "difficulty": "hard",
            "base_price": Decimal("180.00"),
            "ingredients": [
                {"name": "Rice", "quantity": Decimal("0.5"), "unit": "kg"},
                {"name": "Urad Dal", "quantity": Decimal("0.15"), "unit": "kg"},
                {"name": "Potato", "quantity": Decimal("0.5"), "unit": "kg"},
                {"name": "Onion", "quantity": Decimal("0.2"), "unit": "kg"},
                {"name": "Green Chilies", "quantity": Decimal("30"), "unit": "g"},
                {"name": "Mustard Seeds", "quantity": Decimal("10"), "unit": "g"},
                {"name": "Curry Leaves", "quantity": Decimal("2"), "unit": "bunch"},
                {"name": "Vegetable Oil", "quantity": Decimal("100"), "unit": "ml"},
                {"name": "Turmeric Powder", "quantity": Decimal("10"), "unit": "g"},
            ]
        },
        {
            "name": "Chole Bhature",
            "description": "Spicy chickpea curry served with fluffy fried bread, a North Indian street food favorite",
            "category": "street-food",
            "prep_time_minutes": 60,
            "cook_time_minutes": 45,
            "default_servings": 4,
            "min_servings": 2,
            "max_servings": 6,
            "difficulty": "medium",
            "base_price": Decimal("220.00"),
            "ingredients": [
                {"name": "Chickpeas", "quantity": Decimal("0.4"), "unit": "kg"},
                {"name": "Onion", "quantity": Decimal("0.3"), "unit": "kg"},
                {"name": "Tomato", "quantity": Decimal("0.2"), "unit": "kg"},
                {"name": "Ginger", "quantity": Decimal("40"), "unit": "g"},
                {"name": "Garlic", "quantity": Decimal("30"), "unit": "g"},
                {"name": "Green Chilies", "quantity": Decimal("25"), "unit": "g"},
                {"name": "Wheat Flour", "quantity": Decimal("0.3"), "unit": "kg"},
                {"name": "Garam Masala", "quantity": Decimal("20"), "unit": "g"},
                {"name": "Red Chili Powder", "quantity": Decimal("15"), "unit": "g"},
                {"name": "Cumin Seeds", "quantity": Decimal("15"), "unit": "g"},
                {"name": "Vegetable Oil", "quantity": Decimal("200"), "unit": "ml"},
            ]
        },
        {
            "name": "Hyderabadi Biryani",
            "description": "Aromatic rice dish with marinated chicken, saffron, and traditional spices",
            "category": "festive-specials",
            "prep_time_minutes": 90,
            "cook_time_minutes": 60,
            "default_servings": 6,
            "min_servings": 4,
            "max_servings": 10,
            "difficulty": "hard",
            "base_price": Decimal("450.00"),
            "ingredients": [
                {"name": "Basmati Rice", "quantity": Decimal("0.6"), "unit": "kg"},
                {"name": "Chicken", "quantity": Decimal("1.0"), "unit": "kg"},
                {"name": "Onion", "quantity": Decimal("0.5"), "unit": "kg"},
                {"name": "Ginger", "quantity": Decimal("60"), "unit": "g"},
                {"name": "Garlic", "quantity": Decimal("40"), "unit": "g"},
                {"name": "Green Chilies", "quantity": Decimal("40"), "unit": "g"},
                {"name": "Ghee", "quantity": Decimal("150"), "unit": "g"},
                {"name": "Saffron", "quantity": Decimal("2"), "unit": "g"},
                {"name": "Garam Masala", "quantity": Decimal("25"), "unit": "g"},
                {"name": "Cumin Seeds", "quantity": Decimal("20"), "unit": "g"},
                {"name": "Coriander Seeds", "quantity": Decimal("15"), "unit": "g"},
                {"name": "Yogurt", "quantity": Decimal("200"), "unit": "g"},
            ]
        },
        {
            "name": "Pav Bhaji",
            "description": "Mumbai's famous street food - mixed vegetable mash served with buttered bread rolls",
            "category": "street-food",
            "prep_time_minutes": 25,
            "cook_time_minutes": 35,
            "default_servings": 4,
            "min_servings": 2,
            "max_servings": 6,
            "difficulty": "easy",
            "base_price": Decimal("160.00"),
            "ingredients": [
                {"name": "Potato", "quantity": Decimal("0.4"), "unit": "kg"},
                {"name": "Cauliflower", "quantity": Decimal("0.3"), "unit": "piece"},
                {"name": "Green Peas", "quantity": Decimal("0.15"), "unit": "kg"},
                {"name": "Onion", "quantity": Decimal("0.3"), "unit": "kg"},
                {"name": "Tomato", "quantity": Decimal("0.4"), "unit": "kg"},
                {"name": "Bell Pepper", "quantity": Decimal("2"), "unit": "piece"},
                {"name": "Ginger", "quantity": Decimal("30"), "unit": "g"},
                {"name": "Garlic", "quantity": Decimal("20"), "unit": "g"},
                {"name": "Green Chilies", "quantity": Decimal("30"), "unit": "g"},
                {"name": "Pav Bhaji Masala", "quantity": Decimal("30"), "unit": "g"},
                {"name": "Butter", "quantity": Decimal("100"), "unit": "g"},
                {"name": "Cilantro", "quantity": Decimal("1"), "unit": "bunch"},
            ]
        },
        {
            "name": "Dal Tadka",
            "description": "Comforting yellow lentils tempered with aromatic spices and ghee",
            "category": "healthy-indian",
            "prep_time_minutes": 15,
            "cook_time_minutes": 40,
            "default_servings": 4,
            "min_servings": 2,
            "max_servings": 6,
            "difficulty": "easy",
            "base_price": Decimal("140.00"),
            "ingredients": [
                {"name": "Toor Dal", "quantity": Decimal("0.25"), "unit": "kg"},
                {"name": "Moong Dal", "quantity": Decimal("0.15"), "unit": "kg"},
                {"name": "Onion", "quantity": Decimal("0.2"), "unit": "kg"},
                {"name": "Tomato", "quantity": Decimal("0.2"), "unit": "kg"},
                {"name": "Ginger", "quantity": Decimal("25"), "unit": "g"},
                {"name": "Green Chilies", "quantity": Decimal("20"), "unit": "g"},
                {"name": "Ghee", "quantity": Decimal("60"), "unit": "g"},
                {"name": "Cumin Seeds", "quantity": Decimal("15"), "unit": "g"},
                {"name": "Mustard Seeds", "quantity": Decimal("10"), "unit": "g"},
                {"name": "Turmeric Powder", "quantity": Decimal("10"), "unit": "g"},
                {"name": "Red Chili Powder", "quantity": Decimal("10"), "unit": "g"},
                {"name": "Curry Leaves", "quantity": Decimal("1"), "unit": "bunch"},
            ]
        },
        {
            "name": "Vegetable Pulao",
            "description": "Fragrant basmati rice cooked with mixed vegetables and whole spices",
            "category": "quick-meals",
            "prep_time_minutes": 20,
            "cook_time_minutes": 25,
            "default_servings": 4,
            "min_servings": 2,
            "max_servings": 6,
            "difficulty": "easy",
            "base_price": Decimal("180.00"),
            "ingredients": [
                {"name": "Basmati Rice", "quantity": Decimal("0.4"), "unit": "kg"},
                {"name": "Carrot", "quantity": Decimal("0.2"), "unit": "kg"},
                {"name": "Green Peas", "quantity": Decimal("0.1"), "unit": "kg"},
                {"name": "Onion", "quantity": Decimal("0.2"), "unit": "kg"},
                {"name": "Bell Pepper", "quantity": Decimal("1"), "unit": "piece"},
                {"name": "Ghee", "quantity": Decimal("60"), "unit": "g"},
                {"name": "Cumin Seeds", "quantity": Decimal("10"), "unit": "g"},
                {"name": "Bay Leaves", "quantity": Decimal("4"), "unit": "piece"},
                {"name": "Cinnamon", "quantity": Decimal("5"), "unit": "g"},
                {"name": "Cardamom", "quantity": Decimal("5"), "unit": "g"},
                {"name": "Cloves", "quantity": Decimal("5"), "unit": "g"},
            ]
        },
        {
            "name": "Fish Curry",
            "description": "South Indian style fish curry in coconut-based gravy with tamarind and spices",
            "category": "south-indian",
            "prep_time_minutes": 25,
            "cook_time_minutes": 35,
            "default_servings": 4,
            "min_servings": 2,
            "max_servings": 6,
            "difficulty": "medium",
            "base_price": Decimal("380.00"),
            "ingredients": [
                {"name": "Fish Fillet", "quantity": Decimal("0.6"), "unit": "kg"},
                {"name": "Coconut Milk", "quantity": Decimal("2"), "unit": "can"},
                {"name": "Onion", "quantity": Decimal("0.3"), "unit": "kg"},
                {"name": "Tomato", "quantity": Decimal("0.2"), "unit": "kg"},
                {"name": "Ginger", "quantity": Decimal("40"), "unit": "g"},
                {"name": "Garlic", "quantity": Decimal("30"), "unit": "g"},
                {"name": "Green Chilies", "quantity": Decimal("30"), "unit": "g"},
                {"name": "Mustard Seeds", "quantity": Decimal("15"), "unit": "g"},
                {"name": "Cumin Seeds", "quantity": Decimal("10"), "unit": "g"},
                {"name": "Coriander Seeds", "quantity": Decimal("15"), "unit": "g"},
                {"name": "Turmeric Powder", "quantity": Decimal("10"), "unit": "g"},
                {"name": "Curry Leaves", "quantity": Decimal("2"), "unit": "bunch"},
            ]
        },
        {
            "name": "Aloo Gobi",
            "description": "Classic North Indian dry curry with potatoes and cauliflower, mildly spiced",
            "category": "healthy-indian",
            "prep_time_minutes": 15,
            "cook_time_minutes": 25,
            "default_servings": 4,
            "min_servings": 2,
            "max_servings": 6,
            "difficulty": "easy",
            "base_price": Decimal("120.00"),
            "ingredients": [
                {"name": "Potato", "quantity": Decimal("0.5"), "unit": "kg"},
                {"name": "Cauliflower", "quantity": Decimal("1"), "unit": "piece"},
                {"name": "Onion", "quantity": Decimal("0.2"), "unit": "kg"},
                {"name": "Tomato", "quantity": Decimal("0.2"), "unit": "kg"},
                {"name": "Ginger", "quantity": Decimal("25"), "unit": "g"},
                {"name": "Green Chilies", "quantity": Decimal("20"), "unit": "g"},
                {"name": "Vegetable Oil", "quantity": Decimal("60"), "unit": "ml"},
                {"name": "Cumin Seeds", "quantity": Decimal("10"), "unit": "g"},
                {"name": "Turmeric Powder", "quantity": Decimal("10"), "unit": "g"},
                {"name": "Red Chili Powder", "quantity": Decimal("10"), "unit": "g"},
                {"name": "Coriander Seeds", "quantity": Decimal("15"), "unit": "g"},
                {"name": "Cilantro", "quantity": Decimal("1"), "unit": "bunch"},
            ]
        },
    ]
    
    created_recipes = 0
    for recipe_data in recipes_data:
        category = categories.get(recipe_data["category"])
        
        recipe, created = Recipe.objects.get_or_create(
            slug=recipe_data["name"].lower().replace(" ", "-"),
            defaults={
                "name": recipe_data["name"],
                "description": recipe_data["description"],
                "category": category,
                "prep_time_minutes": recipe_data["prep_time_minutes"],
                "cook_time_minutes": recipe_data["cook_time_minutes"],
                "default_servings": recipe_data["default_servings"],
                "min_servings": recipe_data["min_servings"],
                "max_servings": recipe_data["max_servings"],
                "difficulty": recipe_data["difficulty"],
                "base_price": recipe_data["base_price"],
                "instructions": f"Follow the instructions to make delicious {recipe_data['name']}. This authentic Indian recipe serves {recipe_data['default_servings']} people.",
            }
        )
        
        if created:
            created_recipes += 1
            print(f"Created recipe: {recipe.name} @ ₹{recipe.base_price}")
            
            # Add ingredients to recipe
            for ing_data in recipe_data["ingredients"]:
                ingredient = ingredients.get(ing_data["name"])
                if ingredient:
                    RecipeIngredient.objects.get_or_create(
                        recipe=recipe,
                        ingredient=ingredient,
                        defaults={
                            "quantity": ing_data["quantity"]
                        }
                    )
    
    print(f"\nData creation completed!")
    print(f"Total recipes created: {created_recipes}")
    print(f"Total ingredients available: {len(ingredients)}")
    print(f"Total categories available: {len(categories)}")

if __name__ == "__main__":
    create_comprehensive_data()