angular.module("youtubemap", [ 'database' ])
.controller("YouTubeMapController", function($scope) {

})
.controller("HistoryController", function($scope, databaseService, $interval) {

	$scope.log = [];

	$scope.refresh = function() {
        databaseService.getHistoryJSON().then(function (response) {
            $scope.log = response.data;
        });
    };

	$interval($scope.refresh, 5000);

	$scope.refresh();
})
.controller("StatsController", function($scope, databaseService, $interval) {

	$scope.data = [];

	$scope.refresh = function() {
        databaseService.getStatsJSON().then(function (response) {
            $scope.data = response.data;
        });
    };

	$interval($scope.refresh, 5000);

	$scope.refresh();
});