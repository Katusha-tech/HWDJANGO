# Импорт служебных объектов Form
from typing import Any
from django import forms
from django.core.exceptions import ValidationError
from django.forms import ClearableFileInput
from .models import Service, Master, Order, Review

class ReviewForm(forms.ModelForm):
    """
    Форма для создания отзыва о мастере с использованием Bootstrap 5
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Добавляем класс form-control к каждому полю формы
        for field_name, field in self.fields.items():
            if (
                field_name != "rating"
            ):  # Для рейтинга будет специальная обработка через JS
                field.widget.attrs.update({"class": "form-control"})

    # Скрытое поле для рейтинга, которое будет заполняться через JS
    rating = forms.IntegerField(
        widget=forms.HiddenInput(),
        required=True,
    )

    class Meta:
        model = Review
        # Исключаем поле is_published из формы для пользователей
        exclude = ["is_published"]
        widgets = {
            "client_name": forms.TextInput(
                attrs={"placeholder": "Как к вам обращаться?", "class": "form-control"}
            ),
            "text": forms.Textarea(
                attrs={
                    "placeholder": "Расскажите о своем опыте посещения мастера",
                    "class": "form-control",
                    "rows": "3",
                }
            ),
            "photo": forms.FileInput(
                attrs={"class": "form-control", "accept": "image/*"}
            ),
        }

class OrderForm(forms.ModelForm):
    """
    Форма для создания заказа с использованием Bootstrap 5
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Добавляем класс form-control к каждому полю формы
        for field_name, field in self.fields.items():
            field.widget.attrs.update({"class": "form-control"})
    
    class Meta:
        model = Order
        fields = [
            "client_name",
            "phone",
            "comment",
            "master",
            "services",
            "appointment_date",
        ]