from pyramid.config import Configurator
from pyramid.response import Response
import logging
import logging.config

logging.config.fileConfig('logging.ini')
log = logging.getLogger(__name__)

def home(request):
    log.info('Home page accessed')
    return Response('<h1>Check console for logs</h1>')

def debug_view(request):
    log.debug('Debug message')
    log.info('Info message')
    log.warning('Warning message')
    log.error('Error message')
    return Response('<h1>Logs written! Check console and app.log</h1>')

def error_view(request):
    try:
        result = 1 / 0
    except Exception as e:
        log.error(f'Error occurred: {e}', exc_info=True)
        return Response('Error logged!')

if __name__ == '__main__':
    with Configurator() as config:
        config.add_route('home', '/')
        config.add_route('debug', '/debug')
        config.add_route('error', '/error')
        config.add_view(home, route_name='home')
        config.add_view(debug_view, route_name='debug')
        config.add_view(error_view, route_name='error')
        app = config.make_wsgi_app()
    
    from waitress import serve
    log.info('Server starting...')
    serve(app, host='0.0.0.0', port=6543)