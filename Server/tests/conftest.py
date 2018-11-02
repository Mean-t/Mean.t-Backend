import os
import pytest
from flask import g
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from alembic.command import upgrade as alembic_upgrade
from alembic.config import Config as AlembicConfig

from app import create_app
from config.test import TestConfig  # flask application configuration

# typing hits
from flask import Flask
from flask.testing import FlaskClient
from sqlalchemy.engine.base import Engine
from typing import Dict


@pytest.fixture(scope="session")
def flask_app() -> Flask:
    app = create_app(TestConfig)
    app_context = app.app_context()
    app_context.push()

    yield app

    app_context.pop()


@pytest.fixture(scope="session")
def flask_client(flask_app: Flask) -> FlaskClient:
    return flask_app.test_client()


@pytest.fixture(scope="session")
def db() -> Dict[Engine, sessionmaker]:
    engine = create_engine(TestConfig.SQLALCHEMY_DATABASE_URI, echo=True)
    session = sessionmaker(bind=engine)
    print(type(engine), type(session))
    _db = {
        'engine': engine,
        'session': session
    }

    alembic_config = AlembicConfig(os.path.abspath("../../../alembic.ini"))
    alembic_config.set_main_option('script_location', os.path.abspath("../../../meant_alembic"))
    alembic_config.set_main_option('sqlalchemy.url', TestConfig.SQLALCHEMY_DATABASE_URI)
    alembic_upgrade(alembic_config, 'head')

    yield _db

    engine.dispose()


@pytest.fixture(scope='function')
def session(db: Dict[Engine, sessionmaker]) -> sessionmaker:
    session = db['session']()
    g.db = session

    yield session

    session.rollback()
    session.close()
