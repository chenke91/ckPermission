(function() {
    'use strict';

    angular
        .module('myApp')
        .controller('MenuController', menuController)
        .controller('AlertCtrl', alertController)
        .controller('profileController', profileController);

    menuController.$inject = ['$scope', '$rootScope', 'userAPIservice'];
    alertController.$inject = ['$scope', '$rootScope'];
    profileController.$inject = ['$scope', '$rootScope', 'userAPIservice'];

    function menuController($scope, $rootScope, userAPIservice){
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
    }

    function alertController($scope, $rootScope) {
        $scope.closeAlert = function(index) {
            $rootScope.alerts.splice(index, 1);
        };
    }

    function profileController($scope, $rootScope, userAPIservice) {
        $rootScope.trace = [{
            url: '/#/profile',
            name: '个人中心'
        }];
        $scope.getCurrentUser = function() {
            userAPIservice.getCurrentUser().then(function(resp) {
                $scope.currentUser = resp.data;
            });
        }
        $scope.getCurrentUser();
    }

})()