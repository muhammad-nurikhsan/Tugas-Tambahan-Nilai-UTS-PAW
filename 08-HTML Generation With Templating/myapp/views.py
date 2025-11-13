from pyramid.view import view_config

@view_config(route_name='home', renderer='templates/home.pt')
def home_view(request):
    return {
        'project': 'Templating Tutorial',
        'description': 'Learning Chameleon templates in Pyramid'
    }

@view_config(route_name='about', renderer='templates/about.pt')
def about_view(request):
    return {
        'title': 'About Page',
        'features': [
            'Template Inheritance',
            'Variables and Expressions',
            'Loops and Conditionals',
            'Template Macros'
        ]
    }

@view_config(route_name='users', renderer='templates/users.pt')
def users_view(request):
    return {
        'users': [
            {'id': 1, 'name': 'Alice', 'role': 'Admin', 'active': True},
            {'id': 2, 'name': 'Bob', 'role': 'User', 'active': True},
            {'id': 3, 'name': 'Charlie', 'role': 'User', 'active': False},
            {'id': 4, 'name': 'Diana', 'role': 'Moderator', 'active': True},
        ]
    }