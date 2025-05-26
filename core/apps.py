from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    # метод ready вызызвается при запуске приложения и можно импортировать сигналы
    def ready(self):
        import core.signals
