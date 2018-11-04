import os
import optparse

from app import create_app
from app.misc.log import log

from config.dev import DevConfig
from config.production import ProductionConfig

if __name__ == '__main__':
    parser = optparse.OptionParser()

    parser.add_option("-d", "--debug",
                      action="store_true", dest="debug",
                      help=optparse.SUPPRESS_HELP)

    options, _ = parser.parse_args()

    if options.debug:
        app = create_app(DevConfig)
    else:
        print(options.debug)
        app = create_app(ProductionConfig)

    if 'SECRET_KEY' not in os.environ:
        log(message='SECRET KEY is not set in the environment variable.',
            keyword='WARN')

    app.run(**app.config['RUN_SETTING'])
