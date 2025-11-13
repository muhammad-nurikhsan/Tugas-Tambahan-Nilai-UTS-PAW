# CSS/JS/Images Files With Static Assets

## Identitas
Muhammad Nurikhsan (123140057)

## Static View Configuration
```python
config.add_static_view(name='static', path='myapp:static')
```

Parameter:
- `name`: URL prefix (e.g., `/static/`)
- `path`: Directory path dalam package

## Directory Structure
```
myapp/
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── app.js
│   └── images/
│       └── logo.png
```

## Menggunakan di Template
```html
<!-- Manual URL -->
<link rel="stylesheet" href="/static/css/style.css">

<!-- Dengan request.static_url -->
<link rel="stylesheet" href="${request.static_url('myapp:static/css/style.css')}">

<script src="${request.static_url('myapp:static/js/app.js')}"></script>
<img src="${request.static_url('myapp:static/images/logo.png')}">
```

## Cache Busting
```python
# Production config
config.add_static_view(
    name='static',
    path='myapp:static',
    cache_max_age=3600
)

# Generate URL dengan cache buster
url = request.static_url('myapp:static/css/style.css', 
                          _query={'v': '1.2.0'})
# Result: /static/css/style.css?v=1.2.0
```

## Analisis
Static assets handling di Pyramid straightforward tapi ada nuances. `add_static_view` basically expose directory ke URL path tertentu.

Syntax `myapp:static` adalah package-relative path. Colon notation berguna kalau package di-install sebagai egg, path absolute tetap work.

`request.static_url()` better daripada hardcode `/static/` karena:
1. Kalau static URL prefix berubah, semua references tetap valid
2. Support CDN atau external static host
3. Bisa generate absolute URLs

## Multiple Static Views
```python
# CSS/JS dari package
config.add_static_view('static', 'myapp:static')

# User uploads dari filesystem
config.add_static_view('uploads', '/var/www/uploads')

# CDN untuk production
if production:
    config.add_static_view('static', 
                           'https://cdn.example.com/static/')
```

Bisa define multiple static views untuk different purposes.

## Security Consideration
```python
# Restrict file extensions
config.add_static_view(
    'static', 
    'myapp:static',
    permission='view'
)
```

Jangan serve uploaded files dari static directory yang sama dengan app assets. User bisa upload malicious files (PHP, exe, etc).

Best practice:
- Static app assets: `/static/`
- User uploads: `/media/` dengan validation

## Asset Pipeline Alternative
Untuk production, consider pakai webpack/vite untuk bundle CSS/JS. Pyramid cuma serve hasil build, bukan source files.

```python
# Serve bundled assets
config.add_static_view('assets', 'myapp:dist/')
```

Pyramid nggak punya built-in asset pipeline seperti Rails. It's just serving files, processing/minification harus external.

## Best Practices:
1. **Organize by type**: CSS, JS, images dalam folders terpisah
2. **Minification**: Minify CSS/JS untuk production
3. **Versioning**: Use cache busting untuk updates
4. **CDN**: Consider CDN untuk popular libraries
5. **Compression**: Enable gzip compression

## Cache Control:
```python
config.add_static_view('static', 'static', cache_max_age=3600)
```

## Kesimpulan:
Proper static asset management penting untuk performance dan maintainability.