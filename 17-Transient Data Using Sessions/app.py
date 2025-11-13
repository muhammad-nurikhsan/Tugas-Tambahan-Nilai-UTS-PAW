from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.session import SignedCookieSessionFactory
from pyramid.httpexceptions import HTTPFound

def home(request):
    username = request.session.get('username')
    if username:
        html = f'''
        <h1>Welcome, {username}!</h1>
        <a href="/logout">Logout</a>
        '''
    else:
        html = '''
        <h1>Not logged in</h1>
        <form method="POST" action="/login">
            <input name="username" placeholder="Username">
            <button type="submit">Login</button>
        </form>
        '''
    return Response(html)

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        request.session['username'] = username
        request.session.flash(f'Welcome {username}!', 'success')
        return HTTPFound(location='/')
    return HTTPFound(location='/')

def logout(request):
    request.session.invalidate()
    return HTTPFound(location='/')

def flash_demo(request):
    messages = request.session.pop_flash('success')
    if messages:
        html = '<h1>Flash Messages:</h1>'
        for msg in messages:
            html += f'<p>{msg}</p>'
    else:
        html = '<h1>No messages</h1>'
    html += '<a href="/">Home</a>'
    return Response(html)

if __name__ == '__main__':
    session_factory = SignedCookieSessionFactory('secret_key_12345')
    
    with Configurator(session_factory=session_factory) as config:
        config.add_route('home', '/')
        config.add_route('login', '/login')
        config.add_route('logout', '/logout')
        config.add_route('flash', '/flash')
        
        config.add_view(home, route_name='home')
        config.add_view(login, route_name='login')
        config.add_view(logout, route_name='logout')
        config.add_view(flash_demo, route_name='flash')
        
        app = config.make_wsgi_app()
    
    from waitress import serve
    serve(app, host='0.0.0.0', port=6543)