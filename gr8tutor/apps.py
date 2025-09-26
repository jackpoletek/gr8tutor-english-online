from django.apps import AppConfig


class Gr8TutorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'gr8tutor'

    def ready(self):
        import gr8tutor.signals
    