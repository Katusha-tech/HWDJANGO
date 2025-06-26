from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import CreateView
from django.contrib.auth import login # для автоматического входа пользователя после регистрации
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import UserRegisterForm, UserLoginForm
from django.shortcuts import redirect
# Импорт служебных вью для сроса и восстановления пароля

class UserRegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('landing') # URL для редиректа после успешного создания

    def dispatch(self, request, *args, **kwargs):
        # Перенаправляем аутентифицированных пользователей
        if request.user.is_authenticated:
            return redirect('landing')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # Этот метод вызывается, когда форма валидна.
        # Сначала вызываем родительский метод для сохранения пользователя.
        response = super().form_valid(form) 
        # self.object теперь содержит созданного пользователя
        user = self.object 
        login(self.request, user) # Автоматический вход
        messages.success(self.request, f'Добро пожаловать, {user.username}! Регистрация прошла успешно.')
        return response # Возвращаем HTTP-ответ (редирект на success_url)

    def form_invalid(self, form):
        messages.error(self.request, 'Пожалуйста, исправьте ошибки в форме регистрации.')
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация'
        return context

class UserLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm # Используем нашу кастомную форму
    redirect_authenticated_user = True # Перенаправлять, если уже авторизован

    def get_success_url(self):
        messages.success(self.request, f'С возвращением, {self.request.user.username}!')
        next_url = self.request.GET.get('next') # Для поддержки ?next= параметра
        return next_url or reverse_lazy('landing')

    def form_invalid(self, form):
        messages.error(self.request, 'Неверное имя пользователя или пароль. Попробуйте снова.')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Вход'
        return context

class UserLogoutView(LogoutView):
    # URL для редиректа после выхода. Можно также указать в settings.LOGOUT_REDIRECT_URL
    next_page = reverse_lazy('landing') 

    def dispatch(self, request, *args, **kwargs):
        # Добавляем сообщение перед выходом, если пользователь аутентифицирован
        if request.user.is_authenticated:
            messages.info(request, 'Вы успешно вышли из системы.')
        return super().dispatch(request, *args, **kwargs)