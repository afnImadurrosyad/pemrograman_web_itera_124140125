from pyramid.view import view_config


@view_config(route_name='cors', renderer='json')
def cors_options_view(request):
    """Menangani permintaan preflight OPTIONS dari browser."""
    request.response.headers.update({
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST, GET, DELETE, PUT, OPTIONS',
        'Access-Control-Allow-Headers': 'Origin, Content-Type, Accept, Authorization',
        'Access-Control-Max-Age': '1728000',
    })
    return {}
