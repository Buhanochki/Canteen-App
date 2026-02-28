from django import forms

from core.apps.items.models import Item, IngredientItem
from core.apps.ingredients.models import Ingredient


class ItemCreationForm(forms.Form):
    # Основные поля
    title = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Название блюда',
        required=True
    )
    
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        label='Описание',
        required=False
    )
    
    # Метод для создания полей динамически
    def __init__(self, *args, **kwargs):
        # Получаем ингредиенты из kwargs или запрашиваем из БД
        ingredients = kwargs.pop('ingredients', None)
        super().__init__(*args, **kwargs)
        
        if ingredients is None:
            ingredients = Ingredient.objects.all()
        
        # Создаем поле для каждого ингредиента
        for ingredient in ingredients:
            # Чекбокс для выбора ингредиента
            self.fields[f'use_ingredient_{ingredient.id}'] = forms.BooleanField(
                required=False,
                widget=forms.CheckboxInput(attrs={
                    'class': 'form-check-input',
                    'id': f'use_ing_{ingredient.id}'
                }),
                label=f'Использовать {ingredient.title}',
                initial=False
            )
            
            # Поле для количества
            self.fields[f'amount_ingredient_{ingredient.id}'] = forms.IntegerField(
                required=False,
                min_value=1,
                max_value=1000,
                initial=1,
                widget=forms.NumberInput(attrs={
                    'class': 'form-control',
                    'id': f'amount_ing_{ingredient.id}'
                }),
                label='Количество'
            )

class ItemUpdateForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['title', 'description']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Получаем ингредиенты с предзаполненными значениями
        if self.instance.pk:
            # Получаем существующие связи
            existing_items = IngredientItem.objects.filter(item=self.instance)
            existing_dict = {ii.ingredient_id: ii.amount for ii in existing_items}
        
        ingredients = Ingredient.objects.all()
        for ingredient in ingredients:
            # Чекбокс
            is_checked = ingredient.id in existing_dict if self.instance.pk else False
            self.fields[f'use_ingredient_{ingredient.id}'] = forms.BooleanField(
                required=False,
                initial=is_checked,
                widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
            )
            
            # Количество
            initial_amount = existing_dict.get(ingredient.id, 1) if self.instance.pk else 1
            self.fields[f'amount_ingredient_{ingredient.id}'] = forms.IntegerField(
                required=False,
                initial=initial_amount,
                min_value=1,
                widget=forms.NumberInput(attrs={'class': 'form-control'})
            )
    
    def save(self, commit=True):
        item = super().save(commit=commit)
        
        if commit:
            # Удаляем старые связи
            IngredientItem.objects.filter(item=item).delete()
            
            # Создаем новые
            for ingredient in Ingredient.objects.all():
                if self.cleaned_data.get(f'use_ingredient_{ingredient.id}'):
                    amount = self.cleaned_data.get(f'amount_ingredient_{ingredient.id}', 1)
                    if amount:
                        IngredientItem.objects.create(
                            item=item,
                            ingredient=ingredient,
                            amount=amount
                        )
        return item
