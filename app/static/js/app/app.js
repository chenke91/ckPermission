(function() {
    'use strict';

    angular.module('myApp',
        ['ui.bootstrap',
        'angularjs-dropdown-multiselect',
        'ngMessages',
        'angular-loading-bar',
        'ui.router',
        'cgNotify']);


    var csrftoken = $('meta[name=csrf-token]').attr('content');

    angular
        .module('myApp')
        .config(httpSetting)
        .run(runApp);

    httpSetting.$inject = ['$httpProvider'];
    runApp.$inject = ['$rootScope', 'mynotify'];

    function httpSetting($httpProvider) {
        $httpProvider.defaults.headers.common['Accept'] = 'application/json';
        $httpProvider.defaults.headers.post['X-CSRFToken'] = csrftoken;
        $httpProvider.interceptors.push('errorResponse');
    }

    function runApp($rootScope, mynotify) {
        $rootScope.$on('httpErrorEvent', function(event, msg) {
            mynotify.error(msg);
        })
    }

})();