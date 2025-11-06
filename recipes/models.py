from django.db import models
from django.core.validators import MinValueValidator
from django.utils.text import slugify
from ingredients.models import Ingredient
from django.db.models import F, Sum
from decimal import Decimal

class RecipeCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = "Recipe Categories"
        ordering = ['name']
    
    def __str__(self):
        return self.name


class DietaryTag(models.Model):
    DIETARY_CHOICES = [
        ('vegan', 'Vegan'),
        ('gluten_free', 'Gluten Free'),
        ('dairy_free', 'Dairy Free'),
        ('nut_free', 'Nut Free'),
        ('low_sugar', 'Low Sugar'),
        ('keto', 'Keto'),
        ('paleo', 'Paleo'),
    ]
    
    name = models.CharField(max_length=50, choices=DIETARY_CHOICES, unique=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.get_name_display()


class Recipe(models.Model):
    DIFFICULTY_LEVELS = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    
    name = models.CharField(max_length=300)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    
    category = models.ForeignKey(
        RecipeCategory,
        on_delete=models.SET_NULL,
        null=True,
        related_name='recipes'
    )
    dietary_tags = models.ManyToManyField(DietaryTag, blank=True)
    difficulty = models.CharField(
        max_length=10,
        choices=DIFFICULTY_LEVELS,
        default='easy'
    )
    
    featured_image = models.ImageField(
        upload_to='recipes/',
        null=True,
        blank=True
    )
    
    instructions = models.TextField()
    prep_time_minutes = models.IntegerField(default=0)
    cook_time_minutes = models.IntegerField(default=0)
    
    # Servings
    default_servings = models.PositiveIntegerField(default=2)
    min_servings = models.PositiveIntegerField(default=1)
    max_servings = models.PositiveIntegerField(default=12)
    
    # Pricing
    base_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    
    # Availability
    is_published = models.BooleanField(default=False)
    is_seasonal = models.BooleanField(default=False)
    available_from = models.DateField(null=True, blank=True)
    available_until = models.DateField(null=True, blank=True)
    
    # Metadata
    created_by = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.SET_NULL,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['is_published', '-created_at']),
        ]
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    @property
    def total_time_minutes(self):
        return self.prep_time_minutes + self.cook_time_minutes
    
    @property
    def is_available_now(self):
        if not self.is_published:
            return False
        if not self.is_seasonal:
            return True
        
        from datetime import date
        today = date.today()
        if self.available_from and self.available_until:
            return self.available_from <= today <= self.available_until
        return True
    
    def get_nutritional_info(self, servings=None):
        if servings is None:
            servings = self.default_servings
        
        multiplier = Decimal(servings) / Decimal(self.default_servings)
        
        nutrients = self.ingredients.aggregate(
            total_calories=Sum(F('quantity') * F('ingredient__calories')),
            total_protein=Sum(F('quantity') * F('ingredient__protein_g')),
            total_fat=Sum(F('quantity') * F('ingredient__fat_g')),
            total_carbs=Sum(F('quantity') * F('ingredient__carbs_g')),
        )
        
        return {
            'calories': int((nutrients['total_calories'] or 0) * multiplier),
            'protein_g': float((nutrients['total_protein'] or 0) * multiplier),
            'fat_g': float((nutrients['total_fat'] or 0) * multiplier),
            'carbs_g': float((nutrients['total_carbs'] or 0) * multiplier),
        }


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredients'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.PROTECT,
        related_name='recipe_uses'
    )
    
    quantity = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        validators=[MinValueValidator(Decimal('0.001'))]
    )
    
    is_optional = models.BooleanField(default=False)
    notes = models.CharField(max_length=500, blank=True)
    
    class Meta:
        unique_together = ('recipe', 'ingredient')
        ordering = ['ingredient__name']
    
    def __str__(self):
        return f"{self.recipe.name} - {self.ingredient.name}"
    
    def get_price_for_servings(self, servings):
        multiplier = Decimal(servings) / Decimal(self.recipe.default_servings)
        adjusted_quantity = self.quantity * multiplier
        return self.ingredient.base_price_per_unit * adjusted_quantity