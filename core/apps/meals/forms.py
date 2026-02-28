from django import forms
from core.apps.meals.models import Meal
from core.apps.items.models import Item


class MealCreationForm(forms.ModelForm):
    items = forms.ModelMultipleChoiceField(
        queryset=Item.objects.all(),
        widget=forms.SelectMultiple(attrs={"class": "form-control"}),
    )
    cost = forms.IntegerField(
        widget=forms.NumberInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = Meal
        fields = ['items', 'cost']