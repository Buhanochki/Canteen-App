from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from core.apps.meals.models import Meal
from core.apps.reviews.models import Review
from core.apps.reviews.forms import ReviewForm


class MealReviews(LoginRequiredMixin, DetailView):
    model = Meal
    login_url = '/login/'
    template_name = 'reviews/list_reviews.html'
    context_object_name = "meal"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        meal = self.get_object()
        reviews = Review.objects.filter(meal=meal)
        
        context['reviews'] = reviews
        return context
    

class ReviewCreate(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    success_url = "/"
    login_url = '/login/'
    template_name = "reviews/create.html"

    def get(self, request, *args, **kwargs):
        if request.user.status != 'PT':
            return redirect('main-page')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['meal'] = Meal.objects.get(pk=self.kwargs.get('pk'))
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.meal = Meal.objects.get(pk=self.kwargs.get('pk'))
        form.instance.save()

        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy("reviews-view", kwargs = {'pk':Meal.objects.get(pk=self.kwargs.get('pk')).pk})
    

def delete_review(request, pk):
    review = Review.objects.get(pk = pk)
    if not request.user.is_anonymous and review.user == request.user:
        review.delete()

    return HttpResponseRedirect(request.META["HTTP_REFERER"])

