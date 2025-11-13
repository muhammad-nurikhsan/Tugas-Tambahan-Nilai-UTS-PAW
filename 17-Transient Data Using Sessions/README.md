# Transient Data Using Sessions

## Identitas
Muhammad Nurikhsan (123140057)

## Session Setup
```python
from pyramid.config import Configurator
from pyramid.session import SignedCookieSessionFactory

# Create session factory
session_factory = SignedCookieSessionFactory('secret_key_here')

config = Configurator()
config.set_session_factory(session_factory)
```

## Using Sessions
```python
@view_config(route_name='login', request_method='POST')
def login(request):
    username = request.POST['username']
    password = request.POST['password']
    
    user = User.authenticate(username, password)
    if user:
        # Set session data
        request.session['user_id'] = user.id
        request.session['username'] = user.username
        return HTTPFound(location='/dashboard')
    
    return {'error': 'Invalid credentials'}

@view_config(route_name='dashboard')
def dashboard(request):
    # Get session data
    user_id = request.session.get('user_id')
    if not user_id:
        return HTTPFound(location='/login')
    
    username = request.session['username']
    return {'username': username}

@view_config(route_name='logout')
def logout(request):
    # Clear session
    request.session.invalidate()
    return HTTPFound(location='/')
```

## Flash Messages
```python
@view_config(route_name='save_article', request_method='POST')
def save_article(request):
    # Save logic
    article.save()
    
    # Set flash message
    request.session.flash('Article saved successfully!', 
                          queue='success')
    return HTTPFound(location='/articles')

@view_config(route_name='articles', renderer='articles.pt')
def list_articles(request):
    # Get and consume flash messages
    messages = request.session.pop_flash('success')
    return {
        'articles': Article.all(),
        'messages': messages
    }
```

Template:
```html
<div tal:repeat="msg messages" class="alert alert-success">
    ${msg}
</div>
```

## Session Configuration Options
```python
# Cookie-based (default)
session_factory = SignedCookieSessionFactory(
    secret='my_secret',
    cookie_name='myapp_session',
    max_age=3600,  # 1 hour
    httponly=True,
    secure=True  # HTTPS only
)

# Redis-based (for multiple servers)
from pyramid_redis_sessions import RedisSessionFactory
session_factory = RedisSessionFactory(
    'redis://localhost:6379',
    cookie_max_age=86400
)
```

## Analisis
Sessions essential untuk maintain user state across requests. HTTP stateless, sessions bikin app stateful.

Pyramid default pakai signed cookie sessions. Data stored di client-side cookie tapi signed dengan secret key, jadi nggak bisa di-tamper. Keuntungannya: no server storage needed, horizontally scalable.

Disadvantages signed cookies:
- Size limit (~4KB)
- Data sent dengan setiap request
- Client could delete cookies

Untuk production dengan multiple servers, better pakai Redis atau database sessions.

## Flash Messages Pattern
Flash messages brilliant untuk user feedback. Message stored di session, automatically consumed pas next request. Perfect untuk "saved successfully" notifications setelah redirect.

```python
# Set flash
request.session.flash('Success!', 'success')
request.session.flash('Warning!', 'warning')

# Get specific queue
success_msgs = request.session.pop_flash('success')
warning_msgs = request.session.pop_flash('warning')
```

Multiple queues berguna untuk different message types (success, error, info).

## Session Security
```python
session_factory = SignedCookieSessionFactory(
    secret='your-secret-key',  # Use strong random key
    httponly=True,  # Prevent XSS
    secure=True,  # HTTPS only
    samesite='Lax'  # CSRF protection
)
```

**Important**:
- Use cryptographically secure secret key
- Enable `httponly` to prevent JavaScript access
- Use `secure=True` in production (HTTPS)
- Never store sensitive data (passwords, credit cards) in sessions

## Session vs JWT
Sessions untuk traditional web apps dengan server-side state. JWT untuk stateless APIs. Choose based on use case:

- **Sessions**: Multi-page apps, need server-side state
- **JWT**: APIs, microservices, mobile apps

Session invalidation immediate (logout works instantly). JWT invalidation complex karena stateless.

## Security Considerations:
1. **Secret Key**: Use strong, random secret
2. **HTTPS**: Use secure flag for cookies
3. **Expiration**: Set appropriate timeout
4. **Validation**: Regenerate session on privilege change
5. **Sensitive Data**: Don't store passwords

## Best Practices:
1. Keep session data minimal
2. Validate session data
3. Use flash messages untuk user feedback
4. Implement session timeout
5. Clear sessions on logout

## Kesimpulan:
Sessions crucial untuk maintaining state dalam stateless HTTP protocol, enabling personalized user experiences.