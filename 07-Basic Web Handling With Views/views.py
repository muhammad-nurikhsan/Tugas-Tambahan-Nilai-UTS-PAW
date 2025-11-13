from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound, HTTPNotFound


@view_config(route_name='home')
def home_view(request):
    """
    Home page view - returns simple response
    """
    return Response('Welcome to Pyramid Views Tutorial!')


@view_config(route_name='about')
def about_view(request):
    """
    About page - demonstrates Response customization
    """
    response = Response('This is the About page')
    response.content_type = 'text/plain'
    response.status_int = 200
    return response


@view_config(route_name='contact')
def contact_view(request):
    """
    Contact page - demonstrates dictionary return
    """
    return {
        'page': 'Contact',
        'email': 'contact@example.com',
        'phone': '+1234567890'
    }


@view_config(route_name='user')
def user_view(request):
    """
    User detail page - demonstrates URL parameters
    """
    user_id = request.matchdict['id']
    
    # Simulate database lookup
    users = {
        '1': {'name': 'Alice', 'email': 'alice@example.com'},
        '2': {'name': 'Bob', 'email': 'bob@example.com'},
        '3': {'name': 'Charlie', 'email': 'charlie@example.com'},
    }
    
    user = users.get(user_id)
    
    if not user:
        raise HTTPNotFound(f'User {user_id} not found')
    
    html = f"""
    <html>
        <head><title>User Profile</title></head>
        <body>
            <h1>{user['name']}</h1>
            <p>Email: {user['email']}</p>
            <p>ID: {user_id}</p>
        </body>
    </html>
    """
    
    return Response(html)


@view_config(route_name='search')
def search_view(request):
    """
    Search page - demonstrates query parameters
    """
    # Get query parameter
    query = request.params.get('q', '')
    category = request.params.get('category', 'all')
    
    if not query:
        return Response('Please provide a search query. Example: /search?q=pyramid')
    
    # Simulate search results
    results = [
        f'Result 1 for "{query}" in {category}',
        f'Result 2 for "{query}" in {category}',
        f'Result 3 for "{query}" in {category}',
    ]
    
    html = f"""
    <html>
        <head><title>Search Results</title></head>
        <body>
            <h1>Search Results for: {query}</h1>
            <p>Category: {category}</p>
            <ul>
                {''.join(f'<li>{r}</li>' for r in results)}
            </ul>
        </body>
    </html>
    """
    
    return Response(html)


# Example of view with multiple HTTP methods
@view_config(route_name='contact', request_method='POST')
def contact_submit(request):
    """
    Handle contact form submission
    """
    name = request.POST.get('name', '')
    email = request.POST.get('email', '')
    message = request.POST.get('message', '')
    
    # Process form data (save to database, send email, etc.)
    
    # Redirect after POST (PRG pattern)
    return HTTPFound(location='/contact?submitted=true')