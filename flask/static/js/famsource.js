var famSrcApp = angular.module('famsource', ['ui.router']);

famSrcApp.config(function ($stateProvider) {
    $stateProvider
        .state({
            name: "parent",
            url: "/",
            abstract: true,
        })
        .state({
            name: "home",
            url: "/home",
            templateUrl: "/static/html/home.html"
        })
        .state({
            name: "createPlan",
            url: "/createPlan",
            templateUrl: "/static/html/createPlan.html"
        })
        .state({
            name: "joinPlan",
            url: "/joinPlan",
            templateUrl: "/static/html/joinPlan.html"
        })
        .state({
            name: "profile",
            url: "/profile",
            templateUrl: "/static/html/profile.html"
        });
});