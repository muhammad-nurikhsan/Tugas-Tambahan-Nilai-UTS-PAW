from pyramid.config import Configurator

def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')
    config.add_route('home', '/')
    config.add_route('about', '/about')
    config.add_route('users', '/users')
    config.scan()
    return config.make_wsgi_app()