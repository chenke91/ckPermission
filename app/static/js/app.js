'use strict';

var myApp = angular.module('myApp',
    ['ui.bootstrap', 'ngRoute', 'angularjs-dropdown-multiselect', 'ngMessages']);
var csrftoken = $('meta[name=csrf-token]').attr('content');

myApp.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.headers.common['Accept'] = 'application/json';
    $httpProvider.defaults.headers.post['X-CSRFToken'] = csrftoken;
}])