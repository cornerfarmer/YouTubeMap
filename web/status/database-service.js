angular.module('database', [])
.factory('databaseService', function($http) {
  var databaseServiceInstance = {};
 
  databaseServiceInstance.getHistoryJSON = function() {
	  return $http.get('/api/getHistory.php');
  };

  databaseServiceInstance.getStatsJSON = function() {
	  return $http.get('/api/getStats.php');
  };

  databaseServiceInstance.getDetailJSON = function(hash, limitStart, limitCount) {
	  return $http({
		url: 'getHistory.php',
		method: "GET",
		params: {level: hash, limitStart: limitStart, limitCount: limitCount}
	  });
  };
  
  return databaseServiceInstance;
});