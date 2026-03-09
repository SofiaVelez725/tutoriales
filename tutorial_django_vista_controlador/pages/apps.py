from django.apps import AppConfig
from django.conf import settings
from django.utils.module_loading import import_string


class PagesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "pages"

    def ready(self):
        self.image_storage_class = import_string(settings.IMAGE_STORAGE_CLASS)
