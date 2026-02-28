from django.shortcuts import HttpResponseRedirect, redirect
from django.views.generic import CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from core.apps.purchases.models import Purchase
from core.apps.purchases.forms import PurchaseCreateForm
from datetime import date



class PurchasesListView(LoginRequiredMixin, ListView):
    model = Purchase
    context_object_name = "purchases"
    login_url = '/login/'
    template_name = "purchases/view.html"

    def get(self, request, *args, **kwargs):
        if request.user.status == "TC":
            return super().get(request, *args, **kwargs)
        return redirect("main-page")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['date'] = date.today()
        return context

class PurchaseCreateView(LoginRequiredMixin, CreateView):
    model=Purchase
    template_name = "purchases/create.html"
    form_class=PurchaseCreateForm
    login_url = '/login/'
    success_url = 'view'

    def get(self, request, *args, **kwargs):
        if request.user.status != "TC":
            return redirect('main-page')
        return super().get(request, *args, **kwargs)
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.save()
        print(form.cleaned_data)
        return super().form_valid(form)
    
    
class PurchasesAdminListView(LoginRequiredMixin, ListView):
    model = Purchase
    context_object_name = "purchases"
    template_name = "purchases/admin_view.html"
    login_url = '/login/'

    def get(self, request, *args, **kwargs):
        if request.user.status != "AD":
            return redirect('main-page')
        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['date'] = date.today()

        return context

def purchase_approve(request, pk):
    if not request.user.is_anonymous and request.user.status == "AD":
        purchase = Purchase.objects.get(pk=pk)
        purchase.is_approved = True
        purchase.save()
        ingredient = purchase.ingredient
        ingredient.amount += purchase.amount
        ingredient.save()
    return HttpResponseRedirect(request.META["HTTP_REFERER"])


def purchase_delete(request, pk):
    if request.user.status == "TC" and not request.user.is_anonymous:
        object = Purchase.objects.get(pk=pk)
        object.delete()

        return HttpResponseRedirect(request.META["HTTP_REFERER"])
    return redirect("main-page")
