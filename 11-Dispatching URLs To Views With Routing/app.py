from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config

def home(request):
    html = '''
    <h1>Routing Examples</h1>
    <ul>
        <li><a href="/user/john">Dynamic: /user/{username}</a></li>
        <li><a href="/blog/2024/12/my-post">Multi-segment: /blog/{year}/{month}/{slug}</a></li>
        <li><a href="/article/123">Regex: /article/{id:\d+}</a></li>
        <li><a href="/api/data">API GET</a></li>
    </ul>
    '''
    return Response(html)

def user_profile(request):
    username = request.matchdict['username']
    return Response(f'<h1>Profile: {username}</h1>')

def blog_post(request):
    year = request.matchdict['year']
    month = request.matchdict['month']
    slug = request.matchdict['slug']
    return Response(f'<h1>Blog: {year}/{month}/{slug}</h1>')

def article_detail(request):
    article_id = request.matchdict['id']
    return Response(f'<h1>Article ID: {article_id}</h1>')

@view_config(route_name='api_get', request_method='GET', renderer='json')
def api_get(request):
    return {'method': 'GET', 'data': [1, 2, 3]}

@view_config(route_name='api_post', request_method='POST', renderer='json')
def api_post(request):
    return {'method': 'POST', 'status': 'created'}

if __name__ == '__main__':
    with Configurator() as config:
        config.add_route('home', '/')
        config.add_route('user', '/user/{username}')
        config.add_route('blog', '/blog/{year}/{month}/{slug}')
        config.add_route('article', r'/article/{id:\d+}')
        config.add_route('api_get', '/api/data', request_method='GET')
        config.add_route('api_post', '/api/data', request_method='POST')
        
        config.add_view(home, route_name='home')
        config.add_view(user_profile, route_name='user')
        config.add_view(blog_post, route_name='blog')
        config.add_view(article_detail, route_name='article')
        config.scan()
        
        app = config.make_wsgi_app()
    
    from waitress import serve
    serve(app, host='0.0.0.0', port=6543)