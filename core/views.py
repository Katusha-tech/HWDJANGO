from django.shortcuts import render
from django.http import HttpResponse
from .data import *

def landing(request):
    context = {
        'masters': masters,
        'services': services,
        'menu_items': MENU_ITEMS
    }
    return render(request, 'core/landing.html', context)

def thanks(request):
    masters_count = len(masters)
    context = {
        'masters_count': masters_count, 
        'menu_items': MENU_ITEMS
    }
    return render(request, 'core/thanks.html', context)

def orders_list(request):
    context = {
        'orders': orders,
        'menu_items': MENU_ITEMS
    }
    return render(request, 'core/orders_list.html', context)

def order_detail(request, order_id: int):
    try:
        order = [o for o in orders if o['id'] == order_id][0]
    except IndexError:
        # Если заказ не найден , возвращаем 404
        return HttpResponse(status=404)
    return render(request, 'core/order_detail.html', {'order': order})