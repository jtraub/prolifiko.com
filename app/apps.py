from django.apps import AppConfig as Config

# can't use utils.get_logger here because django hasn't finished setting up
import logging
logger = logging.getLogger('prolifiko.%s' % __name__)

class AppConfig(Config):
    name = 'app'

    def ready(self):
        logger.info('Importing signal receivers')
        from . import receivers

