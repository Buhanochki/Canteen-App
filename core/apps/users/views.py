from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView

from core.apps.users.models import CustomUser
from datetime import date

from core.apps.users.forms import ExtendedUserCreationForm, UserLoginForm, UserProfileUpdateForm


class UserLoginView(TemplateView):
    form_class = UserLoginForm
    template_name = "users/login.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        if not request.user.is_anonymous:
            return redirect("main-page")
        return render(request, self.template_name, context={"form": form})

    def post(self, request):
        form = self.form_class(data=request.POST)
        user_not_found = True
        if not request.user.is_anonymous:
            return redirect("main-page")
        elif form.is_valid():
            username = form.clean_username()
            password = form.clean_password()
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
            return redirect("main-page")
        form.fields["password"].widget.attrs.update({"class": "form-control is-invalid"})
        user_not_found = form.errors.get("__all__") is not None
        return render(
            request, self.template_name, context={"form": form, "user_not_found": user_not_found}
        )


def main_page(request):
    if request.user.is_anonymous:
        return redirect("login")
    elif request.user.status == "PT":
        return redirect("user-dashboard", date.today())
    elif request.user.status == "AD":
        return redirect('report-meal', date.today())
    return redirect("admin-dashboard")


def logout_user(request):
    logout(request)
    return redirect("login")


class UserRegistration(CreateView):
    form_class = ExtendedUserCreationForm
    template_name = "users/register.html"

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            user.save()
            login(request, user=user)
            return redirect("main-page")
        return render(request, self.template_name, context={"form": form})


class UserProfile(TemplateView):
    template_name = "users/user_profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        context["user"] = user
        return context

    def get(self, request):
        if request.user.is_anonymous:
            return redirect("login")
        return render(request, self.template_name)


class UserProfileUpdate(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = UserProfileUpdateForm
    template_name = "users/profile_update.html"
    context_object_name = "user"

    def get_context_data(self, **kwargs):
        context = super(UserProfileUpdate, self).get_context_data(**kwargs)
        return context

    def get_object(self, queryset=None):
        return get_object_or_404(CustomUser, id=self.request.user.id)

    def get_success_url(self):
        return reverse_lazy("user-profile")
