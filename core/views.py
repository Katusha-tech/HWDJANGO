from django.shortcuts import render, redirect
from .models import Master, Service, Review, Order
from django.http import HttpResponse
from .data import * 
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages

def landing(request):
    masters = Master.objects.all()
    services = Service.objects.all()
    reviews = Review.objects.all()
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
    masters_count = len(masters)
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
