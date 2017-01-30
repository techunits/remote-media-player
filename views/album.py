import cherrypy

class AlbumViewSet():
    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def index(self):
        http_method = getattr(self, cherrypy.request.method)
        return (http_method)()

    def GET(self):
        return {
            'msg': 'HTTP GET method not supported: Albums'
        }

    def POST(self):
        dataset = cherrypy.request.json
        return dataset
