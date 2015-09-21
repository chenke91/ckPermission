(function() {
    'use strict';
    angular
        .module('myApp')
        .factory('mynotify', mynotify)
        .factory('errorResponse', errorResponse);

    mynotify.$inject = ['notify'];
    errorResponse.$inject = ['$q', '$rootScope'];

    function mynotify(notify) {
        var config = {
            position: 'right',
            duration: 1500
        }
        return {
            success: function(msg) {
                config.message = msg;
                config.classes = 'alert-success';
                notify(config);
            },
            error: function(msg) {
                config.message = msg;
                config.classes = 'alert-danger';
                notify(config);
            }
        }
    }

    function errorResponse($q, $rootScope) {
        return {
            responseError: function(rejection) {
                if (rejection.data.message) {
                    $rootScope.$broadcast('httpErrorEvent', rejection.data.message);
                }
                return $q.reject(rejection);
            }
        }
    }
})();