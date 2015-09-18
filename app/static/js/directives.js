(function() {
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
})();