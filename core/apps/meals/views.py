from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.dateparse import parse_date
from django.views.generic import ListView, DetailView, CreateView
from core.apps.meals.models import Day, Meal, UserMeal
from core.apps.items.models import Item, IngredientItem
from core.apps.ingredients.models import Ingredient
from django.http.response import Http404, HttpResponseRedirect
from datetime import date, timedelta, datetime
from core.apps.meals.forms import MealCreationForm
from core.apps.reports.models import MealReport
from django.contrib.auth.mixins import LoginRequiredMixin

class UserDashboard(LoginRequiredMixin, DetailView):
    model = Day
    template_name = "items/user.html"
    login_url = '/login/'
    context_object_name = "day"

    def get(self, request, *args, **kwargs):
        if request.user.status != "PT": 
            return redirect("main-page")
            
        return super().get(request, *args, **kwargs)

    def get_object(self, queryset=None):
        date_str = self.kwargs.get('date')
        
        if not date_str:
            raise Http404("Дата не указана")
        
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            raise Http404("Неверный формат даты")
        
        queryset = self.get_queryset()
        
        day, created = Day.objects.get_or_create(
            date=date_obj,
            defaults={'date': date_obj}
        )
        
        return day

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        day = self.get_object() 
        
        meals = Meal.objects.filter(day=day)
        try:
            dinner = meals.get(category="DN")
            items = dinner.items.all().prefetch_related('ingredients')
            context['dinner_allergies'] = []
            user_allergic_ingredient_ids = set(
                self.request.user.allergies.values_list('id', flat=True)
            )
            for item in items:
                item_ingredient_ids = set(
                    item.ingredients.values_list('id', flat=True)
                )
                
                dangerous_ingredient_ids = item_ingredient_ids.intersection(
                    user_allergic_ingredient_ids
                )
                
                if dangerous_ingredient_ids:
                    dangerous_ingredients = Ingredient.objects.filter(
                        id__in=dangerous_ingredient_ids
                    )
                    context['dinner_allergies'].append(dangerous_ingredients)
        except:
            dinner = []

    
        
        try:
            breakfast = meals.get(category="BF")
            items = breakfast.items.all().prefetch_related('ingredients')
            context['breakfast_allergies'] = []
            user_allergic_ingredient_ids = set(
                self.request.user.allergies.values_list('id', flat=True)
            )
            for item in items:
                item_ingredient_ids = set(
                    item.ingredients.values_list('id', flat=True)
                )
                
                dangerous_ingredient_ids = item_ingredient_ids.intersection(
                    user_allergic_ingredient_ids
                )
                
                if dangerous_ingredient_ids:
                    dangerous_ingredients = Ingredient.objects.filter(
                        id__in=dangerous_ingredient_ids
                    )
                    context['breakfast_allergies'].append(dangerous_ingredients)
        except:
            breakfast = []

        context['dinner_paid'] = False
        context['breakfast_paid'] = False

        if dinner and dinner.user.filter(id = self.request.user.id).exists():
            context['dinner_paid'] = True
            context['dinner_visited'] = UserMeal.objects.get(meal=dinner, user=self.request.user).is_given
            context['dinner_prepared'] = dinner.is_prepared
            print('dinner')
        if breakfast and breakfast.user.filter(id = self.request.user.id).exists():
            print('breakfast')
            context['breakfast_paid'] = True
            context['breakfast_visited'] = UserMeal.objects.get(meal=breakfast, user=self.request.user).is_given
            context['breakfast_prepared'] = breakfast.is_prepared
            print(breakfast.is_prepared)


        context['dinner'] = dinner
        context['breakfast'] = breakfast
        
        date_obj = day.date
        
        context['next_day_link'] = date_obj + timedelta(days=1)
        context['prev_day_link'] = date_obj - timedelta(days=1)
        
        context['user'] = self.request.user

        
        return context
    
class AdminDayDetailView(LoginRequiredMixin, DetailView):
    model = Day
    context_object_name = "day"
    login_url = '/login/'
    template_name = 'days/admin_list.html'

    def get(self, request, *args, **kwargs):
        if request.user.status != "TC":  
            return redirect("main-page")
            
        return super().get(request, *args, **kwargs)

    def get_object(self, queryset=None):  
        date_str = self.kwargs.get('date')
        
        if not date_str:
            raise Http404("Дата не указана")
        
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            raise Http404("Неверный формат даты")
        
        queryset = self.get_queryset()
        
        day, created = Day.objects.get_or_create(
            date=date_obj,
            defaults={'date': date_obj}
        )
        
        return day
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        day = self.get_object()

        try:
            dinner = Meal.objects.get(day=day, category='DN')
            context['dinner'] = dinner
            context['user_paid_dinner'] = UserMeal.objects.filter(meal = dinner).count()
        except:
            context['dinner'] = []

        try:
            breakfast = Meal.objects.get(day=day, category='BF')
            context['breakfast'] = breakfast
            context['user_paid_breakfast'] = UserMeal.objects.filter(meal = breakfast).count()
        except Exception as e:
            context['breakfast'] = []
            print(e)

        date_obj = day.date

        context['next_day_link'] = date_obj + timedelta(days=1)
        context['prev_day_link'] = date_obj - timedelta(days=1)
        return context
    

class MealCreateView(LoginRequiredMixin, CreateView):
    model = Meal
    form_class = MealCreationForm
    login_url = '/login/'
    template_name = 'meals/create.html'

    def form_valid(self, form):
        form.instance.day = Day.objects.get(pk=self.kwargs.get('day_pk'))
        form.instance.category = self.kwargs.get('category')
        
        self.object = form.save()

        if hasattr(form, 'save_m2m'):
            form.save_m2m()
        
        return super().form_valid(form)
    
    def get(self, request, *args, **kwargs):
        if request.user.status != "TC":
            return redirect('main-page')
        return super().get(request, *args, **kwargs)
    
    def get_success_url(self):
        day = Day.objects.get(pk=self.kwargs.get('day_pk'))
        return reverse('admin-day', kwargs={'date': day.date})
    

def prepare_meal(request, pk):
    if request.user.is_anonymous or request.user.status != 'TC':
        return HttpResponseRedirect(request.META["HTTP_REFERER"])
    meal = Meal.objects.get(pk=pk)
    meal.is_prepared = True
    meal.save()

    user_quantity = UserMeal.objects.filter(meal = meal).count()


    items: Item = meal.items.all()
    for item in items:
        ingredients = item.ingredients
        for ingredient in ingredients.all():
            amount = IngredientItem.objects.get(item=item, ingredient=ingredient).amount * user_quantity
            ingredient.amount -= amount
            ingredient.save()
            report = MealReport.objects.create(
                user = request.user,
                ingredient = ingredient,
                amount = amount
            )
            report.save()

    return HttpResponseRedirect(request.META["HTTP_REFERER"])

class UserMealListView(LoginRequiredMixin, ListView):
    model = UserMeal
    template_name="meals/abons.html"
    login_url = '/login/'
    context_object_name = "abons"

    def get(self, request, *args, **kwargs):
        if request.user.status != "PT":
            return redirect("main-page")
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset().filter(user=self.request.user)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['date'] = date.today()
        return context
    

def delete_meal(request, pk):
    if request.user.status == 'TC' and not request.user.status.is_anonymous:
        Meal.objects.get(pk=pk).delete()
    return HttpResponseRedirect(request.META["HTTP_REFERER"])

def pay_for_day(request, date, category):
    day = get_object_or_404(Day, date=date)
    meals = get_object_or_404(Meal, day=day, category=category)
    user = request.user
    if not meals.user.filter(id=user.id).exists() and not request.user.is_anonymous and request.user.status == 'PT':
        meals.user.add(request.user, through_defaults={'is_given': False})
    return HttpResponseRedirect(request.META["HTTP_REFERER"])

def return_day_payment(request, date, category):
    day = get_object_or_404(Day, date=date)
    meals = get_object_or_404(Meal, day=day, category=category)
    user = request.user
    if meals.user.filter(id=user.id).exists() and not request.user.is_anonymous and request.user.status == 'PT':
        meals.user.remove(request.user)
    return HttpResponseRedirect(request.META["HTTP_REFERER"])

def visit_meal(request, pk):
    meal = Meal.objects.get(pk=pk)
    if not request.user.is_anonymous and request.user.status == "PT" and UserMeal.objects.filter(meal=meal, user=request.user).exists():
        state = UserMeal.objects.get(user=request.user, meal=Meal.objects.get(pk=pk))
        state.is_given = True
        state.save()
    return HttpResponseRedirect(request.META["HTTP_REFERER"])