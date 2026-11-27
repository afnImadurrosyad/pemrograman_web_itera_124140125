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


def _create_product(testapp, sku, name='Produk Uji', price=99.99, category_id=1):
    return testapp.post_json('/api/v1/products', {
        'name': name,
        'description': 'Produk untuk pengujian',
        'price': price,
        'sku': sku,
        'category_id': category_id,
    }, status=201)


def test_get_products_empty(testapp):
    """GET /api/v1/products returns an empty list before any product exists."""
    resp = testapp.get('/api/v1/products', status=200)
    assert resp.json == []


def test_create_product(testapp):
    """POST /api/v1/products creates a product and returns 201."""
    resp = _create_product(testapp, 'TST1001', 'Laptop Uji')
    assert resp.json['name'] == 'Laptop Uji'
    assert resp.json['sku'] == 'TST1001'
    assert resp.json['price'] == 99.99
    assert resp.json['category_id'] == 1
    assert resp.json['category']['name'] == 'Elektronik'
    assert resp.json['is_active'] is True
    assert resp.json['id'] is not None


def test_create_product_duplicate_sku(testapp):
    """POST with a duplicate SKU returns 400."""
    _create_product(testapp, 'TST1002')
    resp = testapp.post_json('/api/v1/products', {
        'name': 'Produk Duplikat',
        'description': 'SKU sama',
        'price': 50.0,
        'sku': 'TST1002',
        'category_id': 1,
    }, status=400)
    assert 'sku' in resp.json['errors']


def test_create_product_invalid_price(testapp):
    """POST with a negative price fails Marshmallow validation (400)."""
    resp = testapp.post_json('/api/v1/products', {
        'name': 'Produk Harga Salah',
        'description': 'Harga negatif',
        'price': -10,
        'sku': 'TST1003',
        'category_id': 1,
    }, status=400)
    assert 'price' in resp.json['errors']


def test_create_product_unknown_category(testapp):
    """POST with a non-existent category_id returns 400."""
    resp = testapp.post_json('/api/v1/products', {
        'name': 'Produk Tanpa Kategori',
        'description': 'Kategori tidak ada',
        'price': 10.0,
        'sku': 'TST1004',
        'category_id': 9999,
    }, status=400)
    assert 'category_id' in resp.json['errors']


def test_get_product_detail(testapp):
    """GET /api/v1/products/{id} returns the product detail."""
    created = _create_product(testapp, 'TST1005', 'Produk Detail')
    product_id = created.json['id']
    resp = testapp.get(f'/api/v1/products/{product_id}', status=200)
    assert resp.json['sku'] == 'TST1005'
    assert resp.json['category']['name'] == 'Elektronik'


def test_get_product_not_found(testapp):
    """GET /api/v1/products/{id} with an unknown ID returns 404."""
    testapp.get('/api/v1/products/99999', status=404)


def test_update_product(testapp):
    """PUT /api/v1/products/{id} updates only the sent fields."""
    created = _create_product(testapp, 'TST1006', 'Produk Lama', price=10.0)
    product_id = created.json['id']
    resp = testapp.put_json(f'/api/v1/products/{product_id}', {
        'name': 'Produk Baru',
        'price': 109.99,
    }, status=200)
    assert resp.json['name'] == 'Produk Baru'
    assert resp.json['price'] == 109.99
    assert resp.json['sku'] == 'TST1006'


def test_delete_product(testapp):
    """DELETE /api/v1/products/{id} soft-deletes the product (204)."""
    created = _create_product(testapp, 'TST1007', 'Produk Hapus')
    product_id = created.json['id']
    testapp.delete(f'/api/v1/products/{product_id}', status=204)
    # Soft-deleted product no longer appears in the list or detail
    testapp.get(f'/api/v1/products/{product_id}', status=404)
    resp = testapp.get('/api/v1/products', status=200)
    assert all(p['id'] != product_id for p in resp.json)
