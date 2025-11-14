from django.db import models
from recipes.models import Recipe, RecipeIngredient
from decimal import Decimal
import uuid


class Cart(models.Model):
    user = models.OneToOneField(
        'users.CustomUser',
        on_delete=models.CASCADE,
        related_name='cart'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Cart for {self.user.username}"
    
    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())
    
    @property
    def item_count(self):
        return self.items.count()
    
    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE
    )
    
    servings = models.PositiveIntegerField(default=2)
    excluded_ingredients = models.ManyToManyField(
        RecipeIngredient,
        blank=True,
        related_name='excluded_in_cart_items'
    )
    
    original_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    customized_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    
    quantity = models.PositiveIntegerField(default=1)
    
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('cart', 'recipe')
    
    def __str__(self):
        return f"{self.recipe.name} (x{self.quantity})"
    
    @property
    def total_price(self):
        return self.customized_price * self.quantity
    
    def calculate_customized_price(self):
        """Calculate price based on servings and excluded ingredients"""
        if not self.recipe:
            self.customized_price = Decimal('0.00')
            return self.customized_price
        
        # Calculate base price as sum of ingredient costs for current servings
        base_price = self.recipe.get_total_cost_for_servings(self.servings)
        
        # Calculate excluded ingredients cost (only if item is saved and has M2M)
        excluded_cost = Decimal('0')
        if self.pk:  # Only access M2M if object is saved
            try:
                for excluded_item in self.excluded_ingredients.all():
                    excluded_cost += excluded_item.get_price_for_servings(self.servings)
            except Exception:
                # If M2M access fails, use base price only
                pass
        
        # Final customized price (minimum 0.01 to avoid zero price issues)
        self.customized_price = max(base_price - excluded_cost, Decimal('0.01'))
        # Keep original_price in sync with the full ingredient total for transparency
        self.original_price = base_price
        return self.customized_price

    def save(self, *args, **kwargs):
        """Override save to handle price calculation safely"""
        # Only calculate customized price if we have the necessary data
        if self.recipe:
            # Set original price if not set
            if not self.original_price:
                self.original_price = self.recipe.base_price
            
            # For new objects, set initial customized price without M2M
            if self.pk is None:
                # Initial save - no M2M yet
                if not self.customized_price:
                    self.customized_price = self.recipe.base_price
            else:
                # Update - can safely calculate with M2M
                self.calculate_customized_price()
        
        super().save(*args, **kwargs)


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.SET_NULL,
        null=True,
        related_name='orders'
    )
    
    order_number = models.CharField(max_length=50, unique=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    shipping = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    total = models.DecimalField(max_digits=10, decimal_places=2)
    
    delivery_address = models.CharField(max_length=500)
    delivery_date = models.DateField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def save(self, *args, **kwargs):
        if not self.order_number:
            import uuid
            self.order_number = f"ORD-{uuid.uuid4().hex[:8].upper()}"
        
        if self.pk is None:  # New order
            self.total = self.subtotal + self.tax + self.shipping
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Order {self.order_number}"

    @property
    def total_amount(self):
        return self.total


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.SET_NULL,
        null=True
    )
    
    servings = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField(default=1)
    excluded_ingredients = models.TextField(blank=True)  # Store as comma-separated IDs
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.recipe.name} - Order {self.order.order_number}"
