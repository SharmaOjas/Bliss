#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blissbox.settings')
django.setup()

from recipes.models import Recipe, RecipeCategory, RecipeIngredient
from ingredients.models import Ingredient
from users.models import CustomUser
from decimal import Decimal
import random

def create_more_recipes():
    """Create additional recipes using existing data"""
    
    # Get existing data
    categories = list(RecipeCategory.objects.all())
    ingredients = list(Ingredient.objects.all())
    
    if not categories:
        print("No categories found. Please create categories first.")
        return
    
    if not ingredients:
        print("No ingredients found. Please create ingredients first.")
        return
    
    # Sample recipe data
    recipes_data = [
        {
            'name': 'Mediterranean Pasta Salad',
            'description': 'Fresh and colorful pasta salad with Mediterranean flavors',
            'instructions': '1. Cook pasta according to package directions.\\n2. Chop vegetables into bite-sized pieces.\\n3. Mix cooked pasta with vegetables.\\n4. Add olive oil, salt, and pepper to taste.\\n5. Chill before serving.',
            'prep_time_minutes': 20,
            'cook_time_minutes': 15,
            'default_servings': 4,
            'min_servings': 2,
            'max_servings': 8,
            'base_price': Decimal('12.50'),
            'difficulty': 'easy',
            'category': 'Lunch',
            'ingredients': [
                ('Pasta', '200', 'g'),
                ('Tomatoes', '2', 'piece'),
                ('Bell Peppers', '1', 'piece'),
                ('Olive Oil', '3', 'tbsp'),
                ('Salt', '1', 'tsp'),
                ('Black Pepper', '0.5', 'tsp')
            ]
        },
        {
            'name': 'Classic Beef Stir-Fry',
            'description': 'Quick and flavorful beef stir-fry with vegetables',
            'instructions': '1. Slice beef into thin strips.\\n2. Heat oil in wok or large pan.\\n3. Stir-fry beef until browned.\\n4. Add vegetables and stir-fry for 5 minutes.\\n5. Season with salt and pepper.\\n6. Serve hot with rice.',
            'prep_time_minutes': 15,
            'cook_time_minutes': 10,
            'default_servings': 4,
            'min_servings': 2,
            'max_servings': 6,
            'base_price': Decimal('18.99'),
            'difficulty': 'medium',
            'category': 'Dinner',
            'ingredients': [
                ('Ground Beef', '500', 'g'),
                ('Bell Peppers', '2', 'piece'),
                ('Onions', '1', 'piece'),
                ('Olive Oil', '2', 'tbsp'),
                ('Salt', '1', 'tsp'),
                ('Black Pepper', '0.5', 'tsp')
            ]
        },
        {
            'name': 'Berry Smoothie Bowl',
            'description': 'Nutritious and colorful breakfast bowl with fresh berries',
            'instructions': '1. Blend bananas with a splash of milk until smooth.\\n2. Pour into bowl.\\n3. Top with berries and granola.\\n4. Drizzle with honey.\\n5. Serve immediately.',
            'prep_time_minutes': 10,
            'cook_time_minutes': 0,
            'default_servings': 2,
            'min_servings': 1,
            'max_servings': 4,
            'base_price': Decimal('6.99'),
            'difficulty': 'easy',
            'category': 'Breakfast',
            'ingredients': [
                ('Bananas', '2', 'piece'),
                ('Berries', '1', 'cup'),
                ('Milk', '0.5', 'cup'),
                ('Honey', '1', 'tbsp')
            ]
        },
        {
            'name': 'Cheesy Broccoli Rice',
            'description': 'Comforting and cheesy rice dish with broccoli',
            'instructions': '1. Cook rice according to package directions.\\n2. Steam broccoli until tender.\\n3. Mix cooked rice with broccoli.\\n4. Add cheese and butter.\\n5. Season with salt and pepper.\\n6. Bake until cheese melts.',
            'prep_time_minutes': 15,
            'cook_time_minutes': 25,
            'default_servings': 6,
            'min_servings': 4,
            'max_servings': 10,
            'base_price': Decimal('8.50'),
            'difficulty': 'easy',
            'category': 'Dinner',
            'ingredients': [
                ('White Rice', '2', 'cup'),
                ('Broccoli', '1', 'head'),
                ('Cheddar Cheese', '2', 'cup'),
                ('Butter', '3', 'tbsp'),
                ('Salt', '1', 'tsp'),
                ('Black Pepper', '0.5', 'tsp')
            ]
        },
        {
            'name': 'Vanilla Berry Parfait',
            'description': 'Elegant layered dessert with vanilla and berries',
            'instructions': '1. Layer Greek yogurt in glass.\\n2. Add layer of berries.\\n3. Sprinkle granola.\\n4. Repeat layers.\\n5. Top with honey and vanilla.\\n6. Chill before serving.',
            'prep_time_minutes': 15,
            'cook_time_minutes': 0,
            'default_servings': 4,
            'min_servings': 2,
            'max_servings': 8,
            'base_price': Decimal('7.99'),
            'difficulty': 'easy',
            'category': 'Desserts',
            'ingredients': [
                ('Greek Yogurt', '2', 'cup'),
                ('Berries', '2', 'cup'),
                ('Vanilla Extract', '1', 'tsp'),
                ('Honey', '2', 'tbsp')
            ]
        }
    ]
    
    created_count = 0
    
    for recipe_data in recipes_data:
        try:
            # Get category
            category = RecipeCategory.objects.get(name=recipe_data['category'])
            
            # Create recipe
            recipe = Recipe.objects.create(
                name=recipe_data['name'],
                slug=recipe_data['name'].lower().replace(' ', '-'),
                description=recipe_data['description'],
                instructions=recipe_data['instructions'],
                prep_time_minutes=recipe_data['prep_time_minutes'],
                cook_time_minutes=recipe_data['cook_time_minutes'],
                default_servings=recipe_data['default_servings'],
                min_servings=recipe_data['min_servings'],
                max_servings=recipe_data['max_servings'],
                base_price=recipe_data['base_price'],
                difficulty=recipe_data['difficulty'],
                category=category,
                is_published=True
            )
            
            # Add ingredients
            for ing_name, quantity, unit in recipe_data['ingredients']:
                try:
                    ingredient = Ingredient.objects.get(name=ing_name)
                    RecipeIngredient.objects.create(
                        recipe=recipe,
                        ingredient=ingredient,
                        quantity=Decimal(quantity),
                        unit=unit,
                        is_optional=False
                    )
                except Ingredient.DoesNotExist:
                    print(f"  Warning: Ingredient '{ing_name}' not found, skipping")
            
            created_count += 1
            print(f"✓ Created recipe: {recipe.name}")
            
        except RecipeCategory.DoesNotExist:
            print(f"  Warning: Category '{recipe_data['category']}' not found, skipping recipe '{recipe_data['name']}'")
        except Exception as e:
            print(f"  Error creating recipe '{recipe_data['name']}': {e}")
    
    print(f"\\nTotal recipes created: {created_count}")
    print(f"Total recipes now in database: {Recipe.objects.count()}")

if __name__ == '__main__':
    print("Adding more recipes to the database...")
    create_more_recipes()
    print("Done!")