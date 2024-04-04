from django.apps import AppConfig


# class FinderConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'finder'


class FinderConfig(AppConfig):
    name = 'finder'

    def ready(self):
        import finder.signals


        

