from django.apps import AppConfig


class CommonConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "common"

    def ready(self) -> None:
        # if methods not imported or invoked, dramatiq actors will not be declared
        from . import tasks

        tasks
