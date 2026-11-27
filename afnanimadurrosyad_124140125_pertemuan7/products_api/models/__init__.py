import os

from dotenv import load_dotenv
from sqlalchemy import engine_from_config
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker, configure_mappers
import zope.sqlalchemy

# Import models to register them with SQLAlchemy
from .category import Category  # noqa: F401
from .product import Product  # noqa: F401

# Run configure_mappers after defining all models
configure_mappers()


def get_database_url() -> str:
    """Build PostgreSQL connection URL safely from .env variables."""
    load_dotenv()
    url = URL.create(
        # SQLAlchemy 2.1 memakai driver psycopg (v3) untuk skema 'postgresql';
        # proyek ini memakai psycopg2-binary sehingga driver ditulis eksplisit.
        drivername='postgresql+psycopg2',
        username=os.getenv('DB_USER', 'postgres'),
        password=os.getenv('DB_PASSWORD', 'postgres'),
        host=os.getenv('DB_HOST', 'localhost'),
        port=int(os.getenv('DB_PORT', '5432')),
        database=os.getenv('DB_NAME', 'products_api_db'),
    )
    return url.render_as_string(hide_password=False)


def get_engine(settings, prefix='sqlalchemy.'):
    return engine_from_config(settings, prefix)


def get_session_factory(engine):
    factory = sessionmaker()
    factory.configure(bind=engine)
    return factory


def get_tm_session(session_factory, transaction_manager):
    """Get a sqlalchemy session managed by the transaction manager."""
    dbsession = session_factory()
    zope.sqlalchemy.register(dbsession, transaction_manager=transaction_manager)
    return dbsession


def includeme(config):
    """Initialize the model for a Pyramid app."""
    settings = config.get_settings()
    settings['tm.manager_hook'] = 'pyramid_tm.explicit_manager'
    config.include('pyramid_tm')
    config.include('pyramid_retry')
    engine = get_engine(settings)
    session_factory = get_session_factory(engine)
    config.registry['dbsession_factory'] = session_factory

    # Add request.dbsession to each request
    config.add_request_method(
        lambda r: get_tm_session(session_factory, r.tm),
        'dbsession',
        reify=True,
    )
