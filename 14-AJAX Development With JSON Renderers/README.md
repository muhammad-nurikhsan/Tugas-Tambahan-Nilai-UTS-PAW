# AJAX Development With JSON Renderers

## Identitas
Muhammad Nurikhsan (123140057)

## JSON Renderer
```python
@view_config(route_name='api_users', renderer='json')
def get_users(request):
    users = [
        {'id': 1, 'name': 'Alice'},
        {'id': 2, 'name': 'Bob'}
    ]
    return users
```

Dengan `renderer='json'`, return value automatically di-serialize jadi JSON response dengan `Content-Type: application/json`.

## Custom JSON Response
```python
from pyramid.response import Response
import json

def custom_json_view(request):
    data = {'status': 'ok', 'message': 'Success'}
    return Response(
        json.dumps(data),
        content_type='application/json'
    )
```

Manual approach kalau butuh custom headers atau status code.

## Handling POST JSON
```python
@view_config(route_name='api_create', 
             renderer='json', 
             request_method='POST')
def create_user(request):
    try:
        data = request.json_body
        name = data['name']
        email = data['email']
        
        # Create user logic
        user = User.create(name=name, email=email)
        
        return {
            'success': True,
            'user': {
                'id': user.id,
                'name': user.name
            }
        }
    except ValueError:
        return {'success': False, 'error': 'Invalid JSON'}
    except KeyError as e:
        return {'success': False, 'error': f'Missing field: {e}'}
```

## Error Handling untuk API
```python
from pyramid.httpexceptions import HTTPBadRequest

@view_config(route_name='api_item', renderer='json')
def get_item(request):
    item_id = request.matchdict['id']
    item = Item.get(item_id)
    
    if not item:
        raise HTTPBadRequest(
            json_body={'error': 'Item not found'}
        )
    
    return {'item': item.to_dict()}
```

## Frontend Integration
```javascript
// GET request
fetch('/api/users')
    .then(res => res.json())
    .then(data => {
        console.log(data);
    });

// POST request
fetch('/api/create', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        name: 'Charlie',
        email: 'charlie@example.com'
    })
})
.then(res => res.json())
.then(data => {
    if (data.success) {
        console.log('User created:', data.user);
    }
});
```

## Analisis
JSON renderer adalah feature paling essential untuk modern web apps. Pyramid automatically handle serialization - tinggal return Python dicts/lists, framework handle the rest.

`request.json_body` convenient untuk parse incoming JSON. Auto-raise ValueError kalau JSON invalid, tapi should wrap dalam try-except untuk proper error response.

## Custom JSON Serialization
```python
from datetime import datetime
from pyramid.renderers import JSON

json_renderer = JSON()

def datetime_adapter(obj, request):
    return obj.isoformat()

json_renderer.add_adapter(datetime, datetime_adapter)

config.add_renderer('json', json_renderer)
```

By default, Pyramid nggak bisa serialize datetime objects. Need custom adapter.

## CORS untuk API
```python
@view_config(route_name='api', renderer='json')
def api_view(request):
    response = {'data': 'value'}
    request.response.headers.update({
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE',
    })
    return response
```

Kalau API diakses dari different domain, need CORS headers. Consider pakai `pyramid-cors` package untuk handle ini automatically.

## REST API Pattern
Pyramid's JSON renderer + routing predicates = perfect untuk REST APIs. Lightweight alternative to Django REST Framework atau Flask-RESTful, tapi manual setup.

## Best Practices:
1. **Consistent Structure**: Use consistent JSON structure
2. **Status Codes**: Use proper HTTP status codes
3. **Error Messages**: Provide clear error messages
4. **Validation**: Validate input data
5. **CORS**: Handle CORS untuk cross-origin requests


## Kesimpulan:
JSON renderers membuat building modern AJAX-driven applications simple dan straightforward.
