from django.shortcuts import render
from .models import Master, Service, Review, Order
from django.http import HttpResponse
from .data import * 
from django.contrib.auth.decorators import login_required

def landing(request):
    masters = Master.objects.all()
    services = Service.objects.all()
    reviews = Review.objects.all()
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
    context = {
        'orders': orders
    }
    return render(request, 'core/orders_list.html', context)

@login_required
def order_detail(request, order_id: int):
    try:
        order = [o for o in orders if o['id'] == order_id][0]
    except IndexError:
        # Если заказ не найден , возвращаем 404
        return HttpResponse(status=404)
    return render(request, 'core/order_detail.html', {'order': order})