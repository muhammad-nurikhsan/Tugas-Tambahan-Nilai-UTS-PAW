from pyramid.config import Configurator
from sqlalchemy.orm import sessionmaker
from .models import init_db

def main(global_config, **settings):
    engine = init_db()
    Session = sessionmaker(bind=engine)
    
    config = Configurator(settings=settings)
    config.registry['dbsession'] = Session
    
    config.add_route('home', '/')
    config.add_route('users_json', '/users')
    config.add_route('users_html', '/users/html')
    config.scan()
    
    return config.make_wsgi_app()