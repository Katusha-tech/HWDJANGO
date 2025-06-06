from doctest import master
from django import db
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Услуги
class Service(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(blank=True, verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    duration = models.PositiveIntegerField(verbose_name="Длительность", help_text="Время выполнения в минутах", default=60)
    is_popular = models.BooleanField(default=False, verbose_name="Популярная услуга")
    image = models.ImageField(upload_to="images/services/", blank=True, null=True, verbose_name="Изображение",)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"
        indexes = [
            models.Index(fields=['price']),
            models.Index(fields=['is_popular']),
        ]

# Мастера
class Master(models.Model):
    name = models.CharField(max_length=150, db_index=True, verbose_name="Имя")
    photo = models.ImageField(upload_to="masters/", blank=True, verbose_name="Фотография")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    address = models.CharField(max_length=255, verbose_name="Адрес")
    experience = models.PositiveIntegerField(verbose_name="Стаж работы", help_text="Опыт работы в годах")
    services = models.ManyToManyField("Service", related_name="masters", verbose_name="Услуги")
    is_active = models.BooleanField(default=True, verbose_name="Активен")

    def __str__(self):
        return f'{self.name}'
    
    class Meta:
        verbose_name = "Мастер"
        verbose_name_plural = "Мастера"
        ordering = ['experience']

        indexes = [
            models.Index(fields=['is_active']),
            models.Index(fields=['experience']),
        ]

# Заказы
class Order(models.Model):
    STATUS_CHOICES = [
        ("not_approved", "Не подтвержден"),
        ("moderated", "На модерации"),
        ("spam", "Спам"),
        ("approved", "Подтвержден"),
        ("in_awaiting", "В ожидании"),
        ("completed", "Завершен"),
        ("canceled", "Отменен"),
    ]

    client_name = models.CharField(max_length=100, verbose_name="Имя клиента")
    phone = models.CharField(max_length=20, default="", verbose_name="Телефон")
    comment = models.TextField(blank=True, db_index=True, verbose_name="Комментарий")
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="not_approved", verbose_name="Статус")
    date_created = models.DateTimeField(auto_now_add=True,db_index=True, verbose_name="Дата создания")
    date_updated = models.DateTimeField(auto_now=True,  verbose_name="Дата обновления")
    master = models.ForeignKey("Master", on_delete=models.SET_NULL, null=True, related_name="orders", verbose_name="Мастер")
    services = models.ManyToManyField("Service", related_name="orders", blank=True, verbose_name="Услуги")
    appointment_date = models.DateTimeField(blank=True, verbose_name="Дата записи", null=True)

    def __str__(self):
        return f"Заказ {self.id}: {self.client_name}"
    
    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ["-date_created"]
        indexes = [
            models.Index(fields=['client_name']),
            models.Index(fields=['phone']),
            models.Index(fields=['status']),
            models.Index(fields=['date_created']),
            models.Index(fields=['status', 'appointment_date'], name='status_appointment_date_idx'),
            models.Index(fields=['client_name', 'phone'], name='client_name_phone_idx'),
        ]


# Отзывы
class Review(models.Model):
    client_name = models.CharField(max_length=100, blank=True, verbose_name="Имя клиента")
    text = models.TextField(verbose_name="Текст отзыва")
    rating = models.IntegerField(verbose_name="Оценка", validators=[MinValueValidator(1), MaxValueValidator(5)])
    master = models.ForeignKey("Master", on_delete=models.CASCADE, related_name="reviews", verbose_name="Мастер")
    photo = models.ImageField(upload_to="images/reviews/", blank=True, null=True, verbose_name="Фотография")
    is_published = models.BooleanField(default=False, verbose_name="Опубликован")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    
    def __str__(self):
        return f"Отзыв от {self.client_name} о мастере {self.master}. Статус: {'Опубликован' if self.is_published else 'Не опубликован'}"
    
    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=['rating']),
            models.Index(fields=['is_published']),
            models.Index(fields=['master', 'rating'], name='master_rating_idx'),
        ]