from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
    
    def ready(self):
        """
        Esta função é chamada quando a app 'core' está pronta.
        Importa os nossos sinais para que eles fiquem "ligados".
        """
        import core.signals