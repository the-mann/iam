from django.apps import AppConfig


class Sprint2Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'

    def ready(self):
        from . import signals
