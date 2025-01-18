from django.apps import AppConfig


class CommentConfig(AppConfig):  # type: ignore
    default_auto_field = "django.db.models.BigAutoField"
    name = "comment"
