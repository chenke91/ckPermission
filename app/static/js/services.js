"use strict";

myApp.service('myAPIservice', function($http, $rootScope) {

    this.getMenu = function() {
        return $http.get('/admin/menus/');
    };
    this.getUsers = function(config) {
        return $http.get('/admin/users/', config);
    };
    this.getUser = function(id) {
        return $http.get('/admin/users/'+id+'/');
    }
    this.getRoles = function() {
        return $http.get('/admin/roles/');
    };
    // this.newUser = function(data) {
    //     return $http.post('/admin/users/new/', data);
    // };
    this.newUser = function (data) {
        $http.post('/admin/users/new/', data).then(function(resp) {
            if (resp.data.status == 0) {
                $rootScope.addAlert('success', '新增成功');
            } else {
                $rootScope.addAlert('danger', resp.data.msg);
            }
        }, function(resp) {
            if (resp.message) {
                $rootScope.addAlert('danger', resp.data.message);
            } else {
                $rootScope.addAlert('danger', '请求异常');
            }
            
        })
    };
})