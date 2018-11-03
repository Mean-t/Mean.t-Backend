import os
import pytest
from flask import g
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from alembic.command import upgrade as alembic_upgrade
from alembic.config import Config as AlembicConfig
from alembic.util.exc import CommandError

from app import create_app
from config.test import TestConfig  # flask application configuration
from app.misc.logger import logger

# typing hits
from flask import Flask
from flask.testing import FlaskClient
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Session
from typing import Dict


@pytest.fixture(scope="session")
def flask_app() -> Flask:
    app = create_app(TestConfig)
    app_context = app.app_context()
    app_context.push()

    logger(message="flask app created", type="INFO")
    yield app

    logger(message="flask app released", type="INFO")
    app_context.pop()


@pytest.fixture(scope="session")
def flask_client(flask_app: Flask) -> FlaskClient:
    logger(message="flask test client created", type="INFO")
    return flask_app.test_client()


@pytest.fixture(scope="session")
def db() -> Dict[Engine, sessionmaker]:
    engine = create_engine(TestConfig.SQLALCHEMY_DATABASE_URI, echo=True)
    session = sessionmaker(bind=engine)

    _db = {
        'engine': engine,
        'session': session
    }
    try:
        alembic_config = AlembicConfig(os.path.abspath("../../alembic.ini"))
        alembic_config.set_main_option('script_location', os.path.abspath("../../meant_alembic"))
        alembic_config.set_main_option('sqlalchemy.url', TestConfig.SQLALCHEMY_DATABASE_URI)
        alembic_upgrade(alembic_config, 'head')
    except CommandError:
        logger(message="testing only specified TCs", type="INFO")
        alembic_config = AlembicConfig(os.path.abspath("../../../alembic.ini"))
        alembic_config.set_main_option('script_location', os.path.abspath("../../../meant_alembic"))
        alembic_config.set_main_option('sqlalchemy.url', TestConfig.SQLALCHEMY_DATABASE_URI)
        alembic_upgrade(alembic_config, 'head')

    logger(message="database created", type="INFO")
    yield _db

    logger(message="database disposed", type="INFO")
    engine.dispose()


@pytest.fixture(scope='function')
def session(db: Dict[Engine, sessionmaker]) -> Session:
    session = db['session']()
    g.db = session

    logger(message="database session created", type="INFO")
    yield session

    logger(message="database session closed", type="INFO")
    session.rollback()
    session.close()
