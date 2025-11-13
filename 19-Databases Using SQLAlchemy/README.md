# Databases Using SQLAlchemy

## Identitas
Muhammad Nurikhsan (123140057)

## Setup SQLAlchemy
```python
# setup.py
requires = [
    'pyramid',
    'SQLAlchemy',
    'pyramid_tm',  # Transaction manager
    'zope.sqlalchemy'
]
```

## Database Configuration
```ini
# development.ini
[app:main]
sqlalchemy.url = sqlite:///%(here)s/myapp.sqlite

# Production example
# sqlalchemy.url = postgresql://user:pass@localhost/dbname
```

## Models Definition
```python
from sqlalchemy import (
    Column, Integer, String, Text, DateTime, ForeignKey
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    articles = relationship('Article', back_populates='author')

class Article(Base):
    __tablename__ = 'articles'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    content = Column(Text)
    author_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    author = relationship('User', back_populates='articles')
```

## Database Initialization
```python
# __init__.py
from sqlalchemy import engine_from_config
from sqlalchemy.orm import sessionmaker
from .models import Base

def main(global_config, **settings):
    engine = engine_from_config(settings, 'sqlalchemy.')
    Base.metadata.create_all(engine)
    
    session_factory = sessionmaker(bind=engine)
    config = Configurator(settings=settings)
    config.registry['dbsession'] = session_factory
    
    return config.make_wsgi_app()
```

## Using Database in Views
```python
@view_config(route_name='articles', renderer='json')
def list_articles(request):
    dbsession = request.registry['dbsession']()
    
    articles = dbsession.query(Article)\
        .order_by(Article.created_at.desc())\
        .all()
    
    return [
        {
            'id': a.id,
            'title': a.title,
            'author': a.author.username
        }
        for a in articles
    ]

@view_config(route_name='create_article', 
             request_method='POST', 
             renderer='json')
def create_article(request):
    dbsession = request.registry['dbsession']()
    
    data = request.json_body
    article = Article(
        title=data['title'],
        content=data['content'],
        author_id=request.session['user_id']
    )
    
    dbsession.add(article)
    dbsession.commit()
    
    return {'success': True, 'id': article.id}
```

## Transaction Management
```python
from pyramid_tm import TransactionManager

config.include('pyramid_tm')

# Dengan transaction manager, auto commit/rollback
@view_config(route_name='update_article')
def update_article(request):
    dbsession = request.dbsession
    article = dbsession.query(Article).get(id)
    
    article.title = request.json_body['title']
    # Auto commit kalau no error
    # Auto rollback kalau ada exception
    
    return {'success': True}
```

## Query Examples
```python
# Basic queries
users = dbsession.query(User).all()
user = dbsession.query(User).filter_by(username='john').first()
user = dbsession.query(User).get(1)  # By primary key

# Filtering
articles = dbsession.query(Article)\
    .filter(Article.created_at > datetime.date(2024, 1, 1))\
    .filter(Article.author_id == user_id)\
    .all()

# Joins
results = dbsession.query(Article, User)\
    .join(User)\
    .filter(User.username == 'john')\
    .all()

# Count
count = dbsession.query(Article).count()

# Update
dbsession.query(User)\
    .filter_by(id=user_id)\
    .update({'email': 'new@email.com'})

# Delete
dbsession.query(Article).filter_by(id=article_id).delete()
```

## Analisis
SQLAlchemy adalah ORM paling powerful di Python. Pyramid integrate well dengan SQLAlchemy tapi nggak opinionated - you setup sendiri.

Comparison dengan Django ORM:
- **Django**: Tightly coupled, simpler API, auto migrations
- **SQLAlchemy**: More flexible, expressive query API, manual migrations

SQLAlchemy Core vs ORM:
- **Core**: SQL-like queries, no models
- **ORM**: Object-oriented, relationship mapping

Most apps pakai ORM karena cleaner dan easier maintenance.

## Relationship Patterns
```python
# One-to-Many
class User(Base):
    articles = relationship('Article', back_populates='author')

class Article(Base):
    author = relationship('User', back_populates='articles')

# Many-to-Many
article_tags = Table('article_tags', Base.metadata,
    Column('article_id', Integer, ForeignKey('articles.id')),
    Column('tag_id', Integer, ForeignKey('tags.id'))
)

class Article(Base):
    tags = relationship('Tag', secondary=article_tags)
```

## Migrations dengan Alembic
```bash
pip install alembic
alembic init alembic
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

SQLAlchemy nggak punya built-in migrations. Need Alembic. Django advantage di sini dengan `makemigrations`.

## Performance Tips
```python
# Eager loading untuk avoid N+1 queries
from sqlalchemy.orm import joinedload

articles = dbsession.query(Article)\
    .options(joinedload(Article.author))\
    .all()

# Lazy vs Eager loading
class Article(Base):
    # Default lazy
    author = relationship('User', lazy='select')
    
    # Eager
    author = relationship('User', lazy='joined')
```

N+1 problem common pitfall. Always use `joinedload` atau `subqueryload` kalau access relationships dalam loop.

## Connection Pooling
SQLAlchemy automatically handle connection pooling. Configuration di `.ini`:
```ini
sqlalchemy.pool_size = 5
sqlalchemy.max_overflow = 10
```

## Kesimpulan:
SQLAlchemy provides powerful ORM capabilities untuk Pyramid applications, enabling efficient database operations dengan clean, Pythonic syntax. Proper understanding of queries, relationships, dan transactions essential untuk building scalable applications.