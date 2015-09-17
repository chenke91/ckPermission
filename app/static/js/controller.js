'use strict';

myApp.controller('MenuController', function($scope, $rootScope, userAPIservice){
    $scope.menu = {
        modules: [],
        current_module: {},
        get_modules: function() {
            userAPIservice.getMenu().success(function(resp) {
                $scope.menu.modules = resp.modules;
                if ($scope.menu.modules) {
                    $scope.menu.current_module = $scope.menu.modules[0];
                }
            });
        },
        selectModule: function(index) {
            $scope.menu.current_module = $scope.menu.modules[index];
        },
        init: function() {
            this.get_modules();
        }
    };
    $scope.menu.init();
});

myApp.controller('AlertCtrl', function($scope, $rootScope) {
    $scope.closeAlert = function(index) {
        $rootScope.alerts.splice(index, 1);
    };
})
