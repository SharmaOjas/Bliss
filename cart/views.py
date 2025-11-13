from django.views.generic import View, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404, render
from django.http import JsonResponse
from django.contrib import messages
from django.db import transaction
from decimal import Decimal
from .models import Cart, CartItem, Order
from recipes.models import Recipe, RecipeIngredient


class CartView(LoginRequiredMixin, TemplateView):
    template_name = 'cart/cart.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Create cart if it doesn't exist
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        context['cart'] = cart
        return context


class AddToCartView(LoginRequiredMixin, View):
    def post(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, id=recipe_id)
        cart, _ = Cart.objects.get_or_create(user=request.user)
        
        servings = int(request.POST.get('servings', recipe.default_servings or 2))
        quantity = int(request.POST.get('quantity', 1))
        
        # Get and clean excluded ingredients - FILTER OUT EMPTY STRINGS
        excluded_ingredient_ids_raw = request.POST.getlist('excluded_ingredients')
        excluded_ingredient_ids = [int(val) for val in excluded_ingredient_ids_raw if val.isdigit()]
        
        try:
            with transaction.atomic():
                # Step 1: Create or get CartItem WITHOUT M2M fields in defaults
                item, created = CartItem.objects.get_or_create(
                    cart=cart,
                    recipe=recipe,
                    defaults={
                        'servings': servings,
                        'quantity': quantity,
                        'original_price': recipe.base_price,
                        'customized_price': recipe.base_price  # Initial value
                    }
                )
                
                if not created:
                    # For existing items, update basic fields first
                    item.quantity += quantity
                    item.servings = servings
                    # Save basic fields before M2M operations
                    item.save(update_fields=['quantity', 'servings'])
                
                # Step 2: Handle excluded ingredients consistently (after item has an ID)
                # Always clear existing exclusions so unchecking boxes is respected
                if not item.pk:
                    item.save()
                item.excluded_ingredients.clear()

                # Add new exclusions if any (only valid numeric IDs)
                added_count = 0
                for ingredient_id in excluded_ingredient_ids:
                    try:
                        recipe_ingredient = RecipeIngredient.objects.get(id=ingredient_id)
                        # Verify it belongs to this recipe
                        if recipe_ingredient.recipe == recipe:
                            item.excluded_ingredients.add(recipe_ingredient)
                            added_count += 1
                    except RecipeIngredient.DoesNotExist:
                        # Ignore invalid ingredient IDs
                        continue

                if added_count > 0:
                    messages.info(request, f'{added_count} ingredients excluded from {recipe.name}.')
                
                # Step 3: Recalculate price after exclusions (now safe after M2M)
                item.calculate_customized_price()
                item.save(update_fields=['customized_price', 'original_price'])
            
            # Success messages
            if created:
                messages.success(request, f'{recipe.name} added to your cart!')
            else:
                messages.info(request, f'{recipe.name} quantity updated in your cart!')
            
        except Exception as e:
            messages.error(request, f'Error adding to cart: {str(e)}')
            return redirect('recipes:home')  # or wherever you want to redirect on error
        
        return redirect('cart:view')


class RemoveFromCartView(LoginRequiredMixin, View):
    def post(self, request, item_id):
        try:
            item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
            recipe_name = item.recipe.name
            item.delete()
            messages.success(request, f'{recipe_name} removed from cart.')
        except Exception as e:
            messages.error(request, f'Error removing item: {str(e)}')
        
        return redirect('cart:view')


class UpdateCartItemView(LoginRequiredMixin, View):
    def post(self, request, item_id):
        try:
            item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
            quantity = int(request.POST.get('quantity', item.quantity))
            servings = int(request.POST.get('servings', item.servings))
            
            # Get and clean excluded ingredients
            excluded_ingredient_ids_raw = request.POST.getlist('excluded_ingredients')
            excluded_ingredient_ids = [int(val) for val in excluded_ingredient_ids_raw if val.isdigit()]
            
            # Update basic fields first
            item.quantity = quantity
            item.servings = servings
            item.save(update_fields=['quantity', 'servings'])
            
            # Handle excluded ingredients: always clear, then re-add any provided
            item.excluded_ingredients.clear()
            added_count = 0
            for ingredient_id in excluded_ingredient_ids:
                try:
                    recipe_ingredient = RecipeIngredient.objects.get(id=ingredient_id)
                    if recipe_ingredient.recipe == item.recipe:
                        item.excluded_ingredients.add(recipe_ingredient)
                        added_count += 1
                except RecipeIngredient.DoesNotExist:
                    continue

            if added_count > 0:
                messages.info(request, f'Updated {added_count} exclusions for {item.recipe.name}.')
            
            # Recalculate price
            item.calculate_customized_price()
            item.save(update_fields=['customized_price', 'original_price'])
            
            if quantity > 0:
                messages.info(request, f'{item.recipe.name} updated.')
            else:
                recipe_name = item.recipe.name
                item.delete()
                messages.success(request, f'{recipe_name} removed from cart.')
                
        except Exception as e:
            messages.error(request, f'Error updating cart: {str(e)}')
        
        return redirect('cart:view')


class CheckoutView(LoginRequiredMixin, View):
    def get(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        if cart.items.count() == 0:
            messages.warning(request, 'Your cart is empty.')
            return redirect('cart:view')
        
        # TODO: Render checkout template with address form
        # For now, show a simple checkout page
        from django.shortcuts import render
        return render(request, 'cart/checkout.html', {
            'cart': cart,
            'subtotal': cart.total_price,
            'shipping': Decimal('50.00'),
            'tax': Decimal('0.00'),
            'total': cart.total_price + Decimal('50.00')
        })
    
    def post(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        if cart.items.count() == 0:
            messages.warning(request, 'Your cart is empty.')
            return redirect('cart:view')
        
        # Get form data
        delivery_address = request.POST.get('delivery_address', '').strip()
        delivery_date_str = request.POST.get('delivery_date')
        
        if not delivery_address:
            messages.error(request, 'Please provide a delivery address.')
            return redirect('cart:checkout')
        
        delivery_date = None
        if delivery_date_str:
            from datetime import datetime, date
            try:
                delivery_date = datetime.strptime(delivery_date_str, '%Y-%m-%d').date()
                if delivery_date < date.today():
                    messages.error(request, 'Delivery date must be today or in the future.')
                    return redirect('cart:checkout')
            except ValueError:
                messages.error(request, 'Invalid delivery date format. Use YYYY-MM-DD.')
                return redirect('cart:checkout')
        
        # Calculate totals
        subtotal = cart.total_price
        tax = Decimal('0.00')  # TODO: Calculate tax
        shipping = Decimal('50.00')  # TODO: Calculate shipping
        total = subtotal + tax + shipping
        
        try:
            with transaction.atomic():
                # Create order
                order = Order.objects.create(
                    user=request.user,
                    subtotal=subtotal,
                    tax=tax,
                    shipping=shipping,
                    total=total,
                    delivery_address=delivery_address,
                    delivery_date=delivery_date
                )
                
                # Create order items
                for cart_item in cart.items.all():
                    OrderItem.objects.create(
                        order=order,
                        recipe=cart_item.recipe,
                        servings=cart_item.servings,
                        quantity=cart_item.quantity,
                        excluded_ingredients=','.join([str(ri.id) for ri in cart_item.excluded_ingredients.all()]),
                        price=cart_item.customized_price
                    )
                
                # Clear cart
                cart.items.all().delete()
                
            messages.success(request, f'Order #{order.order_number} created successfully! Total: ₹{total}')
            return redirect('users:order_history')
            
        except Exception as e:
            messages.error(request, f'Error creating order: {str(e)}')
            return redirect('cart:checkout')
