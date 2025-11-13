from pyramid.config import Configurator
from pyramid.response import Response

def hello_world(request):
    return Response('Hello World from Pyramid!')

if __name__ == '__main__':
    with Configurator() as config:
        config.add_route('hello', '/')
        config.add_view(hello_world, route_name='hello')
        app = config.make_wsgi_app()
    
    from waitress import serve
    print('Server running on http://localhost:6543')
    serve(app, host='0.0.0.0', port=6543)