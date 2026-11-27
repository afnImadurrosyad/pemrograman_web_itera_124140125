from pyramid.httpexceptions import HTTPNotFound
from pyramid.view import view_config


@view_config(route_name='home', renderer='json')
def home(request):
    """Halaman utama API: info singkat proyek dan daftar endpoint."""
    return {
        'status': 'ok',
        'service': 'ProductsAPI',
        'description': 'REST API Manajemen Kategori dan Produk (Praktikum PAW Pertemuan 7)',
        'endpoints': [
            'GET /api/v1/categories',
            'GET /api/v1/categories/{id}',
            'POST /api/v1/categories',
            'PUT /api/v1/categories/{id}',
            'DELETE /api/v1/categories/{id}',
            'GET /api/v1/products',
            'GET /api/v1/products/{id}',
            'POST /api/v1/products',
            'PUT /api/v1/products/{id}',
            'DELETE /api/v1/products/{id}',
        ],
    }


@view_config(context=HTTPNotFound, renderer='json')
def notfound(request):
    """Mengembalikan 404 dalam format JSON agar konsisten dengan API."""
    request.response.status = 404
    return {'error': 'Resource not found'}
