from django import forms

from core.apps.ingredients.models import Ingredient

class IngredientCreateForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    class Meta:
        model = Ingredient
        fields = ['title']