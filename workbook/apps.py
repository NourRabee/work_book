from django.apps import AppConfig


class WorkbookConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'workbook'

    def ready(self):
        import workbook.models.models

