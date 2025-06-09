# users/forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import get_user_model # Рекомендуется для работы с моделью пользователя
from django.contrib.auth.forms import PasswordChangeForm # Добавлен импорт для смены пароля

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
        widget=forms.EmailInput(attrs={'class': 'form-control mb-2', 'placeholder': 'Email'}),
        required=True # Делаем email обязательным
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
        # Убираем help_text для стандартных полей циклом
        for field_name in ('username', 'password1', 'password2'):
            if self.fields.get(field_name): # Проверяем, существует ли поле
                self.fields[field_name].help_text = ''
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'avatar', 'birth_date', 'telegram_id', 'github_id']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'avatar': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'telegram_id': forms.TextInput(attrs={'class': 'form-control'}),
            'github_id': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Если вы не хотите, чтобы пользователь менял email или username через эту форму,
        # можно сделать поля disabled или readonly, или исключить их из fields.
        # Например, для email, если он используется для логина:
        # self.fields['email'].disabled = True 

class UserPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update({
            'class': 'form-control mb-2', 
            'placeholder': 'Старый пароль'
        })
        self.fields['new_password1'].widget.attrs.update({
            'class': 'form-control mb-2', 
            'placeholder': 'Новый пароль'
        })
        self.fields['new_password2'].widget.attrs.update({
            'class': 'form-control', 
            'placeholder': 'Подтвердите новый пароль'
        })
        # Убираем help_text для стандартных полей
        for field_name in ('old_password', 'new_password1', 'new_password2'):
            if self.fields.get(field_name):
                self.fields[field_name].help_text = ''