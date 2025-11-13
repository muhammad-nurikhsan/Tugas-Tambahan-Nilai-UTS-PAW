# Collecting Application Info With Logging

## Identitas
Muhammad Nurikhsan (123140057)

## Basic Logging Setup
```python
import logging

log = logging.getLogger(__name__)

@view_config(route_name='home')
def home_view(request):
    log.info('Home page accessed')
    return Response('Home')
```

## Configuration File (development.ini)
```ini
[app:main]
use = egg:myapp

[loggers]
keys = root, myapp

[logger_root]
level = INFO
handlers = console

[logger_myapp]
level = DEBUG
handlers = console
qualname = myapp

[handlers]
keys = console

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatters]
keys = generic

[formatter_generic]
format = %(asctime)s %(levelname)-5.5s [%(name)s][%(threadName)s] %(message)s
```

## Log Levels
```python
log.debug('Detailed info for debugging')
log.info('General informational messages')
log.warning('Warning messages')
log.error('Error messages')
log.critical('Critical errors')
```

## Practical Usage
```python
import logging
log = logging.getLogger(__name__)

@view_config(route_name='user_login', request_method='POST')
def login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    
    log.info(f'Login attempt for user: {username}')
    
    user = User.authenticate(username, password)
    if user:
        log.info(f'User {username} logged in successfully')
        return HTTPFound(location='/dashboard')
    else:
        log.warning(f'Failed login attempt for user: {username}')
        return {'error': 'Invalid credentials'}
```

## Error Logging
```python
@view_config(route_name='api_data', renderer='json')
def get_data(request):
    try:
        data = external_api_call()
        return {'data': data}
    except ConnectionError as e:
        log.error(f'API connection failed: {e}', exc_info=True)
        return {'error': 'Service unavailable'}
    except Exception as e:
        log.critical(f'Unexpected error: {e}', exc_info=True)
        raise
```

`exc_info=True` include full stack trace dalam log.

## Analisis
Logging essential untuk production debugging. Tanpa proper logging, debug production issues basically impossible.

Python's logging module powerful tapi konfigurasinya verbose. Pyramid pakai `.ini` file untuk configure logging, which is different dari Django/Flask yang sering hardcode dalam code.

## Log Levels Best Practice
- **DEBUG**: Development only, detailed info
- **INFO**: Production events (user login, data changes)
- **WARNING**: Unusual tapi nggak critical (deprecated API usage)
- **ERROR**: Handled errors (API failures, validation errors)
- **CRITICAL**: Unhandled errors yang butuh immediate attention

Jangan log sensitive data (passwords, tokens, personal info). GDPR compliance issue.

## Structured Logging
```python
log.info('User action', extra={
    'user_id': user.id,
    'action': 'purchase',
    'amount': 100.0
})
```

Extra fields bisa di-parse oleh log aggregators (ELK stack, Splunk).

## File Logging (Production)
```ini
[handler_file]
class = FileHandler
args = ('/var/log/myapp/app.log',)
level = INFO
formatter = generic

[logger_myapp]
handlers = file, console
```

Production biasanya log ke file atau external service (Sentry, CloudWatch).

## Performance Consideration
Logging ada overhead. Debug level logging di production could impact performance. Always use appropriate log levels dan consider conditional logging:

```python
if log.isEnabledFor(logging.DEBUG):
    expensive_debug_info = compute_expensive_data()
    log.debug(f'Debug info: {expensive_debug_info}')
```

## Integration dengan Monitoring
Production apps should integrate dengan monitoring services:
- **Sentry**: Error tracking dengan stack traces
- **Datadog/New Relic**: Performance monitoring
- **ELK Stack**: Log aggregation dan search

Pyramid's logging integrate well dengan these services via handlers.

## Log Levels:
1. **DEBUG**: Detailed information untuk debugging
2. **INFO**: Confirmation bahwa things work as expected
3. **WARNING**: Something unexpected happened
4. **ERROR**: Serious problem occurred
5. **CRITICAL**: Very serious error

## Best Practices:
1. **Appropriate Levels**: Use correct log level
2. **Structured Logging**: Include context information
3. **Avoid Sensitive Data**: Don't log passwords, tokens
4. **Performance**: Don't log in tight loops
5. **Rotation**: Configure log rotation

## Production Considerations:
```ini
[logger_myapp]
level = WARNING
handlers = file, email

[handler_email]
class = handlers.SMTPHandler
args = (('localhost', 25), 'from@example.com', ['admin@example.com'], 'App Error')
level = ERROR
```

## Kesimpulan:
Proper logging essential untuk maintaining production applications dan debugging issues.