# Handling Web Requests and Responses

## Identitas
Muhammad Nurikhsan (123140057)

## Request Object Properties
```python
def my_view(request):
    # Method
    method = request.method  # GET, POST, PUT, DELETE
    
    # URL parts
    url = request.url  # Full URL
    path = request.path  # Path only
    host = request.host  # Domain
    
    # Parameters
    query_params = request.params  # ?name=value
    post_data = request.POST  # Form data
    json_data = request.json_body  # JSON payload
    
    # Headers
    content_type = request.content_type
    auth = request.headers.get('Authorization')
    
    # Cookies
    session_id = request.cookies.get('session_id')
```

## Response Types
```python
from pyramid.response import Response, FileResponse
from pyramid.httpexceptions import (
    HTTPFound, HTTPNotFound, HTTPForbidden
)

# Text response
return Response('Hello', content_type='text/plain')

# JSON response (manual)
import json
return Response(
    json.dumps({'status': 'ok'}),
    content_type='application/json'
)

# Redirect
return HTTPFound(location='/home')

# File download
return FileResponse('/path/to/file.pdf')

# Error responses
return HTTPNotFound()  # 404
return HTTPForbidden()  # 403
```

## Custom Response Headers
```python
response = Response('Data')
response.headers['X-Custom-Header'] = 'value'
response.set_cookie('session', 'abc123', max_age=3600)
return response
```

## Analisis
Request object di Pyramid comprehensive - cover semua aspek HTTP request. Property `json_body` convenient untuk REST API, auto-parse JSON dan raise error kalau invalid.

Response handling pakai exception approach untuk HTTP errors. `HTTPNotFound`, `HTTPForbidden`, etc adalah exception classes yang bisa di-raise atau di-return. Ini interesting design - bikin error handling bisa pakai try-except.

```python
def view(request):
    user = User.get(id)
    if not user:
        raise HTTPNotFound()
    return {'user': user}
```

Raise vs return sama aja effect-nya, tapi raise more semantic untuk error cases.

## Request Matching
```python
# Match route parameters
article_id = request.matchdict['id']

# Check matched route
route_name = request.matched_route.name
```

`matchdict` contain route placeholders. Misalnya route `/article/{id}` akan punya `matchdict['id']`.

## File Upload
```python
def upload_view(request):
    uploaded_file = request.POST['file']
    filename = uploaded_file.filename
    content = uploaded_file.file.read()
    
    # Save file
    with open(f'/uploads/{filename}', 'wb') as f:
        f.write(content)
```

File upload handling cukup straightforward, similar dengan framework lain.

## JSON Body Parsing
Pyramid automatically parse JSON kalau `Content-Type: application/json`. Kalau invalid JSON, raise `ValueError`. Should wrap dalam try-except untuk production code.

## Best Practices:
1. Validate input dari request
2. Use proper HTTP status codes
3. Set appropriate content types
4. Handle errors gracefully
5. Secure cookie handling

## Kesimpulan:
Memahami request/response lifecycle critical untuk building robust web applications.