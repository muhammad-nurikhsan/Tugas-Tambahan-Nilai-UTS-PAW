from pyramid.config import Configurator

def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.add_route('home', '/')
    config.add_route('api', '/api/data')
    config.scan()
    return config.make_wsgi_app()