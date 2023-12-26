from django.apps import AppConfig
import crypto_loop


class DatabaseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'database'
