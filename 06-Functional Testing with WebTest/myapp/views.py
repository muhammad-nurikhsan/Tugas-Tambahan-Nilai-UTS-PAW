from pyramid.view import view_config
from pyramid.response import Response

@view_config(route_name='home')
def home_view(request):
    return Response('<h1>Testing Tutorial</h1>')

@view_config(route_name='api', renderer='json')
def api_view(request):
    return {
        'status': 'ok',
        'data': [1, 2, 3, 4, 5]
    }