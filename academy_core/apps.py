from django.apps import AppConfig


class AcademyCoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'academy_core'

    def ready(self):
        from . import signals  # noqa: F401
