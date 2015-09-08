"use strict";

myApp.service('roleAPIservice', function($http, $rootScope) {
    this.getRoles = function() {
        return $http.get('/admin/roles/');
    };
    this.updateRole = function(data) {
        return $http.post('/admin/roles/update/', data);
    };
    this.getModules = function() {
        return $http.get('/admin/roles/modules/');
    }
})