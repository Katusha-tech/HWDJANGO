from django.urls import path
from . import views # Представления мы создадим позже


app_name = 'users' # Пространство имен для URL-адресов этого приложения

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'), #Используем FBV login_view
    path('logout/', views.logout_view, name='logout'),
]
