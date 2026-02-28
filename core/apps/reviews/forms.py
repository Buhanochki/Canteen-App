from django import forms
from core.apps.reviews.models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text', 'rate']  # Только эти поля, без user и meal
        widgets = {
            'text': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Оставьте ваш отзыв здесь...',
                'class': 'form-control'
            }),
            'rate': forms.Select(attrs={
                'class': 'form-select'
            })
        }
        labels = {
            'text': 'Текст отзыва',
            'rate': 'Оценка'
        }