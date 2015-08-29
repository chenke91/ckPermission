"use strict";

myApp.service('myAPIservice', function($http) {

    this.getMenu = function() {
        return $http.get('/admin/menus/');
    };
    this.getUser = function(config) {
        return $http.get('/admin/users/', config);
    };
    this.getRoles = function() {
        return $http.get('/admin/roles/');
    }
})