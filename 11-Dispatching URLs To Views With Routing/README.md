# Dispatching URLs To Views With Routing

## Identitas
Muhammad Nurikhsan (123140057)

## Basic Routing
```python
config.add_route('home', '/')
config.add_route('about', '/about')
config.add_route('contact', '/contact')
```

## Dynamic Segments
```python
# Single parameter
config.add_route('user_profile', '/user/{username}')

# Multiple parameters
config.add_route('blog_post', '/blog/{year}/{month}/{slug}')

# Access dalam view
@view_config(route_name='user_profile')
def profile(request):
    username = request.matchdict['username']
    return {'username': username}
```

## Route Patterns
```python
# Optional segment dengan *
config.add_route('docs', '/docs/*traverse')

# Regex constraints
config.add_route('article', '/article/{id:\d+}')

# Remainder path
config.add_route('static', '/static/*subpath')
```

## Route Predicates
```python
# Method-specific routes
config.add_route('api_get', '/api/data', request_method='GET')
config.add_route('api_post', '/api/data', request_method='POST')

# Header-based routing
config.add_route('api_v1', '/api', 
                 header='X-API-Version:1')

# Custom predicates
def is_mobile(info, request):
    return 'mobile' in request.user_agent.lower()

config.add_route('mobile', '/m', custom_predicates=(is_mobile,))
```

## Analisis
Routing di Pyramid flexible banget. Dynamic segments pakai curly braces `{name}`, similar dengan Flask. Regex constraints powerful untuk validation - misalnya `{id:\d+}` ensure id harus numeric.

Route predicates adalah killer feature. Bisa routing based on HTTP method, headers, atau custom logic. Ini eliminate need untuk if-else dalam view:

```python
# Tanpa predicates (bad)
def api_view(request):
    if request.method == 'GET':
        # GET logic
    elif request.method == 'POST':
        # POST logic

# Dengan predicates (good)
@view_config(route_name='api_get')
def api_get(request):
    # GET logic

@view_config(route_name='api_post')
def api_post(request):
    # POST logic
```

## URL Generation
```python
# Generate URL from route name
url = request.route_url('user_profile', username='john')
# Result: /user/john

# Dengan query params
url = request.route_url('search', _query={'q': 'python'})
# Result: /search?q=python
```

URL generation penting untuk avoid hardcoded URLs. Kalau route pattern berubah, semua generated URLs otomatis update.

## Route Order
Route matching first-come-first-served. Order matters:
```python
# BAD - specific after general
config.add_route('catchall', '/{path}')
config.add_route('about', '/about')  # Never matched!

# GOOD - specific before general
config.add_route('about', '/about')
config.add_route('catchall', '/{path}')
```

Always define specific routes sebelum catch-all routes.

## REST-ful Routing
```python
config.add_route('articles', '/articles', 
                 request_method='GET')
config.add_route('article_create', '/articles', 
                 request_method='POST')
config.add_route('article_detail', '/articles/{id}', 
                 request_method='GET')
config.add_route('article_update', '/articles/{id}', 
                 request_method='PUT')
config.add_route('article_delete', '/articles/{id}', 
                 request_method='DELETE')
```

Predicates bikin REST API routing clean tanpa perlu check method manually.

## Best Practices:
1. Use descriptive route names
2. Group related routes
3. Use URL generation, not hardcoding
4. Document route patterns
5. Consider RESTful conventions

## Kesimpulan:
Proper routing design crucial untuk maintainable URLs dan good user experience.