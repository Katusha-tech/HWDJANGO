from django.contrib import admin
from .models import Service, Master, Order, Review

admin.site.register(Service)
admin.site.register(Master)
admin.site.register(Order)
admin.site.register(Review)
