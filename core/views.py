# Стандартные библиотеки
import json

# Django
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.db.models import Q, F, Prefetch
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

# Приложение
from .models import Master, Service, Review, Order
from .forms import ServiceForm, ReviewForm, OrderForm, ServiceEasyForm
from .data import *



class LandingPageView(TemplateView):
    template_name = 'core/landing.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Главная - Барбершоп Зигзаг удачи"
        context["years_on_market"] = 50
        context["masters"] = Master.objects.all()
        context["services"] = Service.objects.all()
        context["reviews"] = Review.objects.filter(is_published=True)
        return context


class StaffRequiredMixin(UserPassesTestMixin):
    """
    Миксин для проверки, является ли пользователь сотрудником (is_staff).
    Если проверка не пройдена, пользователь перенаправляется на главную страницу
    с сообщением об ошибке.
    """

    def test_func(self):
        """Проверяет, аутентифицирован ли пользователь и является ли сотрудником."""
        return self.request.user.is_authenticated and self.request.user.is_staff

    def handle_no_permission(self):
        """Обрабатывает отсутствие прав доступа, показывая сообщение об ошибке."""
        messages.error(self.request, "У вас нет доступа к этому разделу.")
        return redirect("landing")

class ThanksView(TemplateView):
    template_name = 'core/thanks.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['masters_count'] = Master.objects.filter(is_active=True).count()
        context['additional_message'] = "Спасибо, что выбрали нас!"

        source = self.kwargs.get('source', None)
        if source == 'order':
            context['source_message'] = "Ваш заказ успешно создан и принят в обработку"
        elif source == 'review':
            context['source_message'] = "Ваш отзыв успешно отправлен и будет опубликован после модерации"
        elif source:
            context['source_message'] = f"Благодарим вас за ваше действие, инициированное со страницы: {source}."
        else:
            context['source_message'] = "Спасибо за посещение!"

        return context


class OrdersListView(StaffRequiredMixin, ListView):
    model = Order
    template_name = 'core/orders_list.html'
    context_object_name = 'orders'
    paginate_by = 2

    def get_queryset(self):
        queryset = Order.objects.select_related("master").prefetch_related("services").all()
        search_query = self.request.GET.get("search", "").strip()
        check_boxes = self.request.GET.getlist("search_in")

        if not search_query:
            return queryset

        # Если чекбоксы не выбраны — ищем по имени
        if not check_boxes:
            check_boxes = ['name']

        filters = Q()

        if "phone" in check_boxes:
            filters |= Q(phone__icontains=search_query)
        if "name" in check_boxes:
            filters |= Q(client_name__icontains=search_query)
        if "comment" in check_boxes:
            filters |= Q(comment__icontains=search_query)
        if "status" in check_boxes:
            # Ищем и по отображаемым значениям, и по кодам статусов
            matching_status_codes = [
                code for code, display in Order.STATUS_CHOICES
                if search_query.lower() in display.lower()
            ]
            if matching_status_codes:
                filters |= Q(status__in=matching_status_codes)
            else:
                filters |= Q(status__icontains=search_query)

        return queryset.filter(filters)


class OrderDetailView(StaffRequiredMixin, DetailView):
    """
    Представление для детального просмотра заказа.
    Доступно только для сотрудников. Проверяет права доступа в методе dispatch.
    """

    model = Order # Указываем, какую модель мы хотим отобразить
    template_name = 'core/order_detail.html'
    pk_url_kwarg = 'order_id' # указываем, что pk будет извлекаться из order_id в URL
    
    

class ServiceDetailView(DetailView):
    """
    Представление для отображения детальной информации об услуге.
    Использует модель Service и явно указанное имя шаблона.
    """
    model = Service # Указываем, какую модель мы хотим отобразить
    template_name = 'core/service_detail.html'


class ServiceCreateView(StaffRequiredMixin, CreateView):
    model = Service
    form_class = ServiceForm
    template_name = 'core/service_create.html'  
    success_url = reverse_lazy('services_list')
    extra_content = {
        'title': 'Создание услуги',
        'button_txt': 'Создать',
    }
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.extra_content)
        return context

    def get_form_class(self):
        form_mode = self.kwargs.get("form_mode")
        if form_mode == "normal":
            return ServiceForm
        elif form_mode == "easy":
            return ServiceEasyForm
        return ServiceForm  # дефолт

    def form_valid(self, form):
        messages.success(self.request, f"Услуга '{form.cleaned_data['name']}' успешно создана!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Ошибка формы: проверьте ввод данных.")
        return super().form_invalid(form)


class MasterDetailView(DetailView):
    """
    Представление для отображения детальной информации о мастере и его услугах.
    Реализует:
    - Жадную загрузку связанных услуг и отфильтрованных отзывов для решения проблемы N+1
    - Атомарное обновление счетчика просмотров с использованием F-выражений
    - Кэширование просмотренных мастеров в сессии для избежания повторного счетчика
    """
    model = Master
    template_name = "core/master_detail.html"
    context_object_name = "master"

    def get_queryset(self):
        """
        Возвращает QuerySet с жадной загрузкой связанных услуг и опубликованных отзывов.
        Использует Prefetch для фильтрации отзывов по статусу публикации и сортировки.
        """
        return Master.objects.prefetch_related(
            'services',
            Prefetch('reviews', queryset=Review.objects.filter(is_published=True).order_by("-created_at"))
        )

    def get_object(self, queryset=None):
        """
        Получает объект мастера и атомарно увеличивает счетчик просмотров,
        если мастер еще не был просмотрен в текущей сессии.
        """
        master = super().get_object(queryset)
        
        master_id = master.id
        viewed_masters = self.request.session.get("viewed_masters", [])

        if master_id not in viewed_masters:
            # Атомарное обновление счетчика просмотров в БД
            Master.objects.filter(id=master_id).update(view_count=F("view_count") + 1)
            
            # Обновляем сессию и счетчик в объекте для немедленного отображения
            viewed_masters.append(master_id)
            self.request.session["viewed_masters"] = viewed_masters
            master.view_count += 1

        return master

    def get_context_data(self, **kwargs):
        """
        Добавляет в контекст связанные отзывы, услуги и заголовок страницы.
        Данные уже загружены благодаря `prefetch_related` в `get_queryset`.
        """
        context = super().get_context_data(**kwargs)
        context['reviews'] = self.object.reviews.all()
        context['services'] = self.object.services.all()
        context['title'] = f"Мастер {self.object.first_name} {self.object.last_name}"
        return context


class MastersServicesAjaxView(View):
    """
    AJAX-представление для получения списка услуг мастера.
    Поддерживает GET и POST запросы. Возвращает данные в формате JSON.
    """

    def get(self, request, *args, **kwargs):
        """Обрабатывает GET-запрос с параметром master_id."""
        master_id = request.GET.get("master_id")
        return self.get_services_json_response(master_id)

    def post(self, request, *args, **kwargs):
        """Обрабатывает POST-запрос с JSON-телом, содержащим master_id."""
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        master_id = data.get("master_id")
        return self.get_services_json_response(master_id)

    def get_services_json_response(self, master_id):
        """Возвращает JSON-ответ со списком услуг мастера или ошибку."""
        if not master_id:
            return JsonResponse({"error": "master_id is required"}, status=400)

        master = get_object_or_404(Master, id=master_id)
        services = master.services.all()
        response_data = [
            {"id": service.id, "name": service.name, "price": service.price} for service in services
        ]
        return JsonResponse(response_data, safe=False)

class ServicesListView(StaffRequiredMixin, ListView):
    """
    Представление для отображения списка услуг с доступом только для персонала.
    """
    model = Service # Указываем, какую модель мы хотим отобразить
    template_name = 'core/services_list.html'
    context_object_name = 'services'
    extra_context = {
        'title': 'Управление услугами',
    }


class OrderCreateView(CreateView):
    """
    Представление для создания нового заказа.
    Поддерживает отображение формы и обработку её отправки.
    """
    model = Order
    form_class = OrderForm
    template_name = "core/order_form.html"

    def get_success_url(self):
        # Возвращаем URL для перенаправления после успешного создания заказа
        # Убедись, что в urls.py есть такой путь с именем 'thanks_with_source'
        return reverse_lazy("thanks_with_source", kwargs={"source": "order"})

    def get_context_data(self, **kwargs):
        # Добавляем в контекст заголовок, текст кнопки, список мастеров и пустой список услуг
        context = super().get_context_data(**kwargs)
        context["title"] = "Создание заказа"
        context["button_text"] = "Записаться"
        context["masters"] = Master.objects.all()
        context["services"] = []  # Можно динамически подгружать услуги через AJAX
        return context

    def form_valid(self, form):
        # При успешном сохранении заказа показываем сообщение
        client_name = form.cleaned_data.get("client_name")
        messages.success(
            self.request,
            f"Ваша запись успешно создана, {client_name}! Мы свяжемся с вами для подтверждения!"
        )
        return super().form_valid(form)
    

class ReviewCreateView(CreateView):
    """
    Представление для создания нового отзыва.
    Поддерживает предзаполнение мастера, отправку формы и отображение сообщений.
    """
    model = Review
    form_class = ReviewForm
    template_name = "core/review_form.html"

    def get_success_url(self):
        # URL для редиректа после успешной отправки отзыва
        return reverse_lazy("thanks_with_source", kwargs={"source": "review"})

    def get_initial(self):
        # Устанавливает начальные данные формы, включая мастера, если передан master_id
        initial = super().get_initial()
        master_id = self.request.GET.get("master_id")
        if master_id:
            try:
                initial["master"] = Master.objects.get(pk=master_id)
            except Master.DoesNotExist:
                pass
        return initial

    def get_context_data(self, **kwargs):
        # Расширяет контекст шаблона дополнительными данными
        context = super().get_context_data(**kwargs)
        context["title"] = "Создание отзыва"
        context["button_text"] = "Создать"
        context["masters"] = Master.objects.all()
        return context

    def form_valid(self, form):
        # Обрабатывает валидную форму: сохраняет отзыв и уведомляет пользователя
        review = form.save(commit=False)
        review.is_published = False
        review.save()

        messages.success(
            self.request,
            "Ваш отзыв успешно добавлен! Он будет опубликован после проверки модератором.",
        )
        return redirect(self.get_success_url())


class MasterInfoAjaxView(View):
    """
    AJAX-представление для получения информации о мастере.
    Возвращает JSON с данными мастера по переданному master_id.
    """

    def get(self, request, *args, **kwargs):
        if not self.is_ajax(request):
            return JsonResponse({"success": False, "error": "Недопустимый тип запроса"}, status=400)

        master_id = request.GET.get("master_id")
        if not master_id:
            return JsonResponse({"success": False, "error": "Не указан ID мастера"}, status=400)

        try:
            master = Master.objects.get(pk=master_id)
        except Master.DoesNotExist:
            return JsonResponse({"success": False, "error": "Мастер не найден"}, status=404)

        master_data = {
            "id": master.id,
            "name": f"{master.first_name} {master.last_name}" if hasattr(master, 'first_name') else master.name,
            "experience": master.experience,
            "photo": master.photo.url if master.photo else None,
            "services": list(master.services.values("id", "name", "price")),
        }

        return JsonResponse({"success": True, "master": master_data})

    def is_ajax(self, request):
        return request.headers.get("X-Requested-With") == "XMLHttpRequest"
