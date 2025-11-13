# Single-File Web Applications

## Identitas
Muhammad Nurikhsan (123140057)

## Konsep Dasar
Single-file application di Pyramid adalah cara paling sederhana untuk membuat web app. Semua konfigurasi, routing, dan view ada dalam satu file Python.

## Implementasi
```python
from pyramid.config import Configurator
from pyramid.response import Response

def hello_world(request):
    return Response('Hello World!')

if __name__ == '__main__':
    config = Configurator()
    config.add_route('hello', '/')
    config.add_view(hello_world, route_name='hello')
    app = config.make_wsgi_app()
    
    from waitress import serve
    serve(app, host='0.0.0.0', port=6543)
```

## Analisis
Pendekatan ini mirip Flask tapi lebih verbose. Pyramid memisahkan antara konfigurasi (`Configurator`), routing (`add_route`), dan view mapping (`add_view`).

Keuntungannya cocok untuk prototyping cepat atau microservice sederhana. Tapi untuk aplikasi besar, struktur ini jadi susah di-maintain karena semua tercampur dalam satu file.

Yang menarik adalah Pyramid pakai WSGI server (waitress) secara default, bukan development server seperti Flask. Ini lebih production-ready.

## Perbandingan dengan Framework Lain
- **Flask**: Lebih ringkas dengan decorator `@app.route()`
- **Django**: Tidak support single-file, harus pakai project structure
- **Pyramid**: Lebih eksplisit, good for learning tapi verbose

## Kesimpulan
Single-file cocok untuk belajar konsep dasar atau bikin API sederhana. Untuk real project, better pakai package structure.