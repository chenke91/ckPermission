'use strict';

myApp.config([ '$routeProvider', function($routeProvider) {

    $routeProvider.when('/', {
        templateUrl : '/static/templates/index.html'
    })
    .when('/admin/users', {
        templateUrl : '/static/templates/system/users.html',
        controller : 'UserController'
    })
    .when('/admin/permissions', {
        templateUrl: '/static/templates/system/permissions.html'
    })
    .when('/admin/modules', {
        templateUrl: '/static/templates/system/modules.html'
    })
    .otherwise({
        redirectTo : '/'
    });
 
} ]);