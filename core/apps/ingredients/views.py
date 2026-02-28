from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from datetime import date
from core.apps.ingredients.models import Ingredient
from core.apps.ingredients.forms import IngredientCreateForm

class IngredientsListView(LoginRequiredMixin, ListView):
    model = Ingredient
    login_url = "/login/"
    template_name = "ingredients/all.html"
    context_object_name = "ingredients"

    def get(self, request, *args, **kwargs):
        if request.user.status != 'TC':
            return redirect('main-page')
        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['date'] = date.today()
        return context
    
class IngredientsCreateView(LoginRequiredMixin, CreateView):
    model = Ingredient
    login_url = '/login'
    form_class = IngredientCreateForm
    template_name = "ingredients/create.html"
    
    def get(self, request, *args, **kwargs):
        if request.user.status != "TC":
            return redirect('main-page')
        return super().get(request, *args, **kwargs)
    
    def form_valid(self, form):
        form.instance.amount = 0
        form.instance.save()

        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('ingredients-all')
