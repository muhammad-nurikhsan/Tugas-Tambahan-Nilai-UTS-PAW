from pyramid.config import Configurator


def main(global_config, **settings):
    """
    This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    
    # Add routes
    config.add_route('home', '/')
    config.add_route('hello', '/howdy')
    
    # Scan for @view_config decorators
    config.scan('.views')
    
    return config.make_wsgi_app()