import cherrypy
import os
from lib.media.audio import getAudioFiles 
from lib.media.database import MediaDatabaseHanler
from lib.media.status import MediaStatusHanler
from settings import MP_OBJ

class AudioViewSet():
    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def index(self):
        http_method = getattr(self, cherrypy.request.method)
        return (http_method)()

    def GET(self):
        audioFileList = getAudioFiles()
        return {
            'audios': audioFileList,
        }

    def play(self, id):
        # fetch audio info based on "id"
        dbObj = MediaDatabaseHanler()
        audioData = dbObj.getMediaInfo(id)

        # load status object
        statusObj = MediaStatusHanler()
        statusObj.updateStatus(key='status', value='PLAYING')
        statusObj.updateStatus(key='path', value=str(audioData['path']))
        statusObj.updateStatus(key='id', value=str(audioData['id']))

        # use mplayer master volume settings
        MP_OBJ.use_master()

        # load file for playing
        MP_OBJ.loadfile(str(audioData['path']))
    

    def pause(self):
        # load status object
        statusObj = MediaStatusHanler()
        statusObj.updateStatus(key='status', value='PAUSED')

        # pause MPlayer
        MP_OBJ.pause()

    def stop(self):
        # load status object
        statusObj = MediaStatusHanler()
        statusObj.updateStatus(key='status', value='STOPPED')

        # STOP MPlayer
        MP_OBJ.stop()

    def seekForward(self):
        MP_OBJ.seek(+5)

    def seekBackward(self):
        MP_OBJ.seek(-5)

    def volume(self, idx):
        # load status object
        statusObj = MediaStatusHanler()
        statusObj.updateStatus(key='volume', value=int(idx))

        os.system("amixer set 'Master' {}".format(idx))


class AudioInfoViewSet():
    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def index(self, id):
        http_method = getattr(self, cherrypy.request.method)
        return (http_method)(id)

    def GET(self, id):
        dbObj = MediaDatabaseHanler()
        audioData = dbObj.getMediaInfo(id)
        return {
            'audio': audioData
        }

class AudioStatusViewSet():
    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def index(self, id):
        http_method = getattr(self, cherrypy.request.method)
        return (http_method)(id)

    def GET(self, id):
        # load status object
        statusObj = MediaStatusHanler()
        statusData = statusObj.getStatusData()

        statusFinalData = {}
        if 'volume' in statusData:
            statusFinalData['volume'] = statusData['volume']
        else:
            statusFinalData['volume'] = 40
        
        if 'id' in statusData:
            statusFinalData['id'] = statusData['id']
        else:
            statusFinalData['id'] = 1

        if 'status' in statusData:
            statusFinalData['status'] = statusData['status']
        else:
            statusFinalData['id'] = 'STOPPED'
        