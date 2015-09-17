(function() {
    'use strict';

    angular
        .module('myApp')
        .controller('ModuleController', moduleController);

    moduleController.$inject = ['$scope', '$rootScope', 'moduleAPIservice', 'notify'];

    function moduleController($scope, $rootScope, moduleAPIservice, notify){
        $rootScope.trace = [
            {url: '#/admin/modules',
             name: '模块管理'}
        ];
        $scope.module_list = [];
        $scope.masters = [];

        $scope.getModules = function() {
            moduleAPIservice.getModules().then(function(resp) {
                $scope.module_list = resp.data.items;
            })
        };
        $scope.loadModule = function() {
            moduleAPIservice.loadModule().then(function(resp) {
                notify.success('载入成功');
                $scope.getModules();
            })
        };
        $scope.current_module = {pid: "0"};
        $scope.newModule = function() {
            moduleAPIservice.newModule($scope.current_module).then(function(resp) {
                notify.success(resp.data.msg);
                $scope.getModules();
            })
        };
        $scope.getMasters = function() {
            moduleAPIservice.getMasters().then(function(resp) {
                $scope.masters = resp.data.items;
            })
        };
        $scope.setModule = function(data) {
            $scope.current_module = data;
        };
        $scope.resetModule = function() {
            $scope.current_module = {pid: "0"};
        }
        $scope.getModules();
        $scope.getMasters();
    }
})()