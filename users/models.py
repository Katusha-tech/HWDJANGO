from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # Убираем требование first_name и last_name, если они не обязательны
    first_name = None
    last_name = None

    email = models.EmailField(unique=True) # Делаем email уникальным и обязательным для логина
    
    avatar = models.ImageField(
        upload_to='users/avatars/', 
        null=True, 
        blank=True, 
        verbose_name='Аватар'
    )
    birth_date = models.DateField(
        null=True, 
        blank=True, 
        verbose_name='Дата рождения'
    )
    telegram_id = models.CharField(
        max_length=100, 
        blank=True, 
        null=True, 
        verbose_name='Telegram ID'
    )
    github_id = models.CharField(
        max_length=100, 
        blank=True, 
        null=True, 
        verbose_name='GitHub ID'
    )

    # Указываем, что для логина будет использоваться поле email
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username'] # username все еще нужен для AbstractUser, но можно сделать его не основным

    def __str__(self):
        return self.email # Или self.username, если предпочитаете

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
