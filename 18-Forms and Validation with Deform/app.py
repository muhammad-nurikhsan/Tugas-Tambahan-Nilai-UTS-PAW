from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound
import colander
import deform

class UserSchema(colander.MappingSchema):
    username = colander.SchemaNode(
        colander.String(),
        validator=colander.Length(min=3, max=20),
        description='Choose a username'
    )
    email = colander.SchemaNode(
        colander.String(),
        validator=colander.Email(),
        description='Your email address'
    )
    age = colander.SchemaNode(
        colander.Integer(),
        validator=colander.Range(min=18, max=120),
        description='Your age (18+)'
    )
    bio = colander.SchemaNode(
        colander.String(),
        widget=deform.widget.TextAreaWidget(rows=5),
        description='Tell us about yourself',
        missing=''
    )

def register(request):
    schema = UserSchema()
    form = deform.Form(schema, buttons=('submit',))
    
    if request.method == 'POST':
        try:
            appstruct = form.validate(request.POST.items())
            html = '<h1>Registration Successful!</h1>'
            html += f'<p>Username: {appstruct["username"]}</p>'
            html += f'<p>Email: {appstruct["email"]}</p>'
            html += f'<p>Age: {appstruct["age"]}</p>'
            html += '<a href="/register">Register another</a>'
            return Response(html)
        except deform.ValidationFailure as e:
            return Response(e.render())
    
    html = '<h1>User Registration</h1>' + form.render()
    return Response(html)

if __name__ == '__main__':
    with Configurator() as config:
        config.add_route('register', '/')
        config.add_view(register, route_name='register')
        app = config.make_wsgi_app()
    
    from waitress import serve
    print('Form demo: http://localhost:6543')
    serve(app, host='0.0.0.0', port=6543)