/* ==========================================================================
   dev-dash

   # UserService service
   # TeamsCtrl controller
   # team directive
   # repobutton directive
   # userbutton directive
   # userlist directive
   # assetlist directive
   # role directive
   # expandable directive
   # username filter
   # removeUsers filter
   # toArray filter
   # prepTeamData filter
   # Cross Site Request Forgery protection
   ========================================================================== */

(function(){

  angular.module( 'OSWizardApp', [] );

  /* ==========================================================================
     # UserService service
     A single source for getting user data.
     ========================================================================== */

  angular.module('OSWizardApp').factory( 'UserService', function() {
    var user = { id: '', name: '' };
    var users = [];
    return {
      user: user,
      users: users,
      getByID: function( id ) {
        var requestedUser;
        angular.forEach( this.users, function( user ) {
          if ( user.name === id ) {
            requestedUser = user;
          }
        });
        return requestedUser;
      },
      getName: function( id ) {
        return this.getByID( id ).username;
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
    $scope.$watch(
      function() {
        return UserService.users;
      },
      function ( newValue ) {
        $scope.users = newValue;
      }
    );
    // Functions
    $scope.ready = function() {
      if ( $scope.user.id === '' ) {
        return false;
      }
      if ( $scope.user.name === '' ) {
        return false;
      }
      if ( $scope.users.length === 0 ) {
        return false;
      }
      if ( $scope.teams.length === 0 ) {
        return false;
      }
      return true;
    };
    // Data
    $http.get('/kratos/user/').
      success( function( response, status, headers, config ) {
        var preppedResponse = response;
        UserService.user.name = preppedResponse.username;
        UserService.user.id = preppedResponse.name;
        console.log( 'User\n', UserService.user.name, UserService.user.id );
      });
    $http.get('/kratos/users/').
      success( function( response, status, headers, config ) {
        UserService.users = response;
        // $scope.users = response;
        console.log('Users\n', UserService.users);
      });
    $http.get('/kratos/orgs/devdesign/teams/').
      success( function( response, status, headers, config ) {
        var preppedResponse = $filter('prepTeamData')( response );
        $scope.teams = preppedResponse;
        console.log('Teams\n', preppedResponse);
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
          $scope.teamModel.showMember = false;
          $scope.show = !show;
        };
      },
      templateUrl: '/static/templates/repobutton.html',
      link: function( scope, element, attrs ) {
        // Properties
        if ( scope.teamModel.rsrcs.gh && scope.teamModel.rsrcs.gh.assets ) {
          scope.repos = scope.teamModel.rsrcs.gh.assets;
        }
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
          $scope.teamModel.showMember = false;
          $scope.teamModel.showRepo = false;
          $scope.show = toggledShow;
        };
      },
      templateUrl: '/static/templates/userbutton.html',
      link: function( scope, element, attrs ) {
        // Properties
        scope.role = attrs.role;
        scope.users = scope.teamModel.roles[scope.role.toLowerCase()];
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
        <section userlist team-model="team" role="Admin"></section>
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
        scope.userIDs = scope.teamModel.roles[ scope.role.toLowerCase() ];
        scope.isTeamAdmin = UserService.isTeamAdmin( scope.teamModel.roles.admin );
        scope.editable = scope.isTeamAdmin && scope.role !== 'Admin';
        scope.users = [];
        scope.showAllUsers = false;
        angular.forEach( scope.userIDs, function( value, key ) {
          scope.users.push( UserService.getByID( value ) );
        });
        scope.requestURL = '/kratos/orgs/devdesign/teams/' + scope.teamModel.name +
                           '/roles/' + scope.role.toLowerCase() + '/';
        // Functions
        scope.updateUsers = function() {
          scope.allUsers = $filter('removeUsers')( scope.users );
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
          $.ajax({
            type: 'PUT',
            url: scope.requestURL + user.name
          })
          .done(function( msg ) {
            console.log( 'Data Saved:', msg );
            scope.$apply(function () {
              scope.users.push( user );
              scope.updateUsers();
            });
          })
          .error(function( msg ) {
            console.log( 'Error:', msg );
          });
        };
        scope.remove = function( user ) {
          $.ajax({
            type: 'DELETE',
            url: scope.requestURL + user.name
          })
          .done(function( msg ) {
            console.log( 'Data Saved:', msg );
            scope.$apply(function () {
              var index = scope.users.indexOf( user );
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
     # assetlist directive
     Creates a list of assets for a resource.

     heading: The heading to show above the list of assets, should be plural.

     Example:
        <div assetlist assets="[{name: 'Assets 1'}, {name: 'Assets 2'}]"
             heading="My assets">
        </div>
     ========================================================================== */

  angular.module('OSWizardApp').directive( 'assetlist', function() {
    return {
      restrict: 'A',
      scope: {
        teamModel: '=',
        heading: '='
      },
      templateUrl: '/static/templates/assetlist.html',
      link: function( scope, element, attrs ) {
        // Properties
        scope.heading = attrs.heading;
        if ( scope.teamModel.rsrcs.gh && scope.teamModel.rsrcs.gh.assets ) {
          scope.assets = scope.teamModel.rsrcs.gh.assets;
        } else {
          scope.assets = [];
        }
        scope.total = scope.assets.length;
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
        var roles = scope.teamModel.roles;
        scope.role = 'member';
        if ( roles.member ) {
          if ( roles.member.indexOf( UserService.user.id ) > -1 ) {
            scope.role = 'member';
          }
        }
        if ( roles.admin ) {
          if ( roles.admin.indexOf( UserService.user.id ) > -1 ) {
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
     # removeUsers filter
     Filter a user list for use in a userlist.
     ========================================================================== */
  angular.module('OSWizardApp').filter( 'removeUsers', function( UserService ) {
    return function( users ) {
      var filteredUsers = [];
      angular.forEach( UserService.users, function( user ) {
        if ( users.indexOf( user ) === -1 ) {
          filteredUsers.push( user );
        }
      });
      return filteredUsers;
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
        angular.forEach( team.roles, function( role ) {
          if ( role.indexOf( UserService.user.id ) > -1 ) {
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
        team.showMember = false;
        team.showRepo = false;
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

})();
