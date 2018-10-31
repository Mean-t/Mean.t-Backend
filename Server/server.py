import os

from app import create_app
from app.misc.logger import logger

from config.dev import DevConfig
from config.production import ProductionConfig

if __name__ == '__main__':
    app = create_app(DevConfig)

    if 'SECRET_KEY' not in os.environ:
        logger(message='SECRET KEY is not set in the environment variable.',
               type='WARN')

    app.run(**app.config['RUN_SETTING'])
