from django.apps import AppConfig


class StudPortalConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "stud_portal"
def ready(self):
    import stud_portal.signals