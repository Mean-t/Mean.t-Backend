from flask import Flask
from werkzeug.exceptions import HTTPException

from app.misc.logger import logger


def register_extensions(flask_app: Flask):
    from app import extensions

    extensions.swagger.template = flask_app.config['SWAGGER_TEMPLATE']

    extensions.cors.init_app(flask_app)
    extensions.jwt.init_app(flask_app)
    extensions.validator.init_app(flask_app)
    extensions.swagger.init_app(flask_app)


def register_blueprints(flask_app: Flask):
    from app.blueprints import api_v1_blueprint
    from app.views.common import api_funding, api_idea
    # API load

    flask_app.register_blueprint(api_v1_blueprint)


def register_hooks(flask_app: Flask):
    from app.exceptions.exceptions import broad_exception_error_handler, http_exception_handler
    from app.hooks.request_hook import after_request

    flask_app.after_request(after_request)
    flask_app.register_error_handler(HTTPException, http_exception_handler)
    flask_app.register_error_handler(Exception, broad_exception_error_handler)


def create_app(*config_cls: object) -> Flask:

    logger(message='Flask application initialized with {}'.format(', '.join([config.__name__ for config in config_cls])),
           type='INFO')

    flask_app = Flask(__name__)

    for config in config_cls:
        flask_app.config.from_object(config)

    register_extensions(flask_app)
    register_blueprints(flask_app)
    register_hooks(flask_app)

    return flask_app
