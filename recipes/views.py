from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View
from .models import Recipe, RecipeCategory
from .forms import SubscriptionForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from decimal import Decimal
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages

class SubscribeView(View):
    def post(self, request, *args, **kwargs):
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email') or request.POST.get('email')
            if email:
                subject = "Thank You for Subscribing to BlissBox!"
                message = "Thank you for subscribing! You’ll now receive recipe updates."
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email], fail_silently=False)
                messages.success(request, "Subscription successful! We've sent you a welcome email.")
                return redirect('recipes:home')
            messages.error(request, "Invalid email.")
            return redirect('recipes:home')
        messages.error(request, "Invalid email.")
        return redirect('recipes:home')

from django.views.generic import ListView, DetailView
from .models import Recipe, RecipeCategory
from django.db.models import Q, Count
from datetime import date

class RecipeListView(ListView):
    model = Recipe
    template_name = 'recipes/recipe_list.html'
    context_object_name = 'recipes'
    paginate_by = 12
    
    def get_queryset(self):
        return Recipe.objects.filter(is_published=True).prefetch_related('ingredients__ingredient')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = RecipeCategory.objects.all()
        return context

class RecipeDetailView(DetailView):
    model = Recipe
    template_name = 'recipes/recipe_detail.html'
    context_object_name = 'recipe'
    slug_field = 'slug'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recipe = self.get_object()
        context['nutritional_info'] = recipe.get_nutritional_info()
        return context


class ProductPageView(DetailView):
    """Product page view reusing Recipe model for product display.
    Renders `productpage.html` and provides the `recipe` in context.
    """
    model = Recipe
    template_name = 'productpage.html'
    context_object_name = 'recipe'
    slug_field = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # add any extra context if needed in future
        return context

class CategoryRecipesView(ListView):
    model = Recipe
    template_name = 'recipes/recipe_list.html'
    context_object_name = 'recipes'
    paginate_by = 12

    def get_queryset(self):
        self.category = get_object_or_404(RecipeCategory, slug=self.kwargs['slug'])
        return Recipe.objects.filter(category=self.category, is_published=True).prefetch_related('ingredients__ingredient')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = RecipeCategory.objects.all()
        context['current_category'] = self.category
        return context

class SearchRecipesView(ListView):
    model = Recipe
    template_name = 'recipes/recipe_list.html'
    context_object_name = 'recipes'
    paginate_by = 12

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Recipe.objects.filter(
                Q(name__icontains=query) | Q(description__icontains=query),
                is_published=True
            ).prefetch_related('ingredients__ingredient')
        return Recipe.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = RecipeCategory.objects.all()
        context['search_query'] = self.request.GET.get('q', '')
        return context


@method_decorator(csrf_exempt, name='dispatch')
class CalculatePriceView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            recipe_slug = data.get('recipe_slug')
            servings = int(data.get('servings', 1))
            excluded_ingredients = data.get('excluded_ingredients', [])
            
            # Get the recipe
            recipe = get_object_or_404(Recipe, slug=recipe_slug, is_published=True)
            
            # Calculate base price as sum of ingredient costs for servings
            base_price = recipe.get_total_cost_for_servings(servings)
            
            # Calculate savings from excluded ingredients
            savings = Decimal('0.00')
            if excluded_ingredients:
                for ingredient_id in excluded_ingredients:
                    # Accept either RecipeIngredient.id or Ingredient.id
                    try:
                        # First try Ingredient.id path
                        recipe_ingredient = recipe.ingredients.get(ingredient_id=ingredient_id)
                    except recipe.ingredients.model.DoesNotExist:
                        try:
                            # Fallback: RecipeIngredient.id
                            recipe_ingredient = recipe.ingredients.get(id=ingredient_id)
                        except recipe.ingredients.model.DoesNotExist:
                            continue
                    ingredient_price = recipe_ingredient.get_price_for_servings(servings)
                    savings += ingredient_price
            
            # Calculate final price
            final_price = base_price - savings
            if final_price < Decimal('0.00'):
                final_price = Decimal('0.00')
            
            return JsonResponse({
                'success': True,
                'base_price': float(base_price),
                'savings': float(savings),
                'final_price': float(final_price),
                'currency': '₹'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)
class ProductListView(ListView):
    model = Recipe
    template_name = 'recipes/product_list.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        qs = Recipe.objects.filter(is_published=True)

        categories = self.request.GET.getlist('category') or self.request.GET.get('categories', '').split(',')
        categories = [c for c in categories if c]
        if categories:
            qs = qs.filter(category__slug__in=categories)

        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        if min_price:
            try:
                qs = qs.filter(base_price__gte=min_price)
            except Exception:
                pass
        if max_price:
            try:
                qs = qs.filter(base_price__lte=max_price)
            except Exception:
                pass

        brand = self.request.GET.get('brand')
        if brand:
            qs = qs.filter(created_by__username__iexact=brand)

        available = self.request.GET.get('available')
        if available == '1':
            today = date.today()
            qs = qs.filter(
                Q(is_seasonal=False) |
                Q(available_from__lte=today, available_until__gte=today)
            )

        sort = self.request.GET.get('sort')
        if sort == 'price_asc':
            qs = qs.order_by('base_price')
        elif sort == 'price_desc':
            qs = qs.order_by('-base_price')
        elif sort == 'newest':
            qs = qs.order_by('-created_at')
        elif sort == 'best_selling':
            qs = qs.annotate(order_count=Count('orderitem')).order_by('-order_count', '-created_at')
        elif sort == 'rating':
            qs = qs.order_by('-created_at')
        elif sort == 'az':
            qs = qs.order_by('name')
        elif sort == 'za':
            qs = qs.order_by('-name')
        else:
            qs = qs.order_by('-created_at')

        return qs.select_related('category', 'created_by')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = RecipeCategory.objects.all()
        context['brands'] = Recipe.objects.filter(created_by__isnull=False).values_list('created_by__username', flat=True).distinct()
        context['selected'] = {
            'categories': self.request.GET.getlist('category') or self.request.GET.get('categories', '').split(','),
            'min_price': self.request.GET.get('min_price', ''),
            'max_price': self.request.GET.get('max_price', ''),
            'brand': self.request.GET.get('brand', ''),
            'available': self.request.GET.get('available', ''),
            'sort': self.request.GET.get('sort', 'newest'),
        }
        context['products_count'] = context['paginator'].count if context.get('paginator') else len(context['products'])
        context['querystring'] = self.request.GET.urlencode()
        return context
