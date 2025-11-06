from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.CartView.as_view(), name='view'),
    path('add/<int:recipe_id>/', views.AddToCartView.as_view(), name='add'),
    path('remove/<int:item_id>/', views.RemoveFromCartView.as_view(), name='remove'),
    path('update/<int:item_id>/', views.UpdateCartItemView.as_view(), name='update'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
]
