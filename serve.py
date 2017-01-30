import cherrypy
import os

from lib.mplayer import MPlayer
from views.album import AlbumViewSet
from views.audio import AudioViewSet, AudioInfoViewSet
from lib.media.audio import refreshAudioFiles

audio_path = '/home/skall/Projects/RnD/mediaserv/resources/'
#audio_path = '/media/wd-external-1tb/Backup/Media/Entertainment/audio/'

# load mplayer functions
global mpObj
MPlayer.populate()
mpObj = MPlayer()

class Index:
    @cherrypy.expose
    def index(self):
        http_method = getattr(self, cherrypy.request.method)
        return (http_method)()

    def GET(self):
        return "Welcome to Remote Media Player"


if __name__ == '__main__':
    # connect to  database
    #conn = sqlite3.connect('pyaudioplayer.db.sqlite3')
    #cursor = conn.cursor()
    audioFiles = refreshAudioFiles(path=audio_path)
    
    mapper = cherrypy.dispatch.RoutesDispatcher()
    mapper.connect('index', '/', controller=Index())
    mapper.connect('albums', '/albums/', controller=AlbumViewSet(), action='index')
    mapper.connect('songs', '/songs/', controller=AudioViewSet(), action='index')
    mapper.connect('audio-info', '/audios/{id}/', controller=AudioInfoViewSet(), action='index')
    mapper.connect('play', '/songs/{id}/play/', controller=AudioViewSet(), action='play')
    mapper.connect('pause', '/songs/pause/', controller=AudioViewSet(), action='pause')
    mapper.connect('stop', '/songs/stop/', controller=AudioViewSet(), action='stop')
    mapper.connect('seek-forward', '/songs/seek/forward/', controller=AudioViewSet(), action='seekForward')
    mapper.connect('seek-backward', '/songs/seek/backward/', controller=AudioViewSet(), action='seekBackward')


    application = cherrypy.tree.mount(None, config={
        "/": {
            "request.dispatch": mapper
        },
        '/player': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'player/')
        }
    })

    cherrypy.server.socket_host = "0.0.0.0"
    cherrypy.server.socket_port = 8989
    cherrypy.server.thread_pool = 10
    cherrypy.quickstart(application)


