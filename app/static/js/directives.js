"use strict";

myApp.directive('myNav', function() {
    var config = {
        restrict: "E",
        templateUrl: "/admin/nav.html",
        replace: true
    };
    return config;
})