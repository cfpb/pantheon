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

/* ==========================================================================
   users directive
   Creates a toggleable list of users.

   role:  The user role you wish to display.
          Can be "Admin", "Write", or "Read", capitalization is important.
   group: A reference to a group object.

   Example:
      <section ng-repeat="group in repoGroups">
          <users role="Admin"
                 group="group"
                 class="group-content_list">
          </users>
      </section>
   ========================================================================== */
  angular.module('OSWizardApp').directive( 'users', function() {
    return {
      restrict: 'E',
      scope: { group: '=' },
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
        scope.visiblityKey = 'show' + scope.role;
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
        group.showAdmin = false;
        group.showWrite = false;
        group.showRead = false;
        output.push( group );
      });
      return output;
    };
  });

})();

