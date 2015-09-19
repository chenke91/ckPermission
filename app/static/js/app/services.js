(function() {
    'use strict';
    angular
        .module('myApp')
        .factory('notify', notify)
        .factory('errorResponse', errorResponse);

    notify.$inject = ['$rootScope'];
    errorResponse.$inject = ['$q', 'notify'];

    function notify($rootScope) {
        return {
            success: function(msg) {
                $rootScope.alerts.push({type: 'success', msg: msg});
            },
            error: function(msg) {
                $rootScope.alerts.push({type: 'danger', msg: msg});
            }
        }
    }

    function errorResponse($q, notify) {
        return {
            responseError: function(rejection) {
                if (rejection.data.message) {
                    notify.error(rejection.data.message);
                }
                return $q.reject(rejection);
            }
        }
    }
})();