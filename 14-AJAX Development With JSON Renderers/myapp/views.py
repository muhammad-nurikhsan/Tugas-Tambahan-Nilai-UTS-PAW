from pyramid.view import view_config

@view_config(route_name='home', renderer='templates/home.pt')
def home(request):
    return {}

@view_config(route_name='api_users', renderer='json')
def get_users(request):
    return [
        {'id': 1, 'name': 'Alice', 'email': 'alice@example.com'},
        {'id': 2, 'name': 'Bob', 'email': 'bob@example.com'},
    ]

@view_config(route_name='api_create', renderer='json', request_method='POST')
def create_user(request):
    try:
        data = request.json_body
        return {'success': True, 'user': data}
    except:
        return {'success': False, 'error': 'Invalid JSON'}