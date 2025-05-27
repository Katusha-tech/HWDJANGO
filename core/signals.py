# Опишем сигнал, который будет слушать создание записи в модель Review 
# и проверять есть ли в поле text слова "плохо" или "ужасно" - если нет, то меняем is_published на True
from .models import Review
from django.db.models.signals import post_save
from django.dispatch import receiver
from .mistral import moderate_review

@receiver(post_save, sender=Review)
def check_review_text(sender, instance, created, **kwargs):
    """ Проверяет текст отзыва на налчие слов 'плохо' или 'ужасно'. 
    Если таких слов нет, то устанавливаем is_published = True
    """
    if created:
        if moderate_review(instance.text):
            instance.is_published = True
            instance.save()
            # Вывод  в терминал
            print(f"Отзыв {instance.client_name} опубликован автоматически.")
        else:
            instance.is_published = False
            instance.save()
            # Вывод  в терминал
            print(f"Отзыв {instance.client_name} не опубликован из-за негативных слов.")