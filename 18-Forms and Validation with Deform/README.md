# Forms and Validation with Deform

## Identitas
Muhammad Nurikhsan (123140057)

## Setup Deform
```python
# Add to setup.py
requires = [
    'pyramid',
    'deform',
    'colander'
]
```

## Schema Definition
```python
import colander
import deform

class UserSchema(colander.MappingSchema):
    username = colander.SchemaNode(
        colander.String(),
        validator=colander.Length(min=3, max=20)
    )
    email = colander.SchemaNode(
        colander.String(),
        validator=colander.Email()
    )
    age = colander.SchemaNode(
        colander.Integer(),
        validator=colander.Range(min=18, max=120)
    )
    password = colander.SchemaNode(
        colander.String(),
        widget=deform.widget.PasswordWidget()
    )
```

## Form in View
```python
@view_config(route_name='register', renderer='register.pt')
def register(request):
    schema = UserSchema()
    form = deform.Form(schema, buttons=('submit',))
    
    if request.method == 'POST':
        try:
            # Validate and get data
            appstruct = form.validate(request.POST.items())
            
            # Create user
            user = User(
                username=appstruct['username'],
                email=appstruct['email'],
                age=appstruct['age']
            )
            user.set_password(appstruct['password'])
            user.save()
            
            request.session.flash('Registration successful!')
            return HTTPFound(location='/login')
            
        except deform.ValidationFailure as e:
            # Form akan render dengan errors
            return {'form': e.render()}
    
    return {'form': form.render()}
```

## Template Rendering
```html
<!-- register.pt -->
<div>
    <h1>Register</h1>
    ${form | structure}
</div>
```

`| structure` disable escaping supaya HTML form bisa render.

## Custom Validators
```python
def username_exists(node, value):
    if User.query.filter_by(username=value).first():
        raise colander.Invalid(node, 'Username already taken')

class UserSchema(colander.MappingSchema):
    username = colander.SchemaNode(
        colander.String(),
        validator=colander.All(
            colander.Length(min=3, max=20),
            username_exists
        )
    )
```

## Advanced Widgets
```python
class ArticleSchema(colander.MappingSchema):
    title = colander.SchemaNode(colander.String())
    
    content = colander.SchemaNode(
        colander.String(),
        widget=deform.widget.TextAreaWidget(rows=10)
    )
    
    category = colander.SchemaNode(
        colander.String(),
        widget=deform.widget.SelectWidget(
            values=[('tech', 'Technology'), 
                   ('sci', 'Science')]
        )
    )
    
    published = colander.SchemaNode(
        colander.Boolean(),
        widget=deform.widget.CheckboxWidget()
    )
    
    tags = colander.SchemaNode(
        colander.String(),
        widget=deform.widget.TagsWidget()
    )
```

## Analisis
Deform adalah form library yang integrate dengan Pyramid. Colander untuk schema validation, Deform untuk rendering.

Approach ini different dari manual form handling. Schema define struktur data DAN validation rules sekaligus. Form rendering automatic based on schema.

**Pros**:
- DRY - validation rules defined once
- Automatic HTML generation
- Built-in widgets untuk common inputs
- Server-side validation comprehensive

**Cons**:
- HTML output nggak customizable (kecuali override templates)
- Learning curve untuk Colander syntax
- Generated HTML kadang bloated

## Comparison dengan Alternatives

**WTForms** (Flask ecosystem):
```python
class UserForm(FlaskForm):
    username = StringField('Username', 
                          validators=[Length(min=3)])
```
More pythonic, better documented.

**Django Forms**:
```python
class UserForm(forms.Form):
    username = forms.CharField(max_length=20)
```
Tighter integration dengan models.

**Deform/Colander**:
More verbose tapi powerful. Schema bisa di-reuse untuk non-form validation (API payloads, etc).

## When to Use Deform
Good fit kalau:
- Need complex form validation
- Rapidly prototyping admin interfaces
- Want automatic form generation

Skip kalau:
- Need full control atas HTML
- Building modern SPA with frontend frameworks
- Simple forms dengan minimal validation

Modern approach sering pakai Pyramid untuk API only, forms handled di frontend dengan React/Vue. Deform lebih traditional server-rendered approach.

## CSRF Protection
```python
schema = UserSchema()
form = deform.Form(schema, buttons=('submit',))

# Deform automatically include CSRF token
# Template harus render full form dengan ${form | structure}
```

CSRF protection built-in kalau pakai Deform's form rendering.

## Best Practices:
1. **Separate Schemas**: Keep schemas in separate file
2. **Reusable Validators**: Create custom validators untuk common cases
3. **Client-side Validation**: Add JavaScript validation untuk UX
4. **Error Messages**: Provide clear, helpful error messages
5. **CSRF Protection**: Always include CSRF tokens
6. **File Upload Security**: Validate file types dan sizes

## Kelebihan Deform:
- Automatic form generation
- Built-in validation
- Multiple widget types
- Easy customization
- Schema reusability

## Kekurangan:
- Learning curve untuk Colander schemas
- Limited flexibility untuk complex layouts
- Styling requires custom CSS

## Kesimpulan:
Deform + Colander provide powerful form handling dengan minimal code, ensuring data validation dan security.