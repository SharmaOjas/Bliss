#!/usr/bin/env python
import os
import django
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blissbox.settings')
django.setup()

from recipes.models import Recipe, RecipeCategory, RecipeIngredient
from ingredients.models import Ingredient


def reset_database_to_desserts():
    print("Resetting database to dessert-only data…")

    # Clear existing data (recipes first due to FK, then ingredients)
    RecipeIngredient.objects.all().delete()
    Recipe.objects.all().delete()
    Ingredient.objects.all().delete()

    # Ensure single 'Desserts' category
    desserts_cat, _ = RecipeCategory.objects.get_or_create(
        name='Desserts',
        defaults={'slug': 'desserts', 'description': 'Sweet treats and indulgent desserts'}
    )

    # Dessert-focused ingredients (prices in ₹ per default unit)
    dessert_ingredients = [
        {"name": "Dark Chocolate", "default_unit": "g", "base_price_per_unit": Decimal("2.50")},
        {"name": "Cocoa Powder", "default_unit": "g", "base_price_per_unit": Decimal("1.20")},
        {"name": "Butter", "default_unit": "g", "base_price_per_unit": Decimal("1.00")},
        {"name": "Sugar", "default_unit": "g", "base_price_per_unit": Decimal("0.40")},
        {"name": "Powdered Sugar", "default_unit": "g", "base_price_per_unit": Decimal("0.50")},
        {"name": "Flour", "default_unit": "g", "base_price_per_unit": Decimal("0.30")},
        {"name": "Eggs", "default_unit": "piece", "base_price_per_unit": Decimal("8.00")},
        {"name": "Vanilla Extract", "default_unit": "tsp", "base_price_per_unit": Decimal("15.00")},
        {"name": "Heavy Cream", "default_unit": "ml", "base_price_per_unit": Decimal("0.80")},
        {"name": "Mascarpone", "default_unit": "g", "base_price_per_unit": Decimal("1.80")},
        {"name": "Ladyfingers", "default_unit": "piece", "base_price_per_unit": Decimal("5.00")},
        {"name": "Espresso", "default_unit": "ml", "base_price_per_unit": Decimal("0.50")},
        {"name": "Cream Cheese", "default_unit": "g", "base_price_per_unit": Decimal("1.50")},
        {"name": "Gelatin", "default_unit": "g", "base_price_per_unit": Decimal("2.00")},
        {"name": "Milk", "default_unit": "ml", "base_price_per_unit": Decimal("0.30")},
        {"name": "Brown Sugar", "default_unit": "g", "base_price_per_unit": Decimal("0.45")},
    ]

    ing_map = {}
    for info in dessert_ingredients:
        ing = Ingredient.objects.create(
            name=info["name"],
            default_unit=info["default_unit"],
            base_price_per_unit=info["base_price_per_unit"],
            calories=0,
            protein_g=Decimal("0"),
            fat_g=Decimal("0"),
            carbs_g=Decimal("0"),
            is_available=True,
        )
        ing_map[ing.name] = ing
        print(f"✓ Ingredient: {ing.name} ({ing.base_price_per_unit}/{ing.default_unit})")

    # Helper to create a recipe with its ingredients
    def make_recipe(name, slug, description, instructions, base_price, default_servings, ingredients):
        recipe = Recipe.objects.create(
            name=name,
            slug=slug,
            description=description,
            instructions=instructions,
            prep_time_minutes=15,
            cook_time_minutes=20,
            default_servings=default_servings,
            min_servings=1,
            max_servings=12,
            base_price=base_price,
            difficulty='medium',
            category=desserts_cat,
            is_published=True,
        )
        for ing_name, qty in ingredients:
            RecipeIngredient.objects.create(
                recipe=recipe,
                ingredient=ing_map[ing_name],
                quantity=Decimal(str(qty)),
                is_optional=False,
            )
        print(f"✓ Recipe: {recipe.name}")
        return recipe

    # Dessert recipes
    make_recipe(
        name="Chocolate Lava Cake",
        slug="chocolate-lava-cake",
        description="Decadent chocolate cake with a molten center.",
        instructions="1. Melt chocolate and butter. 2. Whisk eggs and sugar. 3. Fold in flour. 4. Bake until edges set and center lava. 5. Serve warm.",
        base_price=Decimal("250.00"),
        default_servings=2,
        ingredients=[
            ("Dark Chocolate", 120),
            ("Butter", 80),
            ("Sugar", 80),
            ("Flour", 60),
            ("Eggs", 2),
            ("Vanilla Extract", 1),
        ],
    )

    make_recipe(
        name="Classic Tiramisu",
        slug="classic-tiramisu",
        description="Authentic Italian tiramisu with mascarpone and espresso.",
        instructions="1. Whip mascarpone and cream. 2. Dip ladyfingers in espresso. 3. Layer with cream. 4. Dust cocoa and chill.",
        base_price=Decimal("320.00"),
        default_servings=4,
        ingredients=[
            ("Mascarpone", 250),
            ("Heavy Cream", 200),
            ("Ladyfingers", 24),
            ("Espresso", 150),
            ("Sugar", 80),
            ("Cocoa Powder", 20),
            ("Vanilla Extract", 1),
        ],
    )

    make_recipe(
        name="New York Cheesecake",
        slug="new-york-cheesecake",
        description="Creamy baked cheesecake with a buttery crust.",
        instructions="1. Beat cream cheese and sugar. 2. Add eggs and vanilla. 3. Bake in water bath. 4. Chill before slicing.",
        base_price=Decimal("400.00"),
        default_servings=8,
        ingredients=[
            ("Cream Cheese", 600),
            ("Sugar", 150),
            ("Eggs", 3),
            ("Vanilla Extract", 2),
            ("Butter", 100),
            ("Flour", 50),
        ],
    )

    make_recipe(
        name="Chocolate Mousse",
        slug="chocolate-mousse",
        description="Silky chocolate mousse topped with whipped cream.",
        instructions="1. Melt chocolate. 2. Whip cream. 3. Fold chocolate into cream. 4. Chill and serve.",
        base_price=Decimal("220.00"),
        default_servings=4,
        ingredients=[
            ("Dark Chocolate", 150),
            ("Heavy Cream", 250),
            ("Sugar", 40),
            ("Vanilla Extract", 1),
        ],
    )

    make_recipe(
        name="Fudgy Brownies",
        slug="fudgy-brownies",
        description="Rich and fudgy brownies with crackly tops.",
        instructions="1. Melt chocolate and butter. 2. Mix sugar and eggs. 3. Fold flour and cocoa. 4. Bake until set.",
        base_price=Decimal("180.00"),
        default_servings=8,
        ingredients=[
            ("Dark Chocolate", 200),
            ("Butter", 120),
            ("Sugar", 180),
            ("Flour", 120),
            ("Cocoa Powder", 40),
            ("Eggs", 3),
        ],
    )

    make_recipe(
        name="Vanilla Panna Cotta",
        slug="vanilla-panna-cotta",
        description="Creamy Italian panna cotta with vanilla.",
        instructions="1. Bloom gelatin. 2. Heat milk, sugar, and vanilla. 3. Stir in gelatin and cream. 4. Chill until set.",
        base_price=Decimal("160.00"),
        default_servings=4,
        ingredients=[
            ("Milk", 300),
            ("Heavy Cream", 250),
            ("Sugar", 60),
            ("Vanilla Extract", 2),
            ("Gelatin", 8),
        ],
    )

    make_recipe(
        name="Crème Brûlée",
        slug="creme-brulee",
        description="Silky custard with caramelized sugar crust.",
        instructions="1. Heat cream and vanilla. 2. Whisk yolks and sugar. 3. Combine and bake in water bath. 4. Torch sugar topping.",
        base_price=Decimal("240.00"),
        default_servings=4,
        ingredients=[
            ("Heavy Cream", 400),
            ("Sugar", 100),
            ("Eggs", 4),
            ("Vanilla Extract", 2),
        ],
    )

    make_recipe(
        name="Red Velvet Cupcakes",
        slug="red-velvet-cupcakes",
        description="Velvety cupcakes with cream cheese frosting.",
        instructions="1. Mix dry and wet ingredients. 2. Bake cupcakes. 3. Frost with cream cheese icing.",
        base_price=Decimal("200.00"),
        default_servings=12,
        ingredients=[
            ("Flour", 250),
            ("Sugar", 180),
            ("Butter", 120),
            ("Eggs", 2),
            ("Vanilla Extract", 2),
            ("Cream Cheese", 200),
            ("Powdered Sugar", 100),
        ],
    )

    print("\nDessert-only reset complete.")


if __name__ == '__main__':
    reset_database_to_desserts()

