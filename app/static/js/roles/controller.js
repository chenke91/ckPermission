(function() {
    'use strict';

    angular
        .module('myApp')
        .controller('RoleController', roleController);

    roleController.$inject = ['$rootScope', '$scope', 'roleAPIservice', 'notify'];

    function roleController($rootScope, $scope, roleAPIservice, notify) {
        $rootScope.trace = [
            {url: '#/admin/roles',
             name: '角色管理'}
        ];
        $scope.roles = [];
        $scope.getRoles = function() {
            roleAPIservice.getRoles().then(function(resp) {
                $scope.roles = resp.data.items;
            });
        };
        $scope.current_role={};
        $scope.setRole = function(data) {
            $scope.current_role = data;
            _.forEach($scope.module_list, function(module) {
                module.selected = false;
                if ((module.permission & $scope.current_role.permissions) == module.permission) {
                    module.selected = true;
                }
                _.forEach(module.sub_modules, function(module) {
                    module.selected = false;
                    if ((module.permission & $scope.current_role.permissions) == module.permission) {
                        module.selected = true;
                    }
                })
            });
        };
        $scope.resetRole = function() {
            $scope.current_role = {};
            _.forEach($scope.module_list, function(module) {
                module.selected = false;
                _.forEach(module.sub_modules, function(module) {
                    module.selected = false;
                })
            });
        };
        $scope.updateRole = function() {
            roleAPIservice.updateRole($scope.current_role).then(function(resp) {
                notify.success(resp.data.msg);
                $scope.getRoles();
            })
        };
        $scope.getModules = function() {
            roleAPIservice.getModules().then(function(resp) {
                $scope.module_list = resp.data.items;
            })
        };
        $scope.updatePermission = function(module) {
            if (module.selected) {
                $scope.current_role.permissions |= module.permission;
            } else {
                $scope.current_role.permissions &= ($scope.current_role.permissions ^ module.permission);
            }
            console.log($scope.current_role);
        };
        $scope.getRoles();
        $scope.getModules();
    }
})()