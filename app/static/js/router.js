(function() {
    'use strict';

    angular
        .module('myApp')
        .config(router);

    router.$inject = ['$stateProvider'];

    function router($stateProvider) {
        $stateProvider
            .state('index', {
                url: '/',
                templateUrl: '/static/templates/index.html'
            })
            .state('profile', {
                url: '/profile',
                templateUrl: '/static/templates/system/profile.html',
                controller: 'profileController'
            })
            .state('/admin/users', {
                url: '/admin/users',
                templateUrl : '/static/templates/system/users.html',
                controller : 'UserController'
            })
            .state('/admin/new_user', {
                url: '/admin/new_user',
                templateUrl : '/static/templates/system/user_add.html',
                controller : 'NewUserController'
            })
            .state('/admin/edit_user', {
                url: '/admin/edit_user/:id',
                templateUrl : '/static/templates/system/user_edit.html',
                controller : 'EditUserController'
            })
            .state('/admin/roles', {
                url: '/admin/roles',
                templateUrl: '/static/templates/system/roles.html',
                controller: 'RoleController'
            })
            .state('/admin/modules', {
                url: '/admin/modules',
                templateUrl: '/static/templates/system/modules.html',
                controller: 'ModuleController'
            })
            .state('/admin/icons', {
                url: '/admin/icons',
                templateUrl: '/static/templates/system/icons.html'
            })
    }
})();