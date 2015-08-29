'use strict';

myApp.controller('MenuController', function($scope, myAPIservice){
    $scope.menu = {
        modules: [],
        current_module: {},
        get_modules: function() {
            myAPIservice.getMenu().success(function(resp) {
                $scope.menu.modules = resp.modules;
                if ($scope.menu.modules) {
                    $scope.menu.current_module = $scope.menu.modules[0];
                }
            });
        },
        init: function() {
            this.get_modules();
        }
    };
    $scope.menu.init();
});

myApp.controller('UserController', function($scope, myAPIservice) {
    $scope.user = {
        users: [],
        get_users: function() {
            var config = {
                params: {
                    page: this.bigCurrentPage,
                    per_page: this.itemsPerPage
                }
            };
            myAPIservice.getUser(config).success(function(resp) {
                $scope.user.users = resp.items;
                $scope.user.bigTotalItems = resp.total;
            });
        },
        get_roles: function() {
            myAPIservice.getRoles().success(function(resp) {
                $scope.user.role_list = resp.items;
            })
        },
        edit: function(user) {
            alert(user.name);
        },
        //分页
        maxSize : 8,
        bigTotalItems: 0,
        bigCurrentPage: 1,
        itemsPerPage: 10,
        pageChanged: function() {
            this.get_users();
        },
        //multi_drop_down
        role_list: [],
        settings: {
            smartButtonMaxItems: 3,
            displayProp: 'name',
            enableSearch: true
        },
        init: function() {
            this.get_users();
            this.get_roles();
        }
    };
    $scope.user.init();
})