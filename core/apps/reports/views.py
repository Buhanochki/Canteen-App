from django.shortcuts import render,redirect
from django.views.generic import ListView
from core.apps.reports.models import MealReport
from datetime import datetime, timedelta
from django.contrib.auth.mixins import LoginRequiredMixin

class MealReportListView(LoginRequiredMixin, ListView):
    model = MealReport
    login_url = '/login/'
    template_name = "reports/meal.html"
    context_object_name = 'reports'

    def get(self, request, *args, **kwargs):
        if request.user.status != "AD":
            return redirect('main-page')
        return super().get(request, *args, **kwargs)
    
    def get_queryset(self):
        return MealReport.objects.filter(date=self.kwargs.get('date'))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        date_obj = datetime.strptime(self.kwargs.get('date'), "%Y-%m-%d").date()
        context['date'] = date_obj
        context['prev_day_link'] = date_obj - timedelta(days=1)
        context['next_day_link'] = date_obj + timedelta(days=1)
        return context

