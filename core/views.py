from django.shortcuts import render
from .models import Master, Service, Review, Order
from django.http import HttpResponse
from .data import * 
from django.contrib.auth.decorators import login_required

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
    orders = Order.objects.all().prefetch_related('services').order_by('-date_created')
    context = {
        'orders': orders
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