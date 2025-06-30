"""Формы для работы с пользователями: аутентификация, регистрация, профиль."""
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth import get_user_model

User = get_user_model()

class UserLoginForm(AuthenticationForm):
    """Форма для входа пользователя в систему."""
    def __init__(self, *args, **kwargs):
        """Инициализация формы входа: настройка полей."""
        super().__init__(*args, **kwargs)
        # Кастомизация поля username
        self.fields['username'].widget.attrs.update({
            'class': 'form-control mb-2',
            'placeholder': 'Имя пользователя или email'
        })
        # Кастомизация поля password
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Пароль'
        })

class CustomSetPasswordForm(SetPasswordForm):
    """Кастомная форма для сброса пароля."""
    def __init__(self, *args, **kwargs):
        """Инициализация формы сброса пароля: настройка полей."""
        super().__init__(*args, **kwargs)
        # Кастомизация поля new_password1
        self.fields['new_password1'].widget.attrs.update({
            'class': 'form-control mb-2',
            'placeholder': 'Новый пароль'
        })
        # Кастомизация поля new_password2
        self.fields['new_password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Подтвердите новый пароль'
        })
            
        # Сброс help_text для полей пароля
        for field_name in ('new_password1', 'new_password2'):
            if self.fields.get(field_name):
                # Сбрасываем подсказки (help_text)
                self.fields[field_name].help_text = ''



class UserRegisterForm(UserCreationForm):
    """Форма для регистрации нового пользователя."""
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control mb-2', 'placeholder': 'Email'}),
        required=True
    )

    class Meta:
        model = User
        fields = ('username', 'email')

    def __init__(self, *args, **kwargs):
        """Инициализация формы входа: настройка полей."""
        super().__init__(*args, **kwargs)
        
        # Кастомизация поля username
        self.fields['username'].widget.attrs.update({
            'class': 'form-control mb-2',
            'placeholder': 'Имя пользователя',
        })
        # Кастомизация поля password1
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control mb-2',
            'placeholder': 'Придумайте пароль',
        })
        # Кастомизация поля password2
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Повторите пароль',
        })
        # Сбрасываем подсказки (help_text) для полей, чтобы не отображались
        for field_name in ('username', 'password1', 'password2'):
            if self.fields.get(field_name):
                # Сбрасываем подсказки (help_text)
                self.fields[field_name].help_text = ''


class UserProfileUpdateForm(forms.ModelForm):
    """Форма для обновления профиля пользователя."""
    # Метаданные формы
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
        """Инициализация формы обновления профиля."""
        super().__init__(*args, **kwargs)
        # Примечание: при необходимости можно ограничить редактирование полей

class UserPasswordChangeForm(PasswordChangeForm):
    """Форма для смены пароля пользователя."""
    def __init__(self, *args, **kwargs):
        """Инициализация формы смены пароля: настройка полей и сброс подсказок."""
        super().__init__(*args, **kwargs)
        # Кастомизация поля старого пароля
        self.fields['old_password'].widget.attrs.update({
            'class': 'form-control mb-2',
            'placeholder': 'Старый пароль'
        })
        # Кастомизация поля нового пароля
        self.fields['new_password1'].widget.attrs.update({
            'class': 'form-control mb-2',
            'placeholder': 'Новый пароль'
        })
        # Кастомизация поля подтверждения пароля
        self.fields['new_password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Подтвердите новый пароль'
        })
        # Сброс help_text для полей пароля
        for field_name in ('old_password', 'new_password1', 'new_password2'):
            if self.fields.get(field_name):
                # Сбрасываем подсказки (help_text)
                self.fields[field_name].help_text = ''

class CustomPasswordResetForm(PasswordResetForm):
    """Кастомная форма для сброса пароля."""
    def __init__(self, *args, **kwargs):
        """Инициализация формы сброса пароля: настройка полей."""
        super().__init__(*args, **kwargs)
        # Кастомизация поля email
        self.fields['email'].widget.attrs.update({
            'class': 'form-control mb-2',
            'placeholder': 'Email'
        })