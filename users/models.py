from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from ingredients.models import Ingredient
from recipes.models import DietaryTag
from decimal import Decimal

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True)
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return self.username

class UserProfile(models.Model):
    user = models.OneToOneField(
        'users.CustomUser',
        on_delete=models.CASCADE,
        related_name='profile'
    )
    
    dietary_restrictions = models.ManyToManyField(
        DietaryTag,
        blank=True,
        related_name='users_with_restriction'
    )
    preferred_servings = models.PositiveIntegerField(default=2)
    
    address_line1 = models.CharField(max_length=255, blank=True)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    
    phone_number = models.CharField(max_length=20, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"


class Pantry(models.Model):
    user = models.OneToOneField(
        'users.CustomUser',
        on_delete=models.CASCADE,
        related_name='pantry'
    )
    last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s Pantry"
    
    def get_total_items(self):
        return self.ingredients.count()


class PantryIngredient(models.Model):
    pantry = models.ForeignKey(
        Pantry,
        on_delete=models.CASCADE,
        related_name='ingredients'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='pantry_items'
    )
    
    quantity_available = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        validators=[MinValueValidator(Decimal('0.001'))]
    )
    
    date_added = models.DateTimeField(auto_now_add=True)
    date_expires = models.DateField(null=True, blank=True)
    
    class Meta:
        unique_together = ('pantry', 'ingredient')
        verbose_name_plural = 'Pantry Ingredients'
    
    def __str__(self):
        return f"{self.pantry.user.username} - {self.ingredient.name}"
    
    @property
    def is_expired(self):
        if self.date_expires:
            from datetime import date
            return date.today() > self.date_expires
        return False