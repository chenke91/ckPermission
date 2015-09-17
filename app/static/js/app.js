(function() {
    'use strict';

    angular.module('myApp',
        ['ui.bootstrap',
        'angularjs-dropdown-multiselect',
        'ngMessages',
        'angular-loading-bar',
        'ui.router']);


    var csrftoken = $('meta[name=csrf-token]').attr('content');

    angular
        .module('myApp')
        .config(httpSetting)
        .run(runApp);

    httpSetting.$inject = ['$httpProvider'];
    runApp.$inject = ['$rootScope'];

    function httpSetting($httpProvider) {
        $httpProvider.defaults.headers.common['Accept'] = 'application/json';
        $httpProvider.defaults.headers.post['X-CSRFToken'] = csrftoken;
        $httpProvider.interceptors.push('errorResponse');
    }

    function runApp($rootScope) {
        $rootScope.alerts = [];
    }

})()