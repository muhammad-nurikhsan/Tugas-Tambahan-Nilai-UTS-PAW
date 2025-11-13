# Organizing Views With View Classes

## Identitas
Muhammad Nurikhsan (123140057)

## Class-Based Views
```python
from pyramid.view import view_config

class TutorialViews:
    def __init__(self, request):
        self.request = request
        
    @view_config(route_name='home', renderer='home.pt')
    def home(self):
        return {'name': 'Home View'}
    
    @view_config(route_name='about', renderer='about.pt')
    def about(self):
        return {'name': 'About View'}
```

## Shared Logic
```python
class TutorialViews:
    def __init__(self, request):
        self.request = request
        self.user = self.get_current_user()
    
    def get_current_user(self):
        # Shared logic untuk semua views
        user_id = self.request.session.get('user_id')
        return User.get(user_id)
    
    @view_config(route_name='profile')
    def profile(self):
        return {'user': self.user}
    
    @view_config(route_name='settings')
    def settings(self):
        return {'user': self.user}
```

## Analisis
View classes solve problem of code duplication. Kalau punya multiple views yang butuh logic sama (auth check, database connection, etc), class-based approach lebih DRY.

Constructor `__init__` dipanggil untuk setiap request dan receive request object. Ini tempat yang bagus untuk setup shared state atau dependencies.

Dibanding function-based views:
- **Pros**: Better organization, code reuse, easier testing
- **Cons**: Sedikit lebih verbose, overhead object creation

Pattern ini mirip Django's Class-Based Views tapi lebih lightweight. Django punya generic views (ListView, DetailView, etc), Pyramid lebih barebones - you build your own abstractions.

## View Class dengan Property
```python
class ArticleViews:
    def __init__(self, request):
        self.request = request
    
    @property
    def article_id(self):
        return self.request.matchdict['id']
    
    @view_config(route_name='article_view')
    def view(self):
        article = Article.get(self.article_id)
        return {'article': article}
    
    @view_config(route_name='article_edit')
    def edit(self):
        article = Article.get(self.article_id)
        # edit logic
        return {'article': article}
```

Properties berguna untuk computed values yang dipakai di multiple methods.

## Key Components:

1. **@view_defaults**:
   - Applies common configuration to all methods
   - Reduces repetition
   - Can set: route_name, renderer, permission, etc.

2. **__init__(self, request)**:
   - Called for every request
   - Initialize instance variables
   - Shared setup logic

3. **@view_config**:
   - Method-level configuration
   - Overrides or extends view_defaults
   - Specify HTTP methods, renderers, etc.


## Best Practices:

1. **Single Responsibility**:
   - One view class per resource/entity
   - Keep classes focused

2. **Initialization**:
   - Use __init__ for setup
   - Don't do heavy processing in __init__
   - Extract to helper methods if needed

3. **Method Naming**:
   - Use descriptive names
   - Follow REST conventions when applicable
   - get, create, update, delete, list

4. **Error Handling**:
```python
@view_config(request_method='GET', renderer='json')
def get(self):
    try:
        item = self.get_item()
        if not item:
            raise HTTPNotFound()
        return {'item': item}
    except ValueError as e:
        raise HTTPBadRequest(str(e))
```

5. **Inheritance**:
```python
class BaseAPIView:
    def __init__(self, request):
        self.request = request
        self.validate_auth()
    
    def validate_auth(self):
        if not self.request.authenticated_userid:
            raise HTTPUnauthorized()

class UserAPI(BaseAPIView):
    # Inherits authentication
    @view_config(request_method='GET', renderer='json')
    def get(self):
        return {'user': 'data'}
```

## Kesimpulan:
View classes provide superior organization for complex applications,
especially for RESTful APIs and resource-based routing. They promote
code reuse, maintainability, and cleaner architecture.