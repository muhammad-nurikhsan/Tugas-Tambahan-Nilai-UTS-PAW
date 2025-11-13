from pyramid.config import Configurator
from pyramid.view import view_config
from pyramid.response import Response
from pyramid.httpexceptions import HTTPForbidden

# Base class
class BaseView:
    def __init__(self, request):
        self.request = request
        self.user = {'id': 1, 'name': 'John', 'is_admin': True}
    
    def require_auth(self):
        if not self.user:
            raise HTTPForbidden()

# Mixin
class JSONMixin:
    def json_response(self, data):
        import json
        return Response(json.dumps(data), content_type='application/json')

# Combined
class APIViews(JSONMixin, BaseView):
    @view_config(route_name='api_profile')
    def profile(self):
        self.require_auth()
        return self.json_response({'user': self.user})
    
    @view_config(route_name='api_admin')
    def admin(self):
        self.require_auth()
        if not self.user.get('is_admin'):
            raise HTTPForbidden()
        return self.json_response({'message': 'Admin access granted'})

def home(request):
    html = '''
    <h1>View Classes Advanced</h1>
    <ul>
        <li><a href="/api/profile">/api/profile</a></li>
        <li><a href="/api/admin">/api/admin</a></li>
    </ul>
    '''
    return Response(html)

if __name__ == '__main__':
    with Configurator() as config:
        config.add_route('home', '/')
        config.add_route('api_profile', '/api/profile')
        config.add_route('api_admin', '/api/admin')
        config.add_view(home, route_name='home')
        config.scan()
        app = config.make_wsgi_app()
    
    from waitress import serve
    serve(app, host='0.0.0.0', port=6543)