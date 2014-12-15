/* ==========================================================================
   dev-dash

   # UserService service
   # TeamsCtrl controller
   # team directive
   # repobutton directive
   # userbutton directive
   # userlist directive
   # role directive
   # expandable directive
   # username filter
   # userListArray filter
   # toArray filter
   # prepTeamData filter
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
    var user = { id: '', name: '' };
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
      },
      isTeamAdmin: function( permissions ) {
        if ( typeof permissions !== 'undefined' ) {
          return permissions.indexOf( this.user.id ) > -1;
        } else {
          return false;
        }
      }
    };
  });

  /* ==========================================================================
     # TeamsCtrl controller
     The main controller. All it really does is grabs a JSON file, filters it
     and sets two main properties used throughout the app.
     ========================================================================== */

  angular.module('OSWizardApp').controller( 'TeamsCtrl', function( $scope, $http, $filter, UserService ) {
    // Properties
    $scope.user = UserService.user;
    $scope.users = UserService.users;
    $scope.teams = [];
    // Data
    $http.get('/kratos/teams/').
      success( function( response, status, headers, config ) {
        var preppedResponse = $filter('prepTeamData')( response.groups );
        UserService.users = response.users;
        UserService.usersArray = $filter('toArray')( UserService.users );
        UserService.user.id = response.user;
        UserService.user.name = UserService.getName( response.user );
        $scope.teams = preppedResponse;
      });
  });

  /* ==========================================================================
     # team directive
     Displays a team.

     Example:
        <section data="team" ng-repeat="team in teams">
        </section>

     data: This property is required. In this example it is getting accessed
           through `team in teams`. It should point to a team object with name,
           permissions, and repos properties.

     Note: This directive uses the following directives:
           - expandable
           - role
           - userbutton
           - userlist
     ========================================================================== */

  angular.module('OSWizardApp').directive( 'team', function() {
    return {
      restrict: 'A',
      scope: {
        data: '='
      },
      templateUrl: '/static/templates/team.html'
    };
  });

  /* ==========================================================================
     # repobutton directive
     Creates a button to toggle a list of repos on and off.

     team-model: A reference to a team model.

     Example:
        <repobutton team-model="team"></repobutton>

     TODO: Merge with userbutton since they do almost the exact same thing.
     ========================================================================== */

  angular.module('OSWizardApp').directive( 'repobutton', function() {
    return {
      restrict: 'E',
      scope: {
        teamModel: '=',
        show: '='
      },
      controller: function( $scope ) {
        $scope.toggle = function( show ) {
          $scope.teamModel.showAdmin = false;
          $scope.teamModel.showWrite = false;
          $scope.teamModel.showRead = false;
          $scope.show = !show;
        };
      },
      templateUrl: '/static/templates/repobutton.html',
      link: function( scope, element, attrs ) {
        // Properties
        scope.repos = scope.teamModel.repos;
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

     team-model: A reference to a team model.

     Example:
        <userbutton team-model="team"></userbutton>

     TODO: Merge with repobutton since they do almost the exact same thing.
     ========================================================================== */

  angular.module('OSWizardApp').directive( 'userbutton', function() {
    return {
      restrict: 'E',
      scope: {
        teamModel: '=',
        show: '='
      },
      controller: function( $scope ) {
        $scope.toggle = function( show ) {
          var toggledShow = !show;
          $scope.teamModel.showAdmin = false;
          $scope.teamModel.showWrite = false;
          $scope.teamModel.showRead = false;
          $scope.teamModel.showRepo = false;
          $scope.show = toggledShow;
        };
      },
      templateUrl: '/static/templates/userbutton.html',
      link: function( scope, element, attrs ) {
        // Properties
        scope.role = attrs.role;
        scope.users = scope.teamModel.permissions[scope.role.toLowerCase()];
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

     team-model: A reference to a team model.
     role:       The permission role you wish to display.
                 Can be "Admin", "Write", or "Read", capitalization is important.

     Example:
        <userlist team-model="team" role="Admin"></userlist>
     ========================================================================== */

  angular.module('OSWizardApp').directive( 'userlist', function( $compile, $filter, UserService ) {
    return {
      restrict: 'A',
      scope: {
        filter: '=',
        teamModel: '=',
        show: '='
      },
      templateUrl: '/static/templates/userlist.html',
      link: function( scope, element, attrs ) {
        // Properties
        scope.role = attrs.role;
        scope.listPermissions = scope.teamModel.permissions[ scope.role.toLowerCase() ];
        scope.isTeamAdmin = UserService.isTeamAdmin( scope.teamModel.permissions.admin );
        scope.editable = scope.isTeamAdmin && scope.role !== 'Admin';
        scope.users = [];
        scope.showAllUsers = false;
        angular.forEach( scope.listPermissions, function( value, key ) {
          scope.users.push( UserService.users[value] );
        });
        scope.requestURL = '/kratos/teams/' + scope.teamModel.name +
                           '/members/' + scope.role.toLowerCase() + '/';
        // Functions
        scope.updateUsers = function() {
          scope.allUsers = $filter('userListArray')( scope.users );
          if ( typeof scope.users === 'undefined' ) {
            scope.total = 0;
          } else {
            scope.total = scope.users.length;
          }
        };
        scope.inUserList = function( user ) {
          return scope.users.indexOf( user ) > -1;
        };
        scope.add = function( user ) {
          var user_id = getObjKeyByVal( UserService.users, user );
          $.ajax({
            type: 'PUT',
            url: scope.requestURL + user_id
          })
          .done(function( msg ) {
            console.log( 'Data Saved:', msg );
            scope.$apply(function () {
              scope.users.push( UserService.users[ user_id ] );
              scope.updateUsers();
            });
          })
          .error(function( msg ) {
            console.log( 'Error:', msg );
          });
        };
        scope.remove = function( user ) {
          var user_id = getObjKeyByVal( UserService.users, user );
          $.ajax({
            type: 'DELETE',
            url: scope.requestURL + user_id
          })
          .done(function( msg ) {
            console.log( 'Data Saved:', msg );
            scope.$apply(function () {
              var index = scope.users.indexOf( UserService.users[ user_id ] );
              scope.users.splice( index, 1 );
              scope.updateUsers();
            });
          })
          .error(function( msg ) {
            console.log( 'Error:', msg );
          });
        };
        // Init
        scope.updateUsers();
      }
    };
  });

  /* ==========================================================================
     # role directive
     Creates a label identifying the current users permission for a given team.

     team-model: A reference to a team model.

     Example:
        <role teamModel="team"></role>
     ========================================================================== */

  angular.module('OSWizardApp').directive( 'role', function( UserService ) {
    return {
      restrict: 'E',
      scope: {
        teamModel: '=',
        username: '='
      },
      templateUrl: '/static/templates/role.html',
      link: function( scope, element, attrs ) {
        // Properties
        var permissions = scope.teamModel.permissions;
        scope.role = 'read';
        if ( permissions.read ) {
          if ( permissions.read.indexOf( UserService.user.id * 1 ) > -1 ) {
            scope.role = 'read';
          }
        }
        if ( permissions.write ) {
          if ( permissions.write.indexOf( UserService.user.id * 1 ) > -1 ) {
            scope.role = 'write';
          }
        }
        if ( permissions.admin ) {
          if ( permissions.admin.indexOf( UserService.user.id * 1 ) > -1 ) {
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
     # hasCurrentUser filter
     Figures out if the current user is in a team.
     ========================================================================== */
  angular.module('OSWizardApp').filter( 'hasCurrentUser', function( UserService ) {
    return function( teams, toggle ) {
      var newTeams = [],
          inOut = true;
      if ( typeof toggle !== 'undefined' ) {
        inOut = toggle;
      }
      angular.forEach( teams, function( team ) {
        var inTeam = false;
        angular.forEach( team.permissions, function( permission ) {
          if ( permission.indexOf( UserService.user.id ) > -1 ) {
            inTeam = true;
          }
        });
        if ( inOut ) {
          if ( inTeam ) {
            newTeams.push( team );
          }
        } else {
          if ( !inTeam ) {
            newTeams.push( team );
          }
        }
      });
      return newTeams;
    };
  });

  /* ==========================================================================
     # userListArray filter
     Filter a user list for use in a userlist.
     ========================================================================== */
  angular.module('OSWizardApp').filter( 'userListArray', function( UserService ) {
    return function( users ) {
      var filteredUsers = [];
      angular.forEach( UserService.usersArray, function( user ) {
        if ( users.indexOf( user ) === -1 && user.stub === false ) {
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
     # prepTeamData filter
     Adds some properties to the team data before using it.
     ========================================================================== */
  angular.module('OSWizardApp').filter( 'prepTeamData', function() {
    return function( teams ) {
      var output = [];
      angular.forEach( teams, function( team ) {
        team.showAdmin = false;
        team.showWrite = false;
        team.showRead = false;
        team.showRepo = false;
        angular.forEach( team.repos, function( repo ) {
          repo.showAdmin = false;
          repo.showWrite = false;
          repo.showRead = false;
        });
        output.push( team );
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
