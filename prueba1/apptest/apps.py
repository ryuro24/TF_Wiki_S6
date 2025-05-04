from django.apps import AppConfig


class ApptestConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apptest'

    def ready(self):
        import apptest.signals 