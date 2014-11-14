/* ==========================================================================
   os-wizard
   ========================================================================== */

(function(){

  angular.module( 'OSWizardApp', [] );

  angular.module('OSWizardApp').controller( 'RepoGroupsCtrl', function( $scope, $http, $filter ) {

    // Properties
    $scope.repoGroups = [];

    // Data
    $http.get( 'repo-groups.json' ).
      success( function( response, status, headers, config ) {
        var preppedResponse = $filter('prepRepoGroupData')( response.groups );
        $scope.repoGroups = preppedResponse;
      });
  });

  angular.module('OSWizardApp').directive( 'users', function() {
    return {
      restrict: 'E',
      controller: function( $scope ) {
        // Functions
        $scope.toggle = function( group, role ) {
          var key = '';
          switch ( role.toLowerCase() ) {
            case 'admin': key = 'showAdmins';  break;
            case 'read':  key = 'showReaders'; break;
            case 'write': key = 'showWriters'; break;
            default:      key = 'showReaders';
          }
          group[ key ] = !group[ key ];
        };
      },
      scope: {
        group: '='
      },
      templateUrl: '/static/templates/users.html',
      link: function( scope, element, attrs ) {
        // Properties
        scope.role = attrs.role;
        scope.users = scope.group.permissions[scope.role.toLowerCase()];
        if ( typeof scope.users === 'undefined' ) {
          scope.total = 0;
        } else {
          scope.total = scope.users.length;
        }
        if ( scope.role === 'Admin' ) {
          scope.show = 'showAdmins';
        } else if ( scope.role === 'Write' ) {
          scope.show = 'showWriters';
        } else if ( scope.role === 'Read' ) {
          scope.show = 'showReaders';
        }
      }
    };
  });

  // Trying the figure out how to use jQuery plugins with Angular.
  // This doesn't seem like the most intuitive way but it's working for now.
  // https://amitgharat.wordpress.com/2013/02/03/an-approach-to-use-jquery-plugins-with-angularjs/
  // I'm thinking I'll need to make a real expandable directive.
  angular.module('OSWizardApp').directive( 'expandable', function() {
    return {
      restrict: 'A',
      link: function(scope, element, attrs) {
        $(element).expandable();
      }
    };
  });

  /* Add some properties to the repo group data before using it.
     ========================================================================== */
  angular.module('OSWizardApp').filter( 'prepRepoGroupData', function() {
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

