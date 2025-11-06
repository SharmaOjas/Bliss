#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blissbox.settings')
django.setup()

from recipes.models import Recipe, RecipeCategory, RecipeIngredient
from ingredients.models import Ingredient
from users.models import CustomUser
from decimal import Decimal

def create_more_categories():
    """Create additional categories if they don't exist"""
    categories_data = [
        {'name': 'Lunch', 'description': 'Quick and healthy lunch options'},
        {'name': 'Dinner', 'description': 'Hearty dinner recipes for the whole family'},
        {'name': 'Desserts', 'description': 'Sweet treats and desserts'},
        {'name': 'Snacks', 'description': 'Quick snacks and appetizers'},
        {'name': 'Vegetarian', 'description': 'Plant-based vegetarian recipes'},
    ]
    
    created = []
    for cat_data in categories_data:
        try:
            # Check if category exists by name first
            category = RecipeCategory.objects.filter(name=cat_data['name']).first()
            if category:
                print(f"- Category already exists: {category.name}")
                continue
            
            # Try to create with unique slug
            slug = cat_data['name'].lower().replace(' ', '-')
            category = RecipeCategory.objects.create(
                name=cat_data['name'],
                slug=slug,
                description=cat_data['description']
            )
            created.append(category)
            print(f"✓ Created category: {category.name}")
            
        except Exception as e:
            print(f"  Error creating category '{cat_data['name']}': {e}")
    
    return created

def create_more_recipes():
    """Create more recipes using existing data"""
    
    # Get existing data
    categories = {cat.name: cat for cat in RecipeCategory.objects.all()}
    ingredients = {ing.name: ing for ing in Ingredient.objects.all()}
    
    print(f"Found categories: {list(categories.keys())}")
    print(f"Found ingredients: {list(ingredients.keys())}")
    
    # Sample recipe data using existing categories
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
            'category': 'Breakfast',  # Use existing category
            'ingredients': [
                ('Pasta', '200'),  # ingredient_name, quantity
                ('Tomatoes', '2'),
                ('Bell Peppers', '1'),
                ('Olive Oil', '3'),
                ('Salt', '1'),
                ('Black Pepper', '0.5')
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
                ('Bananas', '2'),
                ('Berries', '1'),
                ('Milk', '0.5'),
                ('Honey', '1')
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
            'category': 'Breakfast',
            'ingredients': [
                ('Greek Yogurt', '2'),
                ('Berries', '2'),
                ('Vanilla Extract', '1'),
                ('Honey', '2')
            ]
        }
    ]
    
    created_count = 0
    
    for recipe_data in recipes_data:
        try:
            # Get category
            category = categories.get(recipe_data['category'])
            if not category:
                print(f"  Warning: Category '{recipe_data['category']}' not found, skipping")
                continue
            
            # Create recipe with unique slug
            slug = recipe_data['name'].lower().replace(' ', '-')
            existing_recipe = Recipe.objects.filter(slug=slug).first()
            if existing_recipe:
                print(f"  Recipe '{recipe_data['name']}' already exists, skipping")
                continue
            
            recipe = Recipe.objects.create(
                name=recipe_data['name'],
                slug=slug,
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
            for ing_name, quantity in recipe_data['ingredients']:
                try:
                    ingredient = ingredients.get(ing_name)
                    if not ingredient:
                        print(f"  Warning: Ingredient '{ing_name}' not found, skipping")
                        continue
                    
                    RecipeIngredient.objects.create(
                        recipe=recipe,
                        ingredient=ingredient,
                        quantity=Decimal(quantity),
                        is_optional=False
                    )
                except Exception as e:
                    print(f"  Error adding ingredient '{ing_name}': {e}")
            
            created_count += 1
            print(f"✓ Created recipe: {recipe.name}")
            
        except Exception as e:
            print(f"  Error creating recipe '{recipe_data['name']}': {e}")
    
    print(f"\\nTotal recipes created: {created_count}")
    print(f"Total recipes now in database: {Recipe.objects.count()}")
    
    return created_count

def create_sample_users():
    """Create sample users if they don't exist"""
    users_data = [
        {'username': 'demo_user', 'email': 'demo@example.com', 'password': 'demo123'},
        {'username': 'foodie_jane', 'email': 'jane@example.com', 'password': 'foodie123'},
        {'username': 'chef_mike', 'email': 'mike@example.com', 'password': 'chef123'},
    ]
    
    created = []
    for user_data in users_data:
        try:
            user, is_new = CustomUser.objects.get_or_create(
                username=user_data['username'],
                defaults={'email': user_data['email']}
            )
            if is_new:
                user.set_password(user_data['password'])
                user.save()
                created.append(user)
                print(f"✓ Created user: {user.username}")
            else:
                print(f"- User already exists: {user.username}")
        except Exception as e:
            print(f"  Error creating user '{user_data['username']}': {e}")
    
    return created

if __name__ == '__main__':
    print("Adding more data to the database...")
    print("\\n1. Creating additional categories...")
    create_more_categories()
    
    print("\\n2. Creating more recipes...")
    create_more_recipes()
    
    print("\\n3. Creating sample users...")
    create_sample_users()
    
    print("\\n✓ Done! Check your website to see the new content.")