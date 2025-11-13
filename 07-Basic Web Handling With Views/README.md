# Basic Web Handling With Views

## Identitas
Muhammad Nurikhsan (123140057)

## View Functions
```python
from pyramid.response import Response

def hello_view(request):
    return Response('Hello')

def goodbye_view(request):
    return Response('Goodbye')
```

## View Configuration
```python
# Cara 1: Imperative
config.add_route('hello', '/hello')
config.add_view(hello_view, route_name='hello')

# Cara 2: Declarative dengan decorator
from pyramid.view import view_config

@view_config(route_name='hello')
def hello_view(request):
    return Response('Hello')
```

## Request Object
```python
def detail_view(request):
    # Query params
    name = request.params.get('name', 'Guest')
    
    # POST data
    if request.method == 'POST':
        data = request.POST.get('data')
    
    # Headers
    user_agent = request.headers.get('User-Agent')
    
    return Response(f'Hello {name}')
```

## Analisis
View di Pyramid itu simple - function yang terima `request` dan return response. Request object punya semua info HTTP: params, headers, method, cookies, dll.

Pyramid support dua style konfigurasi:
1. **Imperative**: Manual call `add_route` dan `add_view`. More control tapi verbose.
2. **Declarative**: Pakai decorator `@view_config`. Cleaner tapi butuh `config.scan()`.

Gw lebih suka declarative karena routing logic ada deket view function-nya. Tapi imperative berguna kalau butuh dynamic routing atau conditional registration.

## Response Types
```python
from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound

# Plain text
return Response('text')

# Redirect
return HTTPFound(location='/other')

# Custom status
return Response('Not found', status=404)
```

HTTPExceptions approach untuk redirect/error lumayan elegant - raise exception daripada return response code biasa.

## Catatan
View function harus return response object atau dict (kalau pakai renderer). Kalau return string mentah akan error, beda sama Flask yang auto-wrap ke Response.