from django.apps import AppConfig


class PaaConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "paa"

    def ready(self) -> None:  # pragma: no cover - import side effects
        from . import services  # noqa: F401
