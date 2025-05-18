from typing import Any
from django import forms
from django.core.exceptions import ValidationError
from django.forms import ClearableFileInput
from .models import Master, Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['client_name', 'text', 'rating', 'master', 'photo']
        # Поле is_published исключено из формы для обычных пользователей
        widgets = {
            'client_name': forms.TextInput(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control'}),
            'rating': forms.HiddenInput(attrs={'id': 'rating-value'}),  # Скрытое поле для рейтинга
            'master': forms.Select(attrs={'class': 'form-control'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }
        labels = {
            'client_name': 'Ваше имя',
            'text': 'Текст отзыва',
            'rating': 'Оценка',
            'master': 'Выберите мастера',
            'photo': 'Фотография (необязательно)',
        }
        help_texts = {
            'text': 'Расскажите о вашем опыте посещения барбершопа',
            'rating': 'Оцените качество услуги от 1 до 5',
            'photo': 'Вы можете прикрепить фотографию к отзыву',
        }

    def clean_text(self):
        text = self.cleaned_data.get('text')
        if len(text) < 10:
            raise forms.ValidationError('Текст отзыва должен содержать не менее 10 символов')
        return text

