from django import forms

from core.apps.ingredients.models import Ingredient
from core.apps.purchases.models import Purchase


class PurchaseCreateForm(forms.ModelForm):
    ingredient = forms.ModelChoiceField(
        queryset=Ingredient.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"}),)

    class Meta:
        model = Purchase
        fields = ["title", "amount", "ingredient"]
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Введите название"}
            ),
            "amount": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Введите количество"}
            ),
        }
