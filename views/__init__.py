def getAudioFiles(path=None, databaseFlag=False):
    if databaseFlag is False:
        import fnmatch
        audioFileList = []
        for root, dirnames, filenames in os.walk(path):
            for filename in fnmatch.filter(filenames, '*.mp3'):
                audioFileList.append(os.path.join(root, filename))
            for filename in fnmatch.filter(filenames, '*.wav'):
                audioFileList.append(os.path.join(root, filename))
        return audioFileList
    else:
        audiolistdb = 'pyaudioplayer.db.json'
        jsonObj = []

        # read old database
        if os.path.isfile(audiolistdb) is True:
            with open(audiolistdb, 'r') as infile:
                filedata = infile.read()
                if len(filedata) > 0:
                    jsonObj = json.loads(filedata)
        return jsonObj



def refreshAudioFiles(path):
    # cleanup old data
    audiolistdb = 'pyaudioplayer.db.json'
    os.system('rm -f {}'.format(audiolistdb))

    # get recent audio filelist
    audioFiles = getAudioFiles(path)
    for audioFile in audioFiles:
        updateMediaToDatabase(audioFile)


def updateMediaToDatabase(filepath):
    #sql = "SELECT * FROM songs WHERE path = '%s'" % filepath
    #c.execute(sql)
    #print c.fetchone()
    jsonObj = []
    audiolistdb = 'pyaudioplayer.db.json'

    # read old database
    if os.path.isfile(audiolistdb) is True:
        with open(audiolistdb, 'r') as infile:
            filedata = infile.read()
            if len(filedata) > 0:
                jsonObj = json.loads(filedata)

    # get audio metadata
    audioMetaObj = eyed3.load(filepath)

    # populate the new data
    try:
        jsonObj.append({
            'title': str(audioMetaObj.tag.title),
            'path': filepath,
            'artist': str(audioMetaObj.tag.artist),
            'album': str(audioMetaObj.tag.album),
            'seconds': int(audioMetaObj.info.time_secs)
        })
    except Exception as e:
        print (e)

    # write back to database
    with open(audiolistdb, 'w') as outfile:
        outfile.write(json.dumps(jsonObj))
