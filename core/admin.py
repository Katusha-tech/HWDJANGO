from django.contrib import admin
from .models import Service, Master, Order, Review

admin.site.register(Service)
admin.site.register(Master)
admin.site.register(Order)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'master', 'rating', 'created_at', 'is_published')
    list_filter = ('is_published', 'rating', 'master')
    search_fields = ('client_name', 'text')
    list_editable = ('is_published',)
    readonly_fields = ('created_at',)
    
    # Дополнительные действия
    actions = ['publish_reviews', 'unpublish_reviews']
    
    def publish_reviews(self, request, queryset):
        queryset.update(is_published=True)
    publish_reviews.short_description = "Опубликовать выбранные отзывы"
    
    def unpublish_reviews(self, request, queryset):
        queryset.update(is_published=False)
    unpublish_reviews.short_description = "Снять с публикации выбранные отзывы"