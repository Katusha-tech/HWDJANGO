from django.contrib import admin
from django.urls import path
from .views import (thanks, 
                    orders_list, 
                    order_detail, 
                    service_create,
                    masters_info,
                    masters_services_by_id,
                    order_create,
                    create_review,
                    get_master_info,
                )
# Эти маршруты будут доступны с префиксом /barbershop/
urlpatterns = [
    path('thanks/', thanks, name='thanks'),
    path('orders/', orders_list, name='orders_list'),
    path('orders/<int:order_id>/', order_detail, name='order_detail'),
    path('service_create/', service_create, name='service_create'),
    path('master_detail/<int:master_id>/', masters_info, name='masters_info'),
    path('masters_services/', masters_services_by_id, name='masters_services_by_id_ajax'),
    path('order_create/', order_create, name='order_create'),
    path('create_review/', create_review, name='create_review'),
    path('api/master-info/', get_master_info, name='get_master_info'),
]
