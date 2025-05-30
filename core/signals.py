# Опишем сигнал, который будет слушать создание записи в модель Review 
# и проверять есть ли в поле text слова "плохо" или "ужасно" - если нет, то меняем is_published на True
from .models import Order, Review
from django.db.models.signals import post_save
from django.dispatch import receiver
from .mistral import moderate_review
from .telegram_bot import send_telegram_message
from asyncio import run
# Из настроек импортирум токен и id чата 
from django.conf import settings

TELEGRAM_BOT_API_KEY = settings.TELEGRAM_BOT_API_KEY
TELEGRAM_USER_ID = settings.TELEGRAM_USER_ID


@receiver(post_save, sender=Review)
def check_review_text(sender, instance, created, **kwargs):
    """ Проверяет текст отзыва на наличие слов 'плохо' или 'ужасно'. 
    Если таких слов нет, то устанавливаем is_published = True
    """
    if created:
        if not moderate_review(instance.text):
            instance.is_published = True
            instance.save()
            # Вывод  в терминал
            print(f"Отзыв {instance.client_name} опубликован автоматически.")
        else:
            instance.is_published = False
            instance.save()
            # Вывод  в терминал
            print(f"Отзыв {instance.client_name} не опубликован из-за негативных слов.")

@receiver(post_save, sender=Order)
def telegram_order_notification(sender, instance, created, **kwargs):
    """ 
    Отправляет уведомление в телеграм о создании заказа 
    """
    if created:
        # Если заказ создан, добываем данные
        client_name = instance.client_name
        phone = instance.phone
        comment = instance.comment

        # Формируем сообщение
        telegram__message = f"""
        *Новый заказ от {client_name}!*
        *Телефон:* {phone}
        *Комментарий:* {comment}
        *Ссылка на заказ:* http://127.0.0.1:8000/admin/core/order/{instance.id}/change/
        ====================
        """
        # Логика отправки сообщения в Telegram

        run(send_telegram_message(TELEGRAM_BOT_API_KEY, TELEGRAM_USED_ID, telegram__message))