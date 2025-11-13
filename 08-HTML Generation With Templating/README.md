# HTML Generation With Templating

## Identitas
Muhammad Nurikhsan (123140057)

## Setup Chameleon
```python
config.include('pyramid_chameleon')
```

## View dengan Renderer
```python
@view_config(route_name='home', renderer='templates/home.pt')
def home_view(request):
    return {
        'project': 'MyApp',
        'users': ['Alice', 'Bob', 'Charlie']
    }
```

## Template File (home.pt)
```html
<!DOCTYPE html>
<html>
<head>
    <title>${project}</title>
</head>
<body>
    <h1>Welcome to ${project}</h1>
    <ul>
        <li tal:repeat="user users">${user}</li>
    </ul>
</body>
</html>
```

## TAL Syntax
```html
<!-- Conditional -->
<div tal:condition="user.is_admin">
    Admin Panel
</div>

<!-- Repeat -->
<tr tal:repeat="item items">
    <td>${item.name}</td>
</tr>

<!-- Attributes -->
<a tal:attributes="href item.url">${item.title}</a>
```

## Analisis
Chameleon pakai TAL (Template Attribute Language) yang embed logic sebagai HTML attributes. Approach ini beda dari Jinja2 yang pakai special syntax `{% %}`.

Keuntungan TAL:
- Template tetap valid HTML
- Bisa preview di browser tanpa render
- IDE bisa validate HTML-nya

Disadvantages:
- Syntax agak verbose
- Learning curve lebih tinggi daripada Jinja2
- Dokumentasi kurang populer

View function return dict, bukan render template langsung. Pyramid yang handle rendering based on `renderer` parameter di decorator. Ini clean separation antara logic dan presentation.


## Best Practices:
### 1. DRY Principle:
- Use template inheritance
- Create reusable macros
- Extract common blocks

### 2. Security:
- Auto-escaping is ON by default
- Use |safe filter carefully
- Validate user input before rendering

### 3. Performance:
- Templates are compiled and cached
- Avoid complex logic in templates
- Use view functions for data processing

## Template Inheritance
```html
<!-- base.pt -->
<html metal:define-macro="layout">
    <div metal:define-slot="content">
        Default content
    </div>
</html>

<!-- child.pt -->
<html metal:use-macro="load: base.pt">
    <div metal:fill-slot="content">
        Child content
    </div>
</html>
```

METAL macros untuk inheritance lumayan powerful tapi syntax-nya alien kalau biasa pakai Jinja2.

## Alternatif Template Engine
Pyramid support multiple engines: Jinja2, Mako, Chameleon. Tinggal install dan configure aja. Jinja2 probably more familiar buat most developers.

## Kesimpulan
Templating adalah essential skill untuk web development. Jinja2 provides powerful/ features while maintaining simplicity and security.