'use strict';

myApp.controller('ModuleController', function($scope, $rootScope, moduleAPIservice){
    $rootScope.trace = [
        {url: '#/admin/modules',
         name: '模块管理'}
    ];
    $scope.module_list = [];
    $scope.masters = [];
    $scope.getModules = function() {
        moduleAPIservice.getModules().then(function(resp) {
            $scope.module_list = resp.data.items;
        }, function(resp) {
            $rootScope.addAlert('danger', resp.data.message);
        })
    };
    $scope.loadModule = function() {
        moduleAPIservice.loadModule().then(function(resp) {
            $rootScope.addAlert('success', '载入成功');
            $scope.getModules();
        }, function(resp) {
            $rootScope.addAlert('danger', resp.data.message);
        })
    };
    $scope.current_module = {pid: "0"};
    $scope.newModule = function() {
        moduleAPIservice.newModule($scope.current_module).then(function(resp) {
            $rootScope.addAlert('success', resp.data.msg);
            $scope.getModules();
        }, function(resp) {
            $rootScope.addAlert('danger', resp.data.message);
        })
    };
    $scope.getMasters = function() {
        moduleAPIservice.getMasters().then(function(resp) {
            $scope.masters = resp.data.items;
        }, function(resp) {
            $rootScope.addAlert('danger', resp.data.message);
        })
    };
    $scope.setModule = function(data) {
        $scope.current_module = data;
    };
    $scope.getModules();
    $scope.getMasters();
});