(function() {
    'use strict';

    angular
        .module('myApp')
        .controller('UserController', userController)
        .controller('NewUserController', newUserController)
        .controller('EditUserController', editUserController);

    userController.$inject = ['$rootScope', '$scope', 'userAPIservice', 'mynotify'];
    newUserController.$inject = ['$rootScope', '$scope', 'userAPIservice', 'mynotify'];
    editUserController.$inject = ['$rootScope', '$scope', '$stateParams', 'userAPIservice', 'mynotify'];

    function userController($rootScope, $scope, userAPIservice, mynotify) {
        $rootScope.trace = [
            {url: '#/admin/users',
             name: '用户管理'}
        ];
        $scope.user = {
            users: [],
            get_users: function() {
                var config = {
                    params: {
                        page: this.bigCurrentPage,
                        per_page: this.itemsPerPage
                    }
                };
                userAPIservice.getUsers(config).success(function(resp) {
                    $scope.user.users = resp.items;
                    $scope.user.bigTotalItems = resp.total;
                });
            },
            get_roles: function() {
                userAPIservice.getRoles().success(function(resp) {
                    $scope.user.role_list = resp.items;
                })
            },
            delete_toggle: function(user) {
                userAPIservice.deleteToggleUser(user.id).then(function(resp) {
                    user.avalible = resp.data.avalible;
                })
            },
            /*
                分页
            */
            maxSize : 8,
            bigTotalItems: 0,
            bigCurrentPage: 1,
            itemsPerPage: 10,
            pageChanged: function() {
                this.get_users();
            },
            /*
                multi_drop_down
            */
            role_list: [],
            settings: {
                smartButtonMaxItems: 3,
                displayProp: 'name',
                showCheckAll: false,
                showUncheckAll: false,
            },
            init: function() {
                this.get_users();
                this.get_roles();
            }
        };
        $scope.user.init();
    }

    function newUserController($rootScope, $scope, userAPIservice, mynotify) {
        $rootScope.trace = [
            {url: '#/admin/users',
             name: '用户管理'},
            {url: '#/admin/new_user',
             name: '新增'}
        ];
        $scope.user = {
            action: '新增用户',
            current_user: {},
            role_list: [],
            get_roles: function() {
                userAPIservice.getRoles().success(function(resp) {
                    $scope.user.role_list = resp.items;
                })
            },
            add: function(valid) {
                if (!valid) {
                    mynotify.error('信息填写有误');
                    return;
                }
                var user_data = $scope.user.current_user;
                if (user_data.password != user_data.repass) {
                    mynotify.error('两次密码不一致');
                    return;
                }
                var selected_role_ids = _.map(_.filter($scope.user.role_list, function(role) {
                    return role.selected;
                }), 'id');
                if (selected_role_ids.length == 0) {
                    mynotify.error('请选择角色');
                    return;
                }
                user_data.role_ids = selected_role_ids;
                userAPIservice.newUser(user_data);
            },
            init: function() {
                this.get_roles();
            }
        };
        $scope.user.init();
    }

    function editUserController($rootScope, $scope, $stateParams, userAPIservice, mynotify) {
        $rootScope.trace = [
            {url: '#/admin/users',
             name: '用户管理'},
            {url: '#/admin/edit_user',
             name: '编辑'}
        ];
        $scope.user = {
            action: '编辑用户',
            current_user: {},
            role_list: [],
            get_current_user: function(id) {
                userAPIservice.getUser(id).then(function(resp) {
                        $scope.user.current_user = resp.data;
                        $scope.user.role_list = resp.data.user_roles;
                })
            },
            update: function() {
                var user_data = $scope.user.current_user;
                if (user_data.password != user_data.repass) {
                    mynotify.error('两次密码不一致');
                    return;
                }
                var selected_role_ids = _.map(_.filter($scope.user.role_list, function(role) {
                    return role.selected;
                }), 'id');
                if (selected_role_ids.length == 0) {
                    mynotify.error('请选择角色');
                    return;
                }
                user_data.role_ids = selected_role_ids;
                userAPIservice.updateUser(user_data, $stateParams.id);
            },
            init: function() {
                this.get_current_user($stateParams.id);
            }
        };
        $scope.user.init();
    }
})();