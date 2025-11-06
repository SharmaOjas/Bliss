from django.shortcuts import render, redirect
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CustomUserCreationForm
from .models import Pantry
from cart.models import Order

class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'users/register.html'
    success_url = '/users/login/'

class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    redirect_authenticated_user = True
    next_page = 'users:dashboard'

class CustomLogoutView(LogoutView):
    next_page = '/'

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'users/dashboard.html'

class PantryView(LoginRequiredMixin, TemplateView):
    template_name = 'users/pantry.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pantry'] = Pantry.objects.get(user=self.request.user)
        return context

class OrdersView(LoginRequiredMixin, TemplateView):
    template_name = 'users/orders.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders'] = Order.objects.filter(user=self.request.user)
        return context
