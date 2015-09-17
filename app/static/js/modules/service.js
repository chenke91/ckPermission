(function() {
    "use strict";

    angular
        .module('myApp')
        .service('moduleAPIservice', moduleAPIservice);

    moduleAPIservice.$inject = ['$http'];

    function moduleAPIservice($http) {

        this.getModules = function() {
            return $http.get('/admin/modules/');
        };
        this.loadModule = function() {
            return $http.get('/admin/modules/load/');
        };
        this.newModule = function(data) {
            return $http.post('/admin/modules/add/', data);
        };
        this.getMasters = function() {
            return $http.get('/admin/modules/masters/');
        };
    }
})()