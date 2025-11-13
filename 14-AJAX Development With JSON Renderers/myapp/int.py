from pyramid.config import Configurator

def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')
    config.add_static_view('static', 'myapp:static')
    config.add_route('home', '/')
    config.add_route('api_users', '/api/users')
    config.add_route('api_create', '/api/users/create')
    config.scan()
    return config.make_wsgi_app()