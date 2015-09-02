'use strict';

myApp.controller('ModuleController', function($scope, $rootScope, moduleAPIservice){
    $rootScope.trace = [
        {url: '#/admin/modules',
         name: '模块管理'}
    ];
    $scope.module_list = [];
    $scope.getModules = function() {
        moduleAPIservice.getModules().then(function(resp) {
            $scope.module_list = resp.data.items;
        }, function(resp) {
            $rootScope.addAlert('danger', resp.data.message);
        })
    }
    $scope.getModules();
});