'use strict';

myApp.config([ '$routeProvider', function($routeProvider) {

    $routeProvider.when('/', {
        templateUrl : '/static/templates/index.html'
    })
    .when('/admin/users', {
        templateUrl : '/static/templates/system/users.html',
        controller : 'UserController'
    })
    .when('/admin/new_user', {
        templateUrl : '/static/templates/system/user_edit.html',
        controller : 'NewUserController'
    })
    .when('/admin/edit_user/:id', {
        templateUrl : '/static/templates/system/user_edit.html',
        controller : 'EditUserController'
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