from django.apps import AppConfig


class AccountConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'account'
    verbose_name = 'حساب'
    verbose_name_plural = 'حساب ها'

    def ready(self) -> None:
        from . import signals