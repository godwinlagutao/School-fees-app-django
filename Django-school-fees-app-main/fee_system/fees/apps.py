# fees/apps.py
from django.apps import AppConfig
import logging

logger = logging.getLogger(__name__)

class FeesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'fees'

    def ready(self):
        import fees.signals
        # Only register signals in normal operation
        if not self.is_running_migrations():
            try:
                from . import signals
                logger.info("Fee signals successfully registered")
            except Exception as e:
                logger.error(f"Failed to register signals: {str(e)}")
                raise

    def is_running_migrations(self):
        import sys
        return 'makemigrations' in sys.argv or 'migrate' in sys.argv