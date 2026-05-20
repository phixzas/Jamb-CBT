from django.apps import AppConfig


class ExamsConfig(AppConfig):
    name = 'exams'


    def ready(self):
        import exams.signals