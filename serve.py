import cherrypy
import os
import time
from watchdog.observers import Observer  
from lib.config import RemoteAudioPlayerConfig
from views.album import AlbumViewSet
from views.audio import AudioViewSet, AudioInfoViewSet
from lib.media.watcher import MediaDiskWatchThread, MediaFileManagerThread

# bootstrap remote media player config
rapbObj = RemoteAudioPlayerConfig(inipath = 'remoteaudioplayer.conf')
rapbObj.bootstrap()

# determine audio_path
audio_path = rapbObj.get(section='media', key='path')
MediaFileManagerThread(path=audio_path).start()

class Index:
    @cherrypy.expose
    def index(self):
        http_method = getattr(self, cherrypy.request.method)
        return (http_method)()

    def GET(self):
        return "Welcome to Remote Media Player"


if __name__ == '__main__':
    # start media watchdog to monitor filesystem change events
    print "Starting Media Watchdog: {}".format(audio_path)
    observer = Observer()
    observer.schedule(MediaDiskWatchThread(), path=audio_path, recursive=True)
    observer.start()
    
    # map cherrypy access urls
    mapper = cherrypy.dispatch.RoutesDispatcher()
    mapper.connect('index', '/', controller=Index())
    mapper.connect('status', '/status/', controller=AlbumViewSet(), action='status')
    mapper.connect('albums', '/albums/', controller=AlbumViewSet(), action='index')
    mapper.connect('songs', '/songs/', controller=AudioViewSet(), action='index')
    mapper.connect('audio-info', '/audios/{id}/', controller=AudioInfoViewSet(), action='index')
    mapper.connect('play', '/songs/{id}/play/', controller=AudioViewSet(), action='play')
    mapper.connect('pause', '/songs/pause/', controller=AudioViewSet(), action='pause')
    mapper.connect('stop', '/songs/stop/', controller=AudioViewSet(), action='stop')
    mapper.connect('volume', '/songs/volume/{idx}/', controller=AudioViewSet(), action='volume')
    mapper.connect('seek-forward', '/songs/seek/forward/', controller=AudioViewSet(), action='seekForward')
    mapper.connect('seek-backward', '/songs/seek/backward/', controller=AudioViewSet(), action='seekBackward')

    # set environment as production
    cherrypy.config.update({
        'global': {
            'environment' : 'production'
        }
    })

    application = cherrypy.tree.mount(None, config={
        "/": {
            "request.dispatch": mapper
        },
        '/player': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'player/')
        }
    })

    cherrypy.server.socket_host = rapbObj.get(section='daemon', key='bind_ip')
    cherrypy.server.socket_port = int(rapbObj.get(section='daemon', key='port'))
    cherrypy.server.thread_pool = int(rapbObj.get(section='daemon', key='threads'))
    cherrypy.quickstart(application)