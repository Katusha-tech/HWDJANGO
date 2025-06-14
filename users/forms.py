from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import get_user_model # Рекомендуется для работы с моделью пользователя

User = get_user_model() # Получаем активную модель пользователя

class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control mb-2', # Добавляем отступ снизу для лучшего вида
            'placeholder': 'Имя пользователя или email'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Пароль'
        })

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control mb-2', 'placeholder': 'Email'
                }),
        required=True, # Делаем email обязательным
        help_text="Обязательное поле."
    )

    class Meta: # Убрали наследование от UserCreationForm.Meta
        model = User # Указываем модель пользователя
        fields = ('username', 'email') # Включаем username и email в форму

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control mb-2',
            'placeholder': 'Имя пользователя'
        })
        # Для полей пароля UserCreationForm уже добавляет placeholder'ы, но мы можем переопределить классы
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control mb-2',
            'placeholder': 'Придумайте пароль'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Повторите пароль'
        })
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user