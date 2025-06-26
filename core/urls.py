from django.contrib import admin
from django.urls import path
from .views import (ThanksView, # Добавили импорт класса ThanksView
                    ServiceDetailView, # Добавили импорт класса ServiceCreateView
                    OrderDetailView, # Добавили импорт класса OrderDetailView
                    ServicesListView, # Добавили импорт класса ServicesListView
                    OrdersListView, # Добавили импорт класса OrdersListView
                    ServiceCreateView, # Добавили импорт класса ServiceCreateView
                    OrderCreateView, # Добавили импорт класса OrderCreateView
                    ReviewCreateView, # Добавили импорт класса ReviewCreateView
                    MastersServicesAjaxView, # Добавили импорт класса MastersServicesAjaxView
                    MasterInfoAjaxView, # Добавили импорт класса MasterInfoAjaxView
                    MasterDetailView, # Добавили импорт класса MasterDetailView
                )
# Эти маршруты будут доступны с префиксом /barbershop/
urlpatterns = [
    path('thanks/', ThanksView.as_view(), name='thanks'),
    path('thanks/<str:source>/', ThanksView.as_view(), name='thanks_with_source'),
    path('orders/', OrdersListView.as_view(), name='orders_list'),
    path('orders/<int:order_id>/', OrderDetailView.as_view(), name='order_detail'),
    path('service/<int:pk>/', ServiceDetailView.as_view(), name='service_detail'),
    path('services/', ServicesListView.as_view(), name='services_list'),
    path('service_create/<str:form_mode>/', ServiceCreateView.as_view(), name='service_create'),
    path('master_detail/<int:master_id>/', MasterDetailView.as_view(), name='masters_info'),
    path('masters_services/', MastersServicesAjaxView.as_view(), name='masters_services_by_id_ajax'),
    path('order_create/', OrderCreateView.as_view(), name='order_create'),
    path('create_review/', ReviewCreateView.as_view(), name='create_review'),
    path('api/master-info/', MasterInfoAjaxView.as_view(), name='get_master_info'),
]
