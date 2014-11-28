/* ==========================================================================
   dev-dash

   # RepoGroupsCtrl controller
   # group directive
   # repo directive
   # repobutton directive
   # userbutton directive
   # userlist directive
   # role directive
   # expandable directive
   # prepRepoGroupData filter
   ========================================================================== */

(function(){

  angular.module( 'OSWizardApp', [] );

  /* ==========================================================================
     # RepoGroupsCtrl controller
     The main controller. All it really does is grabs a JSON file, filters it
     and sets two main properties used throughout the app.
     ========================================================================== */

  angular.module('OSWizardApp').controller( 'RepoGroupsCtrl', function( $scope, $http, $filter ) {
    // Properties
    $scope.users = {};
    $scope.user = {};
    $scope.permission = '';
    $scope.repoGroups = [];
    // Functions
    $scope.getUsername = function( id ) {
      if ( $scope.users[id] ) {
        return $scope.users[id].username;
      } else {
        return '';
      }
    };
    // Data
    $http.get( 'test-data.json' ).
      success( function( response, status, headers, config ) {
        var preppedResponse = $filter('prepRepoGroupData')( response.groups );
        $scope.users = response.users;
        $scope.user = response.user;
        $scope.permission = response.permission;
        $scope.repoGroups = preppedResponse;
      });
  });

  /* ==========================================================================
     # group directive
     Displays a repo group.

     Example:
        <group ng-repeat="group in repoGroups">
        </group>

     group: This property is required. In this example it is getting accessed
            through `group in repoGroups`. It should point to a group object
            with name, permissions, and repos properties.

     Note: This directive uses the following directives:
           - repo
           - repobutton
           - userbutton
           - userlist
     ========================================================================== */

  angular.module('OSWizardApp').directive( 'group', function() {
    return {
      restrict: 'E',
      // Priority forces this directive to run before ng-repeat:
      // http://stackoverflow.com/questions/15344306/angularjs-ng-repeat-in-combination-with-custom-directive
      priority: 1001,
      templateUrl: '/static/templates/group.html'
    };
  });

  /* ==========================================================================
     # repo directive
     Displays a repo from a repo group.

     repo: This property is required. It should point to a repo object that has
           name and permissions properties.

     Example:
        <repo ng-repeat="repo in group.repos
              repo="repo">
        </repo>
     ========================================================================== */

  angular.module('OSWizardApp').directive( 'repo', function() {
    return {
      restrict: 'E',
      templateUrl: '/static/templates/repo.html'
    };
  });

  /* ==========================================================================
     # repobutton directive
     Creates a button to toggle a list of repos on and off.

     group: A reference to a repo group object.
     role:  The permission role you wish to display.
            Can be "Admin", "Write", or "Read", capitalization is important.
     show: The state variable that the button should toggle.

     Example:
        <userbutton group="group"
                    role="Admin"
                    show="group.showRead">
        </userbutton>

     TODO: Merge with userbutton since they do almost the exact same thing.
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
          $scope.group.showAdmin = false;
          $scope.group.showWrite = false;
          $scope.group.showRead = false;
          $scope.show = !show;
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
     # userbutton directive
     Creates a button of a certain type of user

     group: A reference to a repo group object.
     role:  The permission role you wish to display.
            Can be "Admin", "Write", or "Read", capitalization is important.
     show: The state variable that the button should toggle.

     Example:
        <userbutton role="Admin"
                    group="group">
        </userbutton>

     TODO: Merge with userbutton since they do almost the exact same thing.
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
     # userlist directive
     Creates a toggleable list of users.

     group: A reference to a repo group object.
     role:  The permission role you wish to display.
            Can be "Admin", "Write", or "Read", capitalization is important.

     Example:
        <userlist group="group"
                  role="Admin">
        </userlist>
     ========================================================================== */

  angular.module('OSWizardApp').directive( 'userlist', function() {
    return {
      restrict: 'E',
      scope: {
        filter: '=',
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
        // console.log( scope.getUsername );
      }
    };
  });

  /* ==========================================================================
     # role directive
     A simple role label.

     group: A reference to a repo group object.
     user:  The username you want to use to figure out the role.

     Example:
        <role group="group"
              user="a_username">
        </userlist>
     ========================================================================== */

  angular.module('OSWizardApp').directive( 'role', function() {
    return {
      restrict: 'E',
      scope: {
        group: '='
      },
      templateUrl: '/static/templates/role.html',
      link: function( scope, element, attrs ) {
        // Properties
        var permissions = scope.group.permissions;
        scope.role = 'read';
        console.log(attrs.username);
        if ( permissions.read ) {
          if ( permissions.read.indexOf( attrs.username ) > -1 ) {
            scope.role = 'read';
          }
        }
        if ( permissions.write ) {
          if ( permissions.write.indexOf( attrs.username ) > -1 ) {
            scope.role = 'write';
          }
        }
        if ( permissions.admin ) {
          if ( permissions.admin.indexOf( attrs.username ) > -1 ) {
            scope.role = 'admin';
          }
        }
        element.addClass('role-icon');
        element.addClass( 'role-icon__' + scope.role );
      }
    };
  });

  /* ==========================================================================
     # expandable directive

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

  /* ==========================================================================
     # prepRepoGroupData filter
     Adds some properties to the repo group data before using it.
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
