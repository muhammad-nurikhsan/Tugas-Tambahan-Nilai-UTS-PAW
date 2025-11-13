from pyramid.config import Configurator
from pyramid.view import view_config
from pyramid.response import Response

class ArticleViews:
    def __init__(self, request):
        self.request = request
        # Simulated data
        self.articles = [
            {'id': 1, 'title': 'First Article', 'author': 'Alice'},
            {'id': 2, 'title': 'Second Article', 'author': 'Bob'},
        ]
    
    @view_config(route_name='article_list')
    def list(self):
        html = '<h1>Articles</h1><ul>'
        for article in self.articles:
            html += f'<li><a href="/article/{article["id"]}">{article["title"]}</a></li>'
        html += '</ul>'
        return Response(html)
    
    @view_config(route_name='article_detail')
    def detail(self):
        article_id = int(self.request.matchdict['id'])
        article = next((a for a in self.articles if a['id'] == article_id), None)
        if article:
            html = f'<h1>{article["title"]}</h1><p>By: {article["author"]}</p>'
            return Response(html)
        return Response('Not found', status=404)

if __name__ == '__main__':
    with Configurator() as config:
        config.add_route('article_list', '/')
        config.add_route('article_detail', '/article/{id}')
        config.scan()
        app = config.make_wsgi_app()
    
    from waitress import serve
    print('Server on http://localhost:6543')
    serve(app, host='0.0.0.0', port=6543)