from pyramid.config import Configurator
from wsgiref.simple_server import make_server


def main(global_config=None, **settings):
    """Application factory"""
    config = Configurator(settings=settings)
    
    # Add routes
    config.add_route('home', '/')
    config.add_route('about', '/about')
    config.add_route('contact', '/contact')
    config.add_route('user', '/user/{id}')
    config.add_route('search', '/search')
    
    # Scan views
    config.scan('.views')
    
    return config.make_wsgi_app()


if __name__ == '__main__':
    app = main()
    server = make_server('0.0.0.0', 6543, app)
    print('Starting server on http://localhost:6543')
    server.serve_forever()