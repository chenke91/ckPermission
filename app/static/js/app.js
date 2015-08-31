'use strict';

var myApp = angular.module('myApp', ['ui.bootstrap', 'ngRoute', 'angularjs-dropdown-multiselect']);

myApp.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.headers.common['Accept'] = 'application/json';
}])