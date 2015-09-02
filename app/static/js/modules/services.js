"use strict";

myApp.service('moduleAPIservice', function($http, $rootScope) {

    this.getModules = function() {
        return $http.get('/admin/modules/');
    };
})