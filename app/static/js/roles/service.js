(function() {
    "use strict";

    angular
        .module('myApp')
        .service('roleAPIservice', roleAPIservice);

    roleAPIservice.$inject = ['$http'];

    function roleAPIservice($http) {
        this.getRoles = function() {
            return $http.get('/admin/roles/');
        };
        this.updateRole = function(data) {
            return $http.post('/admin/roles/update/', data);
        };
        this.getModules = function() {
            return $http.get('/admin/roles/modules/');
        }
    }
})();