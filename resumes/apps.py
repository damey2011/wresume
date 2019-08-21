from django.apps import AppConfig


class ResumesConfig(AppConfig):
    name = 'resumes'

    def ready(self):
        import resumes.signals