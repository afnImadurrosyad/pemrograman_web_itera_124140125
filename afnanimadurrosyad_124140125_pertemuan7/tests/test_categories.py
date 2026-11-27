import os

import pytest
import transaction
from webtest import TestApp
from pyramid.paster import get_app

from products_api.models import get_tm_session
from products_api.models.category import Category
from products_api.models.meta import Base

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(HERE)


@pytest.fixture(scope='module')
def testapp():
    """Build the app with testing.ini (SQLite in-memory) and seed 1 category."""
    app = get_app(os.path.join(PROJECT_ROOT, 'testing.ini'))
    session_factory = app.registry['dbsession_factory']
    engine = session_factory().get_bind()
    Base.metadata.create_all(engine)
    with transaction.manager:
        dbsession = get_tm_session(session_factory, transaction.manager)
        dbsession.add(Category(
            name='Elektronik',
            description='Perangkat elektronik',
        ))
    yield TestApp(app)
    Base.metadata.drop_all(engine)


def test_get_categories_returns_seeded(testapp):
    """GET /api/v1/categories returns the seeded category."""
    resp = testapp.get('/api/v1/categories', status=200)
    assert len(resp.json) == 1
    assert resp.json[0]['name'] == 'Elektronik'
    assert resp.json[0]['is_active'] is True


def test_create_category(testapp):
    """POST /api/v1/categories creates a category and returns 201."""
    resp = testapp.post_json('/api/v1/categories', {
        'name': 'Pakaian',
        'description': 'Pakaian dan aksesori',
    }, status=201)
    assert resp.json['name'] == 'Pakaian'
    assert resp.json['id'] is not None
    assert resp.json['products'] == []


def test_create_category_duplicate_name(testapp):
    """POST with a duplicate category name returns 400."""
    resp = testapp.post_json('/api/v1/categories', {
        'name': 'Elektronik',
        'description': 'Nama sama',
    }, status=400)
    assert 'name' in resp.json['errors']


def test_create_category_invalid_name(testapp):
    """POST with a too-short name fails Marshmallow validation (400)."""
    resp = testapp.post_json('/api/v1/categories', {
        'name': 'X',
    }, status=400)
    assert 'name' in resp.json['errors']


def test_get_category_detail_includes_products(testapp):
    """GET /api/v1/categories/{id} returns the category with its products."""
    created = testapp.post_json('/api/v1/categories', {
        'name': 'Olahraga',
        'description': 'Peralatan olahraga',
    }, status=201)
    category_id = created.json['id']
    testapp.post_json('/api/v1/products', {
        'name': 'Bola Basket',
        'description': 'Bola basket ukuran 7',
        'price': 199.99,
        'sku': 'CAT2001',
        'category_id': category_id,
    }, status=201)
    resp = testapp.get(f'/api/v1/categories/{category_id}', status=200)
    assert resp.json['name'] == 'Olahraga'
    assert len(resp.json['products']) == 1
    assert resp.json['products'][0]['sku'] == 'CAT2001'


def test_get_category_not_found(testapp):
    """GET /api/v1/categories/{id} with an unknown ID returns 404."""
    testapp.get('/api/v1/categories/99999', status=404)


def test_update_and_delete_category(testapp):
    """PUT updates a category; DELETE soft-deletes it (204, then 404)."""
    created = testapp.post_json('/api/v1/categories', {
        'name': 'Kategori Hapus',
        'description': 'Akan dihapus',
    }, status=201)
    category_id = created.json['id']
    resp = testapp.put_json(f'/api/v1/categories/{category_id}', {
        'description': 'Deskripsi diperbarui',
    }, status=200)
    assert resp.json['description'] == 'Deskripsi diperbarui'
    assert resp.json['name'] == 'Kategori Hapus'
    testapp.delete(f'/api/v1/categories/{category_id}', status=204)
    testapp.get(f'/api/v1/categories/{category_id}', status=404)
