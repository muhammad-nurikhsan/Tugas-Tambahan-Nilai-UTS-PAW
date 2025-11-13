from pyramid.view import view_config
from pyramid.response import Response
from sqlalchemy.orm import sessionmaker
from .models import User

@view_config(route_name='home')
def home(request):
    html = '''
    <h1>SQLAlchemy Demo</h1>
    <ul>
        <li><a href="/users">List Users (JSON)</a></li>
        <li><a href="/users/html">List Users (HTML)</a></li>
    </ul>
    '''
    return Response(html)

@view_config(route_name='users_json', renderer='json')
def users_json(request):
    Session = request.registry['dbsession']
    session = Session()
    users = session.query(User).all()
    return [u.to_dict() for u in users]

@view_config(route_name='users_html')
def users_html(request):
    Session = request.registry['dbsession']
    session = Session()
    users = session.query(User).all()
    
    html = '<h1>Users</h1><table border="1"><tr><th>ID</th><th>Username</th><th>Email</th></tr>'
    for u in users:
        html += f'<tr><td>{u.id}</td><td>{u.username}</td><td>{u.email}</td></tr>'
    html += '</table><a href="/">Home</a>'
    return Response(html)