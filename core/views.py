from django.shortcuts import render, redirect
from .models import Master, Service, Review, Order
from django.http import HttpResponse
from django.http import JsonResponse
from .data import * 
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from  django.shortcuts import get_object_or_404
from django.contrib import messages
from .forms import ReviewForm
import json

def landing(request):
    masters = Master.objects.all()
    services = Service.objects.all()
    reviews = Review.objects.filter(is_published=True)
    for master in masters:
        print(f"Master: {master.name}, Photo: {master.photo}")

    context = {
        'title':'Главная - Барбершоп Зигзаг удачи',
        'masters': masters,
        'services': services,
        'reviews': reviews
    }
    return render(request, 'core/landing.html', context)

def thanks(request):
    masters_count = Master.objects.count()
    context = {
        'masters_count': masters_count
    }
    return render(request, 'core/thanks.html', context)

@login_required
def orders_list(request):
    all_orders = Order.objects.all()
    search_query = request.GET.get('search', None)
    check_boxes = request.GET.getlist('search_in')
    
    if not check_boxes:
        check_boxes = ['name']

    if search_query:
        filters = Q()
        
        if "phone" in check_boxes:
            filters |= Q(phone__icontains=search_query)

        if "name" in check_boxes:
            filters |= Q(client_name__icontains=search_query)

        if "status" in check_boxes:
            # Поиск по отображаемым значениям статуса
            status_display_map = dict(Order.STATUS_CHOICES)
            matching_status_codes = []
            
            # Ищем коды статусов, у которых отображаемое значение содержит поисковый запрос
            for code, display in Order.STATUS_CHOICES:
                if search_query.lower() in display.lower():
                    matching_status_codes.append(code)
            
            # Если найдены совпадения, добавляем их в фильтр
            if matching_status_codes:
                filters |= Q(status__in=matching_status_codes)
            else:
                # Если нет совпадений по отображаемым значениям, 
                # пробуем искать по коду статуса (для администраторов)
                filters |= Q(status__icontains=search_query) 

        all_orders = all_orders.filter(filters)

    context = {
        'title': 'Список заказов',
        'orders': all_orders,
    }
    return render(request, 'core/orders_list.html', context)
            

@login_required
def order_detail(request, order_id: int):
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        # Если заказ не найден , возвращаем 404
        return HttpResponse(status=404)
    return render(request, 'core/order_detail.html', {'order': order})

def service_create(request):
    if request.method == 'GET':
        context = {
            'title': 'Создание услуги',
        }
        return render(request, 'core/service_create.html', context)
    
    elif request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        description = request.POST.get('description', '')
        
        # Проверка только обязательных полей: название и цена
        if not name or not price:
            error_message = 'Название и цена услуги обязательны для заполнения'
            context = {
                'title': 'Создание услуги',
                'error': error_message,
                'form_data': {
                    'name': name,
                    'price': price,
                    'description': description,
                }
            }
            return render(request, 'core/service_create.html', context)
        
        # Создание услуги
        try:
            new_service = Service.objects.create(
                name=name,
                price=price,
                description=description
            )
            return HttpResponse(f"Услуга '{new_service.name}' успешно создана!")
        except Exception as e:
            context = {
                'title': 'Создание услуги',
                'error': f'Ошибка при создании услуги: {str(e)}',
                'form_data': {
                    'name': name,
                    'price': price,
                    'description': description,
                }
            }
            return render(request, 'core/service_create.html', context)
    
    # Этот блок выполнится только при нестандартных HTTP методах
    return HttpResponse(f"Ошибка: для создания услуги используйте форму на сайте.", status=405)

# Проверить 

def masters_info(request, master_id=None):
    if master_id is None:
        data = json.loads(request.body)
        master_id = data.get('master_id') 

    master = get_object_or_404(Master, id=master_id)

    master_data = {
        'id': master.id,
        'name': master.name,
        'photo': master.photo.url if master.photo else None,
        'description': master.description,
        'services': [{'name': service.name, 'price': service.price} for service in master.services.all()]
    }

    return HttpResponse(
        json.dumps(master_data, ensure_ascii=False, indent = 4), 
        content_type='application/json',
        )

def create_review(request):
    if request.method == 'GET':
        form = ReviewForm()
        masters = Master.objects.all()

        context = {
            'title': 'Создание отзыва',
            'form': form,
            'masters': masters,
            'button_text': 'Создать',
        }
        return render(request, 'core/review_form.html', context)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)

        if form.is_valid():
            review = form.save(commit=False)
            review.is_published = False
            review.save()

            client_name = form.cleaned_data.get('client_name')
            messages.success(request, f"Отзыв от {client_name} успешно создан и отправлен на модерацию!")

            return redirect("thanks")
        else:
            messages.error(request, "Пожалуйста, исправьте ошибки в форме.")
        
        masters = Master.objects.all()
        context = {
            'title': 'Создание отзыва',
            'form': form,
            'masters': masters,
            'button_text': 'Создать',
        }
        return render(request, 'core/review_form.html', context)


def get_master_info(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        master_id = request.GET.get('master_id')
        if master_id:
            try:
                master = Master.objects.get(pk=master_id)
                master_data = {
                    'id': master.id,
                    'name': f"{master.name}",
                    'experience': master.experience,
                    'photo': master.photo.url if master.photo else None,
                    'services': list(master.services.values('id', 'name', 'price')),
                }
                return JsonResponse({'success': True, 'master': master_data})
            except Master.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Мастер не найден'})
        return JsonResponse({'success': False, 'error': 'Не указан ID мастера'})
    return JsonResponse({'success': False, 'error': 'Недопустимый запрос'})

