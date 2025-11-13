from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, View
from .models import Recipe, RecipeCategory
from .forms import SubscriptionForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from decimal import Decimal

class SubscribeView(View):
    def post(self, request, *args, **kwargs):
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            # Here you would typically save the email to a database
            # or a mailing list. For now, we'll just return a success message.
            return JsonResponse({'message': 'Subscription successful!'})
        return JsonResponse({'message': 'Invalid email.'}, status=400)

from django.views.generic import ListView, DetailView
from .models import Recipe, RecipeCategory
from django.db.models import Q

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
