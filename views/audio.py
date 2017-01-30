import cherrypy
from lib.media.audio import getAudioFiles
from settings import MP_OBJ

class AudioViewSet():
    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def index(self):
        http_method = getattr(self, cherrypy.request.method)
        return (http_method)()

    def GET(self):
        audioFileList = getAudioFiles(databaseFlag=True)
        return {
            'audios': audioFileList,
        }

    def play(self, id):
        audioFileList = getAudioFiles(databaseFlag=True)
        audioData = audioFileList[int(id)]
        MP_OBJ.loadfile(str(audioData['path']))

    def pause(self):
        MP_OBJ.pause()

    def stop(self):
        MP_OBJ.stop()

    def seekForward(self):
        MP_OBJ.seek(+5)

    def seekBackward(self):
        MP_OBJ.seek(-5)


class AudioInfoViewSet():
    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def index(self, id):
        http_method = getattr(self, cherrypy.request.method)
        return (http_method)(id)

    def GET(self, id):
        audioFileList = getAudioFiles(databaseFlag=True)
        return {
            'audio': audioFileList[int(id)]
        }