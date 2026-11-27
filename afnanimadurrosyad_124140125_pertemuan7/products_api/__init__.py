"""Aplikasi REST API Manajemen Kategori dan Produk.

Praktikum PAW Pertemuan 7 — Basis Data: SQLAlchemy, Alembic & Pyramid.
Nama: Afnan Imadurrosyad | NIM: 124140125 | Kelas: RB
"""

from pyramid.config import Configurator
from pyramid.events import NewResponse
from pyramid.renderers import JSON

from .models import get_database_url


def add_cors_headers_response_callback(event):
    """Menambahkan header CORS pada setiap HTTP response."""
    event.response.headers.update({
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST, GET, DELETE, PUT, OPTIONS',
        'Access-Control-Allow-Headers': 'Origin, Content-Type, Accept, Authorization',
        'Access-Control-Max-Age': '1728000',
    })


def main(global_config, **settings):
    """Return a Pyramid WSGI application."""
    # Pertahankan SQLite in-memory saat pytest menjalankan testing.ini
    if not str(settings.get('sqlalchemy.url', '')).startswith('sqlite:///:memory:'):
        settings['sqlalchemy.url'] = get_database_url()

    with Configurator(settings=settings) as config:
        # Konfigurasi JSON renderer dan CORS
        config.add_renderer('json', JSON(indent=4))
        config.add_subscriber(add_cors_headers_response_callback, NewResponse)
        config.add_route('cors', '/{path:.*}', request_method='OPTIONS')

        # Konfigurasi model, template, dan routes
        config.include('.models')
        config.include('pyramid_jinja2')
        config.include('.routes')
        config.scan()
    return config.make_wsgi_app()
