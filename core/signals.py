# Опишем сигнал, который будет слушать создание записи в модель Review 
# и проверять есть ли в поле text слова "плохо" или "ужасно" - если нет, то меняем is_published на True
from .models import Order, Review
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from .mistral import is_bad_review
from .telegram_bot import send_telegram_message
from asyncio import run
# Из настроек импортирум токен и id чата 
from django.conf import settings

TELEGRAM_BOT_API_KEY = settings.TELEGRAM_BOT_API_KEY
TELEGRAM_USER_ID = settings.TELEGRAM_USER_ID


@receiver(post_save, sender=Review)
def check_review_text(sender, instance, created, **kwargs):
    """ 
    Проверяет текст отзыва на наличие слов 'плохо' или 'ужасно'. 
    Если таких слов нет, то устанавливаем is_published = True
    """
    if created:
        if not is_bad_review(instance.text):
            instance.is_published = True
            instance.save()
            # Отправка в телеграм
            message = f"""
🎉*Новый отзыв от клиента!*🎉

👤*Имя:* {instance.client_name}
💬*Текст:* {instance.text}
⭐*Оценка:* {instance.rating}

🔗*Ссылка на отзыв:* http://127.0.0.1:8000/admin/core/review/{instance.id}/change/

#отзыв
=================
"""
            run(send_telegram_message(TELEGRAM_BOT_API_KEY, TELEGRAM_USER_ID, message))

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
        telegram_message = f"""📞*Новый заказ от {client_name}!*📞

*Телефон:* `{phone}`
*Комментарий:* {comment}
*Ссылка на заказ:* http://127.0.0.1:8000/admin/core/order/{instance.id}/change/
====================
"""
        # Логика отправки сообщения в Telegram

        run(send_telegram_message(TELEGRAM_BOT_API_KEY, TELEGRAM_USER_ID, telegram_message))

# Делаем так же с ожиданием m2m_changed
# Order.services.through - это промежуточная модель, которая создается автоматически при создании связи многие-ко-многим между Order и Service.
# Ожидаем события m2m_changed, когда туда запишутся новые связи
@receiver(m2m_changed, sender=Order.services.through)
def send_telegram_notification(sender, instance, action, **kwargs):
    """
    Обработка сигнала m2m_changed для модели Order.
    Он обрабатывает добавление каждой услуги в запись на консультацию.
    """
    # action == 'post_add' - это значит, что в промежуточную табличку добаивли новую связь. Но надо убедиться,
    # что это именно добавление новой связи, а не удаление или изменение
    # pk_set - это список id услуг, которые были добавлены в запись (формируется только при создании Order или удалении)
    # Комбинация позволяет точно понять, что это именно создание новой услуги и что все M2M связи уже созданы
    if action == 'post_add' and kwargs.get('pk_set'):
        # Получаем список услуг
        services = [service.name for service in instance.services.all()]

        # Формируем сообщение

        message = f"""✂️ *НОВАЯ ЗАПИСЬ НА УСЛУГУ!* ✂️

*Имя:* {instance.client_name}
*Телефон:* `{instance.phone or 'Не указан'}`
*Комментарий:* _{instance.comment or 'Не указан'}_
*Услуги:* {', '.join(services) or 'Не указаны'}
*Дата создания:* {instance.date_created.strftime('%d.%m.%Y %H:%M') if instance.date_created else 'Не указана'}
*Мастер:* {instance.master.name if instance.master else 'Не указан'}
*Желаемая дата:* {instance.appointment_date.strftime('%d.%m.%Y %H:%M') if instance.appointment_date else 'Не указана'}

🔗*Ссылка на запись:* http://127.0.0.1:8000/admin/core/order/{instance.id}/change/
        
#новаязапись #мастер{instance.master.name.replace(' ', '').replace('"', '') if instance.master else 'неизвестен'}
====================
""" 
        run(send_telegram_message(TELEGRAM_BOT_API_KEY, TELEGRAM_USER_ID, message))
