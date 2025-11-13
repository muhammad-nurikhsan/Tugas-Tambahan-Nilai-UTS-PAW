from pyramid.config import Configurator
from pyramid.response import Response, FileResponse
from pyramid.httpexceptions import HTTPFound, HTTPNotFound
import json

def home(request):
    html = '''
    <h1>Request/Response Demo</h1>
    <ul>
        <li><a href="/query?name=John&age=25">Query Params</a></li>
        <li><a href="/headers">Headers</a></li>
        <li><a href="/json">JSON Response</a></li>
        <li><a href="/redirect">Redirect</a></li>
        <li><a href="/cookie">Set Cookie</a></li>
    </ul>
    '''
    return Response(html)

def query_demo(request):
    name = request.params.get('name', 'Guest')
    age = request.params.get('age', 'unknown')
    html = f'<h1>Hello {name}, age {age}</h1>'
    return Response(html)

def headers_demo(request):
    user_agent = request.headers.get('User-Agent', 'unknown')
    method = request.method
    url = request.url
    html = f'''
    <h1>Request Info</h1>
    <p>Method: {method}</p>
    <p>URL: {url}</p>
    <p>User-Agent: {user_agent}</p>
    '''
    return Response(html)

def json_demo(request):
    data = {'status': 'ok', 'items': [1, 2, 3]}
    return Response(json.dumps(data), content_type='application/json')

def redirect_demo(request):
    return HTTPFound(location='/')

def cookie_demo(request):
    response = Response('<h1>Cookie Set!</h1><a href="/">Home</a>')
    response.set_cookie('username', 'john', max_age=3600)
    return response

if __name__ == '__main__':
    with Configurator() as config:
        config.add_route('home', '/')
        config.add_route('query', '/query')
        config.add_route('headers', '/headers')
        config.add_route('json', '/json')
        config.add_route('redirect', '/redirect')
        config.add_route('cookie', '/cookie')
        
        config.add_view(home, route_name='home')
        config.add_view(query_demo, route_name='query')
        config.add_view(headers_demo, route_name='headers')
        config.add_view(json_demo, route_name='json')
        config.add_view(redirect_demo, route_name='redirect')
        config.add_view(cookie_demo, route_name='cookie')
        
        app = config.make_wsgi_app()
    
    from waitress import serve
    serve(app, host='0.0.0.0', port=6543)