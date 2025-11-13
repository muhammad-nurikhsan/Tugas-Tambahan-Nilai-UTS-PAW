# More With View Classes

## Identitas
Muhammad Nurikhsan (123140057)

## Base View Class Pattern
```python
class BaseView:
    def __init__(self, request):
        self.request = request
        self.user = self.get_user()
    
    def get_user(self):
        user_id = self.request.session.get('user_id')
        if user_id:
            return User.get(user_id)
        return None
    
    def require_auth(self):
        if not self.user:
            raise HTTPFound(location='/login')

class ArticleViews(BaseView):
    @view_config(route_name='article_list', renderer='json')
    def list(self):
        articles = Article.all()
        return [a.to_dict() for a in articles]
    
    @view_config(route_name='article_create', 
                 renderer='json', 
                 request_method='POST')
    def create(self):
        self.require_auth()
        data = self.request.json_body
        article = Article.create(**data)
        return {'success': True, 'id': article.id}
```

## Mixin Pattern
```python
class JSONMixin:
    def json_response(self, data, status=200):
        self.request.response.status = status
        return data
    
    def error_response(self, message, status=400):
        return self.json_response(
            {'error': message}, 
            status=status
        )

class ArticleAPI(JSONMixin, BaseView):
    @view_config(route_name='api_article', renderer='json')
    def detail(self):
        article_id = self.request.matchdict['id']
        article = Article.get(article_id)
        
        if not article:
            return self.error_response('Not found', 404)
        
        return self.json_response(article.to_dict())
```

## Property-Based Logic
```python
class ArticleViews(BaseView):
    @property
    def article(self):
        if not hasattr(self, '_article'):
            article_id = self.request.matchdict['id']
            self._article = Article.get(article_id)
        return self._article
    
    @view_config(route_name='article_view')
    def view(self):
        return {'article': self.article}
    
    @view_config(route_name='article_edit')
    def edit(self):
        self.require_auth()
        if self.article.author_id != self.user.id:
            raise HTTPForbidden()
        return {'article': self.article}
```

Lazy loading dengan property + memoization. Query database cuma sekali meskipun property diakses multiple times.

## Analisis
View classes shine kalau punya complex application dengan banyak shared logic. Inheritance dan mixins bikin code reusable tanpa copy-paste.

Pattern Base + Mixin common di codebases besar:
- **BaseView**: Common logic untuk semua views (auth, database, etc)
- **Mixins**: Specific functionality (JSON handling, pagination, etc)
- **Concrete Views**: Actual endpoints

## Decorator Pattern dalam Class
```python
def require_admin(method):
    def wrapper(self):
        if not self.user or not self.user.is_admin:
            raise HTTPForbidden()
        return method(self)
    return wrapper

class AdminViews(BaseView):
    @view_config(route_name='admin_dashboard')
    @require_admin
    def dashboard(self):
        return {'users': User.all()}
```

Custom decorators bisa combine dengan view_config untuk add middleware-like functionality.

## Comparison: Functions vs Classes

**Function-based** (simple apps):
```python
@view_config(route_name='hello')
def hello(request):
    return Response('Hello')
```

**Class-based** (complex apps):
```python
class Views:
    def __init__(self, request):
        self.request = request
    
    @view_config(route_name='hello')
    def hello(self):
        return Response('Hello')
```

Function-based lebih simple dan direct. Class-based better untuk organization dan code reuse. Choose based on complexity needs.

## Testing Class Views
```python
class TestArticleViews(unittest.TestCase):
    def test_list(self):
        request = DummyRequest()
        view = ArticleViews(request)
        result = view.list()
        self.assertIsInstance(result, list)
```

Testing class views straightforward - instantiate dengan mock request, call methods directly. Easier to test shared logic separately.

## Best Practices:
1. Use inheritance untuk shared functionality
2. Keep class focused (Single Responsibility)
3. Use mixins untuk cross-cutting concerns
4. Document class hierarchy
5. Consider testability

## Kesimpulan:
Advanced view class patterns enable sophisticated code organization untuk large applications.