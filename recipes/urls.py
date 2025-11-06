from django.urls import path
from . import views

app_name = 'recipes'

urlpatterns = [
    path('', views.RecipeListView.as_view(), name='home'),
    path('recipe/<slug:slug>/', views.RecipeDetailView.as_view(), name='detail'),
    path('category/<slug:slug>/', views.CategoryRecipesView.as_view(), name='category'),
    path('search/', views.SearchRecipesView.as_view(), name='search'),
    path('subscribe/', views.SubscribeView.as_view(), name='subscribe'),
    path('calculate-price/', views.CalculatePriceView.as_view(), name='calculate-price'),
]