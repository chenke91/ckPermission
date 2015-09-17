(function() {
    "use strict";

    angular
        .module('myApp')
        .service('userAPIservice', userAPIservice);

    userAPIservice.$inject = ['$http', 'notify'];

    function userAPIservice($http, notify) {

        this.getMenu = function() {
            return $http.get('/admin/menus/');
        };
        this.getUsers = function(config) {
            return $http.get('/admin/users/', config);
        };
        this.getUser = function(id) {
            return $http.get('/admin/users/'+id+'/');
        };
        this.getCurrentUser = function() {
            return $http.get('/admin/current_user/');
        };
        this.getRoles = function() {
            return $http.get('/admin/roles/');
        };
        this.newUser = function (data) {
            $http.post('/admin/users/new/', data).then(function(resp) {
                notify.success('新增成功');
            })
        };
        this.updateUser = function(data, id) {
            $http.post('/admin/users/update/'+id+'/', data).then(function(resp) {
                notify.success('更新成功');
            })
        };
        this.deleteToggleUser = function(id) {
            return $http.get('/admin/users/delete_toggle/'+id+'/');
        }
    }
})()