from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal

class Ingredient(models.Model):
    UNIT_CHOICES = [
        ('g', 'Grams'),
        ('kg', 'Kilograms'),
        ('ml', 'Milliliters'),
        ('l', 'Liters'),
        ('cup', 'Cups'),
        ('tbsp', 'Tablespoons'),
        ('tsp', 'Teaspoons'),
        ('piece', 'Pieces'),
        ('slice', 'Slices'),
    ]
    
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    
    # Nutritional information per unit
    calories = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0,
        validators=[MinValueValidator(Decimal('0'))]
    )
    protein_g = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0,
        validators=[MinValueValidator(Decimal('0'))]
    )
    fat_g = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0,
        validators=[MinValueValidator(Decimal('0'))]
    )
    carbs_g = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0,
        validators=[MinValueValidator(Decimal('0'))]
    )
    
    # Pricing and availability
    base_price_per_unit = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    default_unit = models.CharField(
        max_length=10,
        choices=UNIT_CHOICES,
        default='g'
    )
    
    # Metadata
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Ingredient'
        verbose_name_plural = 'Ingredients'
    
    def __str__(self):
        return self.name
