from django.shortcuts import HttpResponseRedirect, redirect, render, get_object_or_404
from django.views.generic import DetailView, ListView, TemplateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from core.apps.items.models import Item, IngredientItem
from datetime import date

from core.apps.items.forms import ItemCreationForm, ItemUpdateForm
from core.apps.ingredients.models import Ingredient


class AdminItemsListView(LoginRequiredMixin, ListView):
    model = Item
    login_url = '/login/'
    template_name = "main_page/admin.html"
    context_object_name = "items"

    def get(self, request, *args, **kwargs):
        if not self.request.user.status == "TC":
            return redirect("user-dashboard")

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["items"] = Item.objects.prefetch_related('ingredientitem_set__ingredient').all()
        context["date"] = date.today()

        return context

class ItemCreateView(LoginRequiredMixin, TemplateView):
    template_name = "items/create.html"
    login_url = '/login/'
    
    def get(self, request, *args, **kwargs):
        if request.user.status != "TC":
            return redirect("main-page")
        
        ingredients = Ingredient.objects.all()
        
        form = ItemCreationForm(ingredients=ingredients)
        
        return render(request, self.template_name, {
            "form": form,
            "ingredients": ingredients
        })
    
    def post(self, request, *args, **kwargs):
        if request.user.status != "TC":
            return redirect("main-page")
        
        ingredients = Ingredient.objects.all()
        
        form = ItemCreationForm(request.POST, ingredients=ingredients)
        
        if form.is_valid():

            print(form.cleaned_data)
            title = form.cleaned_data['title']
            description = form.cleaned_data.get('description', '')
            
            item = Item.objects.create(
                title=title,
                description=description
            )

            for ingredient in ingredients:
                use_field = f'use_ingredient_{ingredient.id}'
                amount_field = f'amount_ingredient_{ingredient.id}'

                if form.cleaned_data.get(use_field):
                    amount = form.cleaned_data.get(amount_field, 1)
                    
                    if amount and amount >= 0:
                        if amount <= 1000:
                            IngredientItem.objects.create(
                                item=item,
                                ingredient=ingredient,
                                amount=amount
                            )
            
            return redirect("main-page")
        
        return render(request, self.template_name, {
            "form": form,
            "ingredients": ingredients
        })
    
class ItemUpdateView(LoginRequiredMixin, TemplateView):
    template_name = "items/update.html"
    login_url = '/login/'
    
    def get(self, request, pk):
        if request.user.status != "TC":
            return redirect("main-page")
        
        item = get_object_or_404(Item, id=pk)
        
        ingredients = []
        all_ingredients = Ingredient.objects.all()
        
        for ingredient in all_ingredients:
            try:
                ingredient_item = IngredientItem.objects.get(item=item, ingredient=ingredient)
                ingredients.append({
                    'id': ingredient.id,
                    'title': ingredient.title,
                    'amount': ingredient.amount,
                    'selected': True,
                    'selected_amount': ingredient_item.amount
                })
            except IngredientItem.DoesNotExist:
                ingredients.append({
                    'id': ingredient.id,
                    'title': ingredient.title,
                    'amount': ingredient.amount,
                    'selected': False,
                    'selected_amount': 1
                })
        
        return render(request, self.template_name, {
            'item': item,
            'ingredients': ingredients
        })
    
    def post(self, request, pk):
        if request.user.status != "TC":
            return redirect("main-page")
        
        item = get_object_or_404(Item, id=pk)
        
        item.title = request.POST.get('title')
        item.description = request.POST.get('description', '')
        item.save()
        
        IngredientItem.objects.filter(item=item).delete()
        
        for ingredient in Ingredient.objects.all():
            use_field = f'use_{ingredient.id}'
            amount_field = f'amount_{ingredient.id}'
            
            if request.POST.get(use_field) == 'on':
                amount = request.POST.get(amount_field, '1')
                try:
                    amount_int = int(amount)
                    if amount_int >= 0:
                        IngredientItem.objects.create(
                            item=item,
                            ingredient=ingredient,
                            amount=amount_int
                        )
                except ValueError:
                    pass
        
        return redirect('/')


class ItemDetailedView(LoginRequiredMixin, DetailView):
    model = Item
    template_name = "items/detailed.html"
    login_url =' /login/'
    context_object_name = "item"

def item_delete(request, pk):
    if request.user.status == "TC" and not request.user.is_anonymous:
        object = Item.objects.get(pk=pk)
        object.delete()

        return HttpResponseRedirect(request.META["HTTP_REFERER"])
    return redirect("main-page")
