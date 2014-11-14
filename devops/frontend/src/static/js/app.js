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
     group directive
     Displays a repo group.

     Example:
        <group ng-repeat="group in repoGroups"></group>
     ========================================================================== */

  angular.module('OSWizardApp').directive( 'group', function() {
    return {
      restrict: 'E',
      scope: {
        group: '='
      },
      // Priority forces this directive to run before ng-repeat:
      // http://stackoverflow.com/questions/15344306/angularjs-ng-repeat-in-combination-with-custom-directive
      priority: 1001,
      templateUrl: '/static/templates/group.html'
    };
  });

  /* ==========================================================================
     repo directive
     Displays a repo from a group.

     Example:
        ...
     ========================================================================== */

  angular.module('OSWizardApp').directive( 'repo', function() {
    return {
      restrict: 'E',
      scope: {
        repo: '='
      },
      // Priority forces this directive to run before ng-repeat:
      // http://stackoverflow.com/questions/15344306/angularjs-ng-repeat-in-combination-with-custom-directive
      // priority: 1001,
      templateUrl: '/static/templates/repo.html'
    };
  });

  /* ==========================================================================
     repobutton directive
     Creates a button to toggle the repo view

     group: A reference to a group object.
     show: The state variable that the button should toggle.

     Example:
        <userbutton role="Admin"
                    group="group">
        </userbutton>
     ========================================================================== */

  angular.module('OSWizardApp').directive( 'repobutton', function() {
    return {
      restrict: 'E',
      scope: {
        group: '=',
        show: '='
      },
      controller: function( $scope ) {
        $scope.toggle = function( show ) {
          var toggledShow = !show;
          $scope.group.showAdmin = false;
          $scope.group.showWrite = false;
          $scope.group.showRead = false;
          $scope.group.showRepo = false;
          $scope.show = toggledShow;
        };
      },
      templateUrl: '/static/templates/repobutton.html',
      link: function( scope, element, attrs ) {
        // Properties
        scope.repos = scope.group.repos;
        if ( typeof scope.repos === 'undefined' ) {
          scope.total = 0;
        } else {
          scope.total = scope.repos.length;
        }
        // Events
        element.on( 'click', function() {
          if ( scope.show ) {
            element.parents('.expandable')[0].expand();
          } else {
            element.parents('.expandable')[0].collapse();
          }
        });
      }
    };
  });

  /* ==========================================================================
     userbutton directive
     Creates a button of a certain type of user

     group: A reference to a group object.
     role:  The user role you wish to display.
            Can be "Admin", "Write", or "Read", capitalization is important.
     show: The state variable that the button should toggle.

     Example:
        <userbutton role="Admin"
                    group="group">
        </userbutton>
     ========================================================================== */

  angular.module('OSWizardApp').directive( 'userbutton', function() {
    return {
      restrict: 'E',
      scope: {
        group: '=',
        show: '='
      },
      controller: function( $scope ) {
        $scope.toggle = function( show ) {
          var toggledShow = !show;
          $scope.group.showAdmin = false;
          $scope.group.showWrite = false;
          $scope.group.showRead = false;
          $scope.group.showRepo = false;
          $scope.show = toggledShow;
        };
      },
      templateUrl: '/static/templates/userbutton.html',
      link: function( scope, element, attrs ) {
        // Properties
        scope.role = attrs.role;
        scope.users = scope.group.permissions[scope.role.toLowerCase()];
        if ( typeof scope.users === 'undefined' ) {
          scope.total = 0;
        } else {
          scope.total = scope.users.length;
        }
        // Events
        element.on( 'click', function() {
          if ( scope.show ) {
            element.parents('.expandable')[0].expand();
          } else {
            element.parents('.expandable')[0].collapse();
          }
        });
      }
    };
  });

  /* ==========================================================================
     userlist directive
     Creates a toggleable list of users.

     role:  The user role you wish to display.
            Can be "Admin", "Write", or "Read", capitalization is important.
     group: A reference to a group object.

     Example:
        <section ng-repeat="group in repoGroups">
            <userlist role="Admin"
                      group="group"
                      class="group-content_list">
            </userlist>
        </section>
     ========================================================================== */

  angular.module('OSWizardApp').directive( 'userlist', function() {
    return {
      restrict: 'E',
      scope: {
        group: '=',
        show: '='
      },
      templateUrl: '/static/templates/userlist.html',
      link: function( scope, element, attrs ) {
        // Properties
        scope.role = attrs.role;
        scope.users = scope.group.permissions[scope.role.toLowerCase()];
        if ( typeof scope.users === 'undefined' ) {
          scope.total = 0;
        } else {
          scope.total = scope.users.length;
        }
      }
    };
  });

  /* ==========================================================================
     Trying the figure out how to use jQuery plugins with Angular.
     This doesn't seem like the most intuitive way but it's working for now.
     https://amitgharat.wordpress.com/2013/02/03/an-approach-to-use-jquery-plugins-with-angularjs/
     I'm thinking I'll need to make a real expandable directive.
     ========================================================================== */

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
        group.showRepo = false;
        angular.forEach( group.repos, function( repo ) {
          repo.showAdmin = false;
          repo.showWrite = false;
          repo.showRead = false;
        });
        output.push( group );
      });
      return output;
    };
  });

})();

