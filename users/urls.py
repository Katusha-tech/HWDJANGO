# users/urls.py
from django.urls import path
from . import views

app_name = 'users'
# users:register
# users:login
# users:logout

urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    # Новый маршрут для профиля
    path('profile/<int:pk>/', views.UserProfileDetailView.as_view(), name='profile_detail'),
    # Обновленный маршрут для смены пароля
    path('password_change/', views.UserPasswordChangeView.as_view(), name='password_change'),
    # Новый маршрут для редактирования профиля
    path('profile/edit/', views.UserProfileUpdateView.as_view(), name='profile_edit'),

    # Маршруты для восстановления пароля
    path('password-reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),

]
