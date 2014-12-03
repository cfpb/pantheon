/* ==========================================================================
   dev-dash

   # UserService service
   # RepoGroupsCtrl controller
   # group directive
   # repo directive
   # repobutton directive
   # userbutton directive
   # userlist directive
   # role directive
   # expandable directive
   # username filter
   # inUser filter
   # toArray filter
   # prepRepoGroupData filter
   # Cross Site Request Forgery protection
   # getObjKeyByVal
   ========================================================================== */

(function(){

  angular.module( 'OSWizardApp', [] );

  /* ==========================================================================
     # UserService service
     A single source for getting user data.
     ========================================================================== */

  angular.module('OSWizardApp').factory( 'UserService', function() {
    var user = { id: '', name: '', permission: 'read' };
    var users = {};
    var usersArray = [];
    return {
      user: user,
      users: users,
      usersArray: usersArray,
      getName: function( id ) {
        if ( this.users[id] ) {
          return this.users[id].username;
        } else {
          return '';
        }
      }
    };
  });

  /* ==========================================================================
     # RepoGroupsCtrl controller
     The main controller. All it really does is grabs a JSON file, filters it
     and sets two main properties used throughout the app.
     ========================================================================== */

  angular.module('OSWizardApp').controller( 'RepoGroupsCtrl', function( $scope, $http, $filter, UserService ) {
    // Properties
    $scope.user = UserService.user;
    $scope.users = UserService.users;
    $scope.repoGroups = [];
    // Data
    $http.get( '/kratos/teams/' ).
      success( function( response, status, headers, config ) {
        var preppedResponse = $filter('prepRepoGroupData')( response.groups );
        UserService.users = response.users;
        UserService.usersArray = $filter('toArray')( UserService.users );
        UserService.user.id = response.user;
        UserService.user.name = UserService.getName( response.user );
        UserService.user.permission = response.permission;
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

  angular.module('OSWizardApp').directive( 'userlist', function( $compile, $filter, UserService ) {
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
        scope.editable = UserService.user.permission === 'admin';
        scope.role = attrs.role;
        scope.users = [];
        angular.forEach( scope.group.permissions[scope.role.toLowerCase()], function( value, key ) {
          scope.users.push( UserService.users[value] );
        });
        scope.allUsers = $filter('inUser')( scope.users );
        if ( typeof scope.users === 'undefined' ) {
          scope.total = 0;
        } else {
          scope.total = scope.users.length;
        }
        scope.showAllUsers = false;
        // Functions
        scope.inUserList = function( user ) {
          return scope.users.indexOf( user ) > -1;
        };
        scope.editUser = function( action, user ) {
          var requestURL = '/kratos/' +
                'teams/' + scope.group.name + '/' +
                'members/' +  scope.role.toLowerCase() + '/' +
                getObjKeyByVal( UserService.users, user ) + '/',
              requestType = '';
          if ( action === 'add' ) {
            requestType = 'PUT';
          } else if ( action === 'remove' ) {
            requestType = 'DELETE';
          }
          $.ajax({
            type: requestType,
            url: requestURL
          })
          .done(function( msg ) {
            console.log( 'Data Saved: ' + msg );
          })
          .error(function( msg ) {
            console.log( 'Error:', msg );
          });
        };
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
        if ( permissions.read ) {
          if ( permissions.read.indexOf( attrs.username * 1 ) > -1 ) {
            scope.role = 'read';
          }
        }
        if ( permissions.write ) {
          if ( permissions.write.indexOf( attrs.username * 1 ) > -1 ) {
            scope.role = 'write';
          }
        }
        if ( permissions.admin ) {
          if ( permissions.admin.indexOf( attrs.username * 1 ) > -1 ) {
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
     # username filter
     Get the username from a user id.
     ========================================================================== */
  angular.module('OSWizardApp').filter( 'username', function( UserService ) {
    return function( id ) {
      return UserService.getName( id );
    };
  });

  /* ==========================================================================
     # inUser filter
     Filter a user list with another user list.
     ========================================================================== */
  angular.module('OSWizardApp').filter( 'inUser', function( UserService ) {
    return function( users ) {
      var filteredUsers = [];
      angular.forEach( UserService.usersArray, function( user ) {
        if ( users.indexOf( user ) === -1 ) {
          filteredUsers.push( user );
        }
      });
      return filteredUsers;
    };
  });

  /* ==========================================================================
     # toArray filter
     A very simple object to array filter.
     ========================================================================== */
  angular.module('OSWizardApp').filter( 'toArray', function() {
    return function( obj ) {
      var array = [];
      angular.forEach( obj, function( obj_prop ) {
        array.push( obj_prop );
      });
      return array;
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

  /* ==========================================================================
     # Cross Site Request Forgery protection
     https://docs.djangoproject.com/en/1.7/ref/contrib/csrf/#ajax
     ========================================================================== */
  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
        var cookie = jQuery.trim(cookies[i]);
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) == (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
  var csrftoken = getCookie('csrftoken');

  function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  }
  function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
  }
  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
      if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
        // Send the token to same-origin, relative URLs only.
        // Send the token only if the method warrants CSRF protection
        // Using the CSRFToken value acquired earlier
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
    }
  });

  /* ==========================================================================
     # getObjKeyByVal
     http://stackoverflow.com/questions/9907419/javascript-object-get-key-by-value
     ========================================================================== */
  getObjKeyByVal = function( obj, value ) {
    for( var prop in obj ) {
      if( obj.hasOwnProperty( prop ) ) {
         if( obj[ prop ] === value ) {
           return prop;
         }
      }
    }
  };

})();
