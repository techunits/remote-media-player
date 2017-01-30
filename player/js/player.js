var playerApp = angular.module('playerApp', []);

playerApp.controller('PlayerCtrl', function($scope, $http) {
    $scope.currentAudioId = 0;
    $scope.player = {
        'status': false
    };
    

    $scope.getAudioMetaInfo = function(id) {
        var endpoint = '/audios/' + id + '/';
        $http({
            method: 'GET',
            url: endpoint
        })
        .then(function successCallback(response) {
            $scope.audio = {
                'title': response.data.audio.title,
                'artist': response.data.audio.artist,
                'album': response.data.audio.album,
                'duration': response.data.audio.seconds,
            };
        }, function() {
            alert('Sorry!!! Can\'t this load audio info');
        });
    };
    //  load first media info
    $scope.getAudioMetaInfo($scope.currentAudioId);

    $scope.play = function(id) {
        $scope.currentAudioId = id;

        //  load audio info
        $scope.getAudioMetaInfo(id);

        //  start playing audio
        var endpoint = '/songs/' + $scope.currentAudioId + '/play/';
        $http({
            method: 'GET',
            url: endpoint
        })
        .then(function successCallback() {
            $scope.player.status = 'PLAYING';
        }, function() {
            alert('Sorry!!! Can\'t this play audio');
        });
    };

    $scope.pause = function() {
        var endpoint = '/songs/pause/';
        $http({
            method: 'GET',
            url: endpoint
        })
        .then(function successCallback() {
            $scope.player.status = 'PAUSED';
        }, function() {
            alert('Sorry!!! Can\'t this pause audio');
        });
    };

    $scope.stop = function() {
        var endpoint = '/songs/stop/';
        $http({
            method: 'GET',
            url: endpoint
        })
        .then(function successCallback() {
            $scope.player.status = 'STOPPED';
        }, function() {
            alert('Sorry!!! Can\'t this stop audio');
        });
    };

    $scope.seekForward = function() {
        var endpoint = '/songs/seek/forward/';
        $http({
            method: 'GET',
            url: endpoint
        })
        .then(function successCallback() {
            $scope.player.status = 'PLAYING';
        }, function() {
            alert('Sorry!!! Can\'t this seek audio');
        });
    };

    $scope.seekBackward = function() {
        var endpoint = '/songs/seek/backward/';
        $http({
            method: 'GET',
            url: endpoint
        })
        .then(function successCallback() {
            $scope.player.status = 'PLAYING';
        }, function() {
            alert('Sorry!!! Can\'t this seek audio');
        });
    };

    $scope.next = function() {
        var nextAudioId = $scope.currentAudioId + 1;
        $scope.play(nextAudioId);
    };

    $scope.prev = function() {
        var prevAudioId = $scope.currentAudioId - 1;
        prevAudioId = (prevAudioId < 0)?0:prevAudioId;
        $scope.play(prevAudioId);
    };

    $scope.loadPlaylist = function() {
        var endpoint = '/songs/';
        $http({
            method: 'GET',
            url: endpoint
        })
        .then(function successCallback(response) {
            console.log(response.data.songs);
            $scope.playlist = response.data.audios;
        }, function() {
            alert('Sorry!!! Can\'t load audio playlist');
        });
    };
});