(function() {
    'use strict';

    angular.module('myApp',
        ['ui.bootstrap',
        'angularjs-dropdown-multiselect',
        'ngMessages',
        'angular-loading-bar',
        'ui.router']);


    var csrftoken = $('meta[name=csrf-token]').attr('content');

    angular
        .module('myApp')
        .config(httpSetting)
        .run(runApp);

    httpSetting.$inject = ['$httpProvider'];
    runApp.$inject = ['$rootScope'];

    function httpSetting($httpProvider) {
        $httpProvider.defaults.headers.common['Accept'] = 'application/json';
        $httpProvider.defaults.headers.post['X-CSRFToken'] = csrftoken;
        $httpProvider.interceptors.push('errorResponse');
    }

    function runApp($rootScope) {
        $rootScope.alerts = [];
    }

})();(function() {
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

})();(function() {
    "use strict";

    angular
        .module('myApp')
        .directive('moduleTree', moduleTree);

    function moduleTree() {
        var config = {
            restrict: "E",
            templateUrl: "/static/templates/tpls/moduleTree.html",
            replace: true,
            scope: {
                modules: '=',
                setfunc: '&'
            },
            link: function(scope, element, attrs) {
                scope.toggle = function(module) {
                    module.show = !module.show;
                }
            }
        };
        return config;
    }
})();(function() {
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
})();(function() {
    "use strict";

    angular
        .module('myApp')
        .service('moduleAPIservice', moduleAPIservice);

    moduleAPIservice.$inject = ['$http'];

    function moduleAPIservice($http) {

        this.getModules = function() {
            return $http.get('/admin/modules/');
        };
        this.loadModule = function() {
            return $http.get('/admin/modules/load/');
        };
        this.newModule = function(data) {
            return $http.post('/admin/modules/add/', data);
        };
        this.getMasters = function() {
            return $http.get('/admin/modules/masters/');
        };
    }
})();(function() {
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
})();(function() {
    "use strict";

    angular
        .module('myApp')
        .service('roleAPIservice', roleAPIservice);

    roleAPIservice.$inject = ['$http'];

    function roleAPIservice($http) {
        this.getRoles = function() {
            return $http.get('/admin/roles/');
        };
        this.updateRole = function(data) {
            return $http.post('/admin/roles/update/', data);
        };
        this.getModules = function() {
            return $http.get('/admin/roles/modules/');
        }
    }
})();(function() {
    'use strict';

    angular
        .module('myApp')
        .config(router);

    router.$inject = ['$stateProvider'];

    function router($stateProvider) {
        $stateProvider
            .state('index', {
                url: '/',
                templateUrl: '/static/templates/index.html'
            })
            .state('profile', {
                url: '/profile',
                templateUrl: '/static/templates/system/profile.html',
                controller: 'profileController'
            })
            .state('/admin/users', {
                url: '/admin/users',
                templateUrl : '/static/templates/system/users.html',
                controller : 'UserController'
            })
            .state('/admin/new_user', {
                url: '/admin/new_user',
                templateUrl : '/static/templates/system/user_add.html',
                controller : 'NewUserController'
            })
            .state('/admin/edit_user', {
                url: '/admin/edit_user/:id',
                templateUrl : '/static/templates/system/user_edit.html',
                controller : 'EditUserController'
            })
            .state('/admin/roles', {
                url: '/admin/roles',
                templateUrl: '/static/templates/system/roles.html',
                controller: 'RoleController'
            })
            .state('/admin/modules', {
                url: '/admin/modules',
                templateUrl: '/static/templates/system/modules.html',
                controller: 'ModuleController'
            })
            .state('/admin/icons', {
                url: '/admin/icons',
                templateUrl: '/static/templates/system/icons.html'
            })
    }
})();(function() {
    'use strict'
    angular
        .module('myApp')
        .factory('notify', notify)
        .factory('errorResponse', errorResponse);

    notify.$inject = ['$rootScope'];
    errorResponse.$inject = ['$q', 'notify'];

    function notify($rootScope) {
        return {
            success: function(msg) {
                $rootScope.alerts.push({type: 'success', msg: msg});
            },
            error: function(msg) {
                $rootScope.alerts.push({type: 'danger', msg: msg});
            }
        }
    }

    function errorResponse($q, notify) {
        return {
            responseError: function(rejection) {
                if (rejection.status == 400) {
                    notify.error(rejection.data.message);
                }
                return $q.reject(rejection);
            }
        }
    }
})();(function() {
    'use strict';

    angular
        .module('myApp')
        .controller('UserController', userController)
        .controller('NewUserController', newUserController)
        .controller('EditUserController', editUserController);

    userController.$inject = ['$rootScope', '$scope', 'userAPIservice', 'notify'];
    newUserController.$inject = ['$rootScope', '$scope', 'userAPIservice', 'notify'];
    editUserController.$inject = ['$rootScope', '$scope', '$stateParams', 'userAPIservice', 'notify'];

    function userController($rootScope, $scope, userAPIservice, notify) {
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

    function newUserController($rootScope, $scope, userAPIservice, notify) {
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
                    notify.error('信息填写有误');
                    return;
                }
                var user_data = $scope.user.current_user;
                if (user_data.password != user_data.repass) {
                    notify.error('两次密码不一致');
                    return;
                }
                var selected_role_ids = _.map(_.filter($scope.user.role_list, function(role) {
                    return role.selected;
                }), 'id');
                if (selected_role_ids.length == 0) {
                    notify.error('请选择角色');
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

    function editUserController($rootScope, $scope, $stateParams, userAPIservice, notify) {
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
                    notify.error('两次密码不一致');
                    return;
                }
                var selected_role_ids = _.map(_.filter($scope.user.role_list, function(role) {
                    return role.selected;
                }), 'id');
                if (selected_role_ids.length == 0) {
                    notify.error('请选择角色');
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
})();(function() {
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
})();