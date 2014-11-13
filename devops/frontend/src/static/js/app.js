/* ==========================================================================
   os-wizard
   ========================================================================== */

(function(){

  angular.module( 'OSWizardApp', [] );

  angular.module('OSWizardApp').controller( 'RepoGroupsCtrl', function ( $scope, $http, $filter ) {

    // Properties
    $scope.repoGroups = [];

    // Data
    $http.get( 'repo-groups.json' ).
      success( function( response, status, headers, config ) {
        var preppedResponse = $filter('prepRepoGroupData')( response.groups );
        $scope.repoGroups = preppedResponse;
      });

    // Functions
    $scope.toggleUserType = function ( group, type ) {
      var key = '';
      switch ( type ) {
        case 'admin': key = 'showAdmins';  break;
        case 'read':  key = 'showReaders'; break;
        case 'write': key = 'showWriters'; break;
        default:      key = 'showReaders';
      }
      group[ key ] = !group[ key ];
    };

  });

  // Trying the figure out how to use jQuery plugins with Angular.
  // This doesn't seem like the most intuitive way but it's working for now.
  // https://amitgharat.wordpress.com/2013/02/03/an-approach-to-use-jquery-plugins-with-angularjs/
  // I'm thinking I'll need to make a real expandable directive.
  angular.module('OSWizardApp').directive( 'expandable', function () {
    return {
      restrict: 'A',
      link: function(scope, element, attrs) {
        $(element).expandable();
      }
    };
  });

  /* Add some properties to the repo group data before using it.
     ========================================================================== */
  angular.module('OSWizardApp').filter( 'prepRepoGroupData', function () {
    return function( repoGroups ) {
      var output = [];
      angular.forEach( repoGroups, function( group ) {
        group.showAdmins = false;
        group.showReaders = false;
        group.showWriters = false;
        output.push( group );
      });
      return output;
    };
  });

})();

