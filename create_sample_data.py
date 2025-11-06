#!/usr/bin/env python
import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blissbox.settings')
django.setup()

from django.contrib.auth.models import User
from recipes.models import Recipe, RecipeCategory, RecipeIngredient
from ingredients.models import Ingredient
from users.models import CustomUser
from cart.models import Cart, CartItem
from cart.models import Cart, CartItem, Order, OrderItem
from decimal import Decimal
import random
from datetime import date, timedelta

def create_categories():
    categories = [
        {'name': 'Breakfast', 'description': 'Start your day with delicious breakfast recipes'},
        {'name': 'Lunch', 'description': 'Hearty and satisfying lunch options'},
        {'name': 'Dinner', 'description': 'Perfect dinner recipes for any occasion'},
        {'name': 'Desserts', 'description': 'Sweet treats and indulgent desserts'},
        {'name': 'Snacks', 'description': 'Quick and tasty snack recipes'},
        {'name': 'Beverages', 'description': 'Refreshing drinks and smoothies'},
        {'name': 'Vegetarian', 'description': 'Plant-based vegetarian recipes'},
        {'name': 'Quick Meals', 'description': 'Fast and easy recipes for busy days'},
        {'name': 'Healthy', 'description': 'Nutritious and wholesome recipes'},
        {'name': 'International', 'description': 'Recipes from around the world'},
    ]
    
    created_categories = []
    for cat_data in categories:
        try:
            category, created = RecipeCategory.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            created_categories.append(category)
            print(f"Category '{category.name}' {'created' if created else 'already exists'}")
        except Exception as e:
            print(f"Error creating category '{cat_data['name']}': {e}")
            # Try to get existing category
            try:
                category = RecipeCategory.objects.get(name=cat_data['name'])
                created_categories.append(category)
                print(f"Using existing category '{category.name}'")
            except:
                pass
    
    return created_categories

def create_ingredients():
    ingredients = [
        # Proteins
        {'name': 'Chicken Breast', 'default_unit': 'kg', 'base_price_per_unit': Decimal('8.99'), 'calories': 165, 'protein_g': 31, 'fat_g': 3.6, 'carbs_g': 0},
        {'name': 'Ground Beef', 'default_unit': 'kg', 'base_price_per_unit': Decimal('12.99'), 'calories': 250, 'protein_g': 26, 'fat_g': 15, 'carbs_g': 0},
        {'name': 'Salmon Fillet', 'default_unit': 'kg', 'base_price_per_unit': Decimal('24.99'), 'calories': 208, 'protein_g': 25, 'fat_g': 12, 'carbs_g': 0},
        {'name': 'Eggs', 'default_unit': 'piece', 'base_price_per_unit': Decimal('0.30'), 'calories': 70, 'protein_g': 6, 'fat_g': 5, 'carbs_g': 1},
        {'name': 'Greek Yogurt', 'default_unit': 'cup', 'base_price_per_unit': Decimal('1.99'), 'calories': 130, 'protein_g': 20, 'fat_g': 0, 'carbs_g': 9},
        
        # Vegetables
        {'name': 'Tomatoes', 'default_unit': 'kg', 'base_price_per_unit': Decimal('3.99'), 'calories': 18, 'protein_g': 0.9, 'fat_g': 0.2, 'carbs_g': 3.9},
        {'name': 'Onions', 'default_unit': 'kg', 'base_price_per_unit': Decimal('2.49'), 'calories': 40, 'protein_g': 1.1, 'fat_g': 0.1, 'carbs_g': 9.3},
        {'name': 'Bell Peppers', 'default_unit': 'piece', 'base_price_per_unit': Decimal('1.99'), 'calories': 31, 'protein_g': 1, 'fat_g': 0.3, 'carbs_g': 7.3},
        {'name': 'Broccoli', 'default_unit': 'kg', 'base_price_per_unit': Decimal('3.49'), 'calories': 34, 'protein_g': 2.8, 'fat_g': 0.4, 'carbs_g': 7},
        {'name': 'Spinach', 'default_unit': 'kg', 'base_price_per_unit': Decimal('4.99'), 'calories': 23, 'protein_g': 2.9, 'fat_g': 0.4, 'carbs_g': 3.6},
        
        # Grains & Pasta
        {'name': 'White Rice', 'default_unit': 'cup', 'base_price_per_unit': Decimal('0.50'), 'calories': 205, 'protein_g': 4.3, 'fat_g': 0.4, 'carbs_g': 45},
        {'name': 'Brown Rice', 'default_unit': 'cup', 'base_price_per_unit': Decimal('0.65'), 'calories': 216, 'protein_g': 5, 'fat_g': 1.8, 'carbs_g': 45},
        {'name': 'Pasta', 'default_unit': 'g', 'base_price_per_unit': Decimal('0.02'), 'calories': 131, 'protein_g': 5, 'fat_g': 1.1, 'carbs_g': 25},
        
        # Dairy & Cheese
        {'name': 'Milk', 'default_unit': 'cup', 'base_price_per_unit': Decimal('0.75'), 'calories': 149, 'protein_g': 8, 'fat_g': 8, 'carbs_g': 12},
        {'name': 'Butter', 'default_unit': 'tbsp', 'base_price_per_unit': Decimal('0.25'), 'calories': 102, 'protein_g': 0.1, 'fat_g': 12, 'carbs_g': 0},
        {'name': 'Cheddar Cheese', 'default_unit': 'cup', 'base_price_per_unit': Decimal('3.99'), 'calories': 403, 'protein_g': 25, 'fat_g': 33, 'carbs_g': 1.3},
        
        # Herbs & Spices
        {'name': 'Olive Oil', 'default_unit': 'tbsp', 'base_price_per_unit': Decimal('0.35'), 'calories': 119, 'protein_g': 0, 'fat_g': 14, 'carbs_g': 0},
        {'name': 'Salt', 'default_unit': 'tsp', 'base_price_per_unit': Decimal('0.05'), 'calories': 0, 'protein_g': 0, 'fat_g': 0, 'carbs_g': 0},
        {'name': 'Black Pepper', 'default_unit': 'tsp', 'base_price_per_unit': Decimal('0.10'), 'calories': 6, 'protein_g': 0.2, 'fat_g': 0.1, 'carbs_g': 1.5},
        
        # Fruits
        {'name': 'Bananas', 'default_unit': 'piece', 'base_price_per_unit': Decimal('0.35'), 'calories': 105, 'protein_g': 1.3, 'fat_g': 0.4, 'carbs_g': 27},
        {'name': 'Apples', 'default_unit': 'piece', 'base_price_per_unit': Decimal('0.99'), 'calories': 95, 'protein_g': 0.5, 'fat_g': 0.3, 'carbs_g': 25},
        {'name': 'Berries', 'default_unit': 'cup', 'base_price_per_unit': Decimal('3.99'), 'calories': 84, 'protein_g': 1.1, 'fat_g': 0.5, 'carbs_g': 21},
        
        # Baking & Sweeteners
        {'name': 'Sugar', 'default_unit': 'cup', 'base_price_per_unit': Decimal('0.50'), 'calories': 774, 'protein_g': 0, 'fat_g': 0, 'carbs_g': 200},
        {'name': 'Flour', 'default_unit': 'cup', 'base_price_per_unit': Decimal('0.25'), 'calories': 364, 'protein_g': 10, 'fat_g': 1, 'carbs_g': 76},
        {'name': 'Vanilla Extract', 'default_unit': 'tsp', 'base_price_per_unit': Decimal('0.30'), 'calories': 12, 'protein_g': 0, 'fat_g': 0, 'carbs_g': 0.5},
        {'name': 'Honey', 'default_unit': 'tbsp', 'base_price_per_unit': Decimal('0.40'), 'calories': 64, 'protein_g': 0.1, 'fat_g': 0, 'carbs_g': 17},
    ]
    
    created_ingredients = []
    for ing_data in ingredients:
        ingredient, created = Ingredient.objects.get_or_create(
            name=ing_data['name'],
            defaults={
                'default_unit': ing_data['default_unit'],
                'base_price_per_unit': ing_data['base_price_per_unit'],
                'calories': ing_data['calories'],
                'protein_g': ing_data['protein_g'],
                'fat_g': ing_data['fat_g'],
                'carbs_g': ing_data['carbs_g'],
                'is_available': True
            }
        )
        created_ingredients.append(ingredient)
        print(f"Ingredient '{ingredient.name}' {'created' if created else 'already exists'}")
    
    return created_ingredients

def create_recipes(categories, ingredients):
    recipes_data = [
        {
            'name': 'Classic Pancakes',
            'description': 'Fluffy homemade pancakes perfect for weekend breakfast',
            'prep_time_minutes': 15,
            'cook_time_minutes': 20,
            'default_servings': 4,
            'min_servings': 2,
            'max_servings': 8,
            'instructions': '1. Mix dry ingredients in a bowl. 2. In another bowl, whisk eggs, milk, and melted butter. 3. Combine wet and dry ingredients. 4. Cook on hot griddle until bubbles form. 5. Flip and cook until golden brown.',
            'base_price': Decimal('12.99'),
            'is_published': True,
            'category_name': 'Breakfast',
            'ingredients': [
                ('Flour', 1.5, 'cup'),
                ('Eggs', 2, 'piece'),
                ('Milk', 1.25, 'cup'),
                ('Butter', 3, 'tbsp'),
                ('Sugar', 2, 'tbsp'),
                ('Salt', 0.5, 'tsp'),
            ]
        },
        {
            'name': 'Grilled Chicken Salad',
            'description': 'Healthy and protein-rich salad with grilled chicken and fresh vegetables',
            'prep_time_minutes': 20,
            'cook_time_minutes': 15,
            'default_servings': 2,
            'min_servings': 1,
            'max_servings': 4,
            'instructions': '1. Season and grill chicken breast. 2. Let chicken rest, then slice. 3. Wash and chop vegetables. 4. Mix greens with vegetables. 5. Top with sliced chicken and dressing.',
            'base_price': Decimal('18.99'),
            'is_published': True,
            'category_name': 'Lunch',
            'ingredients': [
                ('Chicken Breast', 0.5, 'kg'),
                ('Spinach', 2, 'bunch'),
                ('Tomatoes', 2, 'piece'),
                ('Bell Peppers', 1, 'piece'),
                ('Olive Oil', 2, 'tbsp'),
                ('Salt', 1, 'tsp'),
                ('Black Pepper', 0.5, 'tsp'),
            ]
        },
        {
            'name': 'Beef Stir Fry',
            'description': 'Quick and flavorful Asian-inspired beef stir fry',
            'prep_time_minutes': 10,
            'cook_time_minutes': 15,
            'default_servings': 4,
            'min_servings': 2,
            'max_servings': 6,
            'instructions': '1. Slice beef thinly against the grain. 2. Heat wok or large pan. 3. Stir-fry beef until browned. 4. Add vegetables and stir-fry. 5. Add sauce and serve over rice.',
            'base_price': Decimal('24.99'),
            'is_published': True,
            'category_name': 'Dinner',
            'ingredients': [
                ('Ground Beef', 0.5, 'kg'),
                ('Broccoli', 1, 'head'),
                ('Onions', 1, 'piece'),
                ('Garlic', 3, 'clove'),
                ('Olive Oil', 2, 'tbsp'),
                ('Brown Rice', 2, 'cup'),
            ]
        },
        {
            'name': 'Chocolate Chip Cookies',
            'description': 'Classic homemade chocolate chip cookies',
            'prep_time_minutes': 15,
            'cook_time_minutes': 12,
            'default_servings': 24,
            'min_servings': 12,
            'max_servings': 48,
            'instructions': '1. Cream butter and sugars. 2. Beat in eggs and vanilla. 3. Mix in flour gradually. 4. Stir in chocolate chips. 5. Drop spoonfuls on baking sheet. 6. Bake at 375°F for 10-12 minutes.',
            'base_price': Decimal('8.99'),
            'is_published': True,
            'category_name': 'Desserts',
            'ingredients': [
                ('Flour', 2.25, 'cup'),
                ('Butter', 1, 'cup'),
                ('Sugar', 0.75, 'cup'),
                ('Eggs', 2, 'piece'),
                ('Vanilla Extract', 2, 'tsp'),
                ('Salt', 1, 'tsp'),
            ]
        },
        {
            'name': 'Greek Yogurt Parfait',
            'description': 'Healthy and delicious breakfast or snack parfait',
            'prep_time_minutes': 5,
            'cook_time_minutes': 0,
            'default_servings': 1,
            'min_servings': 1,
            'max_servings': 4,
            'instructions': '1. Layer yogurt in a glass. 2. Add berries. 3. Sprinkle granola. 4. Drizzle honey. 5. Repeat layers. 6. Serve immediately.',
            'base_price': Decimal('6.99'),
            'is_published': True,
            'category_name': 'Breakfast',
            'ingredients': [
                ('Greek Yogurt', 1, 'cup'),
                ('Berries', 0.5, 'cup'),
                ('Honey', 1, 'tbsp'),
            ]
        },
        {
            'name': 'Salmon Teriyaki',
            'description': 'Delicious Japanese-style salmon with teriyaki glaze',
            'prep_time_minutes': 10,
            'cook_time_minutes': 15,
            'default_servings': 2,
            'min_servings': 1,
            'max_servings': 4,
            'instructions': '1. Pat salmon dry and season. 2. Mix teriyaki sauce ingredients. 3. Pan-sear salmon skin-side down. 4. Flip and brush with sauce. 5. Glaze until caramelized. 6. Serve with steamed rice.',
            'base_price': Decimal('32.99'),
            'is_published': True,
            'category_name': 'Dinner',
            'ingredients': [
                ('Salmon Fillet', 0.4, 'kg'),
                ('White Rice', 1, 'cup'),
                ('Garlic', 2, 'clove'),
                ('Honey', 2, 'tbsp'),
            ]
        },
    ]
    
    created_recipes = []
    for recipe_data in recipes_data:
        # Get category
        category = RecipeCategory.objects.get(name=recipe_data['category_name'])
        
        # Create recipe
        recipe, created = Recipe.objects.get_or_create(
            name=recipe_data['name'],
            defaults={
                'description': recipe_data['description'],
                'prep_time_minutes': recipe_data['prep_time_minutes'],
                'cook_time_minutes': recipe_data['cook_time_minutes'],
                'default_servings': recipe_data['default_servings'],
                'min_servings': recipe_data['min_servings'],
                'max_servings': recipe_data['max_servings'],
                'instructions': recipe_data['instructions'],
                'base_price': recipe_data['base_price'],
                'is_published': recipe_data['is_published'],
                'category': category,
                'difficulty': 'easy'
            }
        )
        
        if created:
            # Add ingredients
            for ing_name, quantity, unit in recipe_data['ingredients']:
                ingredient = Ingredient.objects.get(name=ing_name)
                RecipeIngredient.objects.get_or_create(
                    recipe=recipe,
                    ingredient=ingredient,
                    defaults={
                        'quantity': quantity,
                        'is_optional': False
                    }
                )
            
            print(f"Recipe '{recipe.name}' created successfully")
        else:
            print(f"Recipe '{recipe.name}' already exists")
        
        created_recipes.append(recipe)
    
    return created_recipes

def create_sample_users():
    users_data = [
        {'username': 'demo_user', 'email': 'demo@blissbox.com', 'password': 'demo123', 'first_name': 'Demo', 'last_name': 'User'},
        {'username': 'foodie_jane', 'email': 'jane@example.com', 'password': 'foodie123', 'first_name': 'Jane', 'last_name': 'Smith'},
        {'username': 'chef_mike', 'email': 'mike@example.com', 'password': 'chef123', 'first_name': 'Mike', 'last_name': 'Johnson'},
    ]
    
    created_users = []
    for user_data in users_data:
        user, created = CustomUser.objects.get_or_create(
            username=user_data['username'],
            defaults={
                'email': user_data['email'],
                'first_name': user_data['first_name'],
                'last_name': user_data['last_name']
            }
        )
        
        if created:
            user.set_password(user_data['password'])
            user.save()
            print(f"User '{user.username}' created successfully")
        else:
            print(f"User '{user.username}' already exists")
        
        created_users.append(user)
    
    return created_users

def main():
    print("Creating sample data for BlissBox...")
    print("=" * 50)
    
    try:
        # Create categories
        print("\n1. Creating categories...")
        categories = create_categories()
        
        # Create ingredients
        print("\n2. Creating ingredients...")
        ingredients = create_ingredients()
        
        # Create recipes
        print("\n3. Creating recipes...")
        recipes = create_recipes(categories, ingredients)
        
        # Create users
        print("\n4. Creating users...")
        users = create_users()
        
        print("\n" + "=" * 50)
        print("Sample data creation completed!")
        print(f"Categories: {len(categories)}")
        print(f"Ingredients: {len(ingredients)}")
        print(f"Recipes: {len(recipes)}")
        print(f"Users: {len(users)}")
        print("\nYou can now log in with:")
        print("- Username: demo_user, Password: demo123")
        print("- Username: foodie_jane, Password: foodie123")
        print("- Username: chef_mike, Password: chef123")
        
    except Exception as e:
        print(f"Error during data creation: {e}")
        print("Continuing with available data...")

if __name__ == '__main__':
    main()