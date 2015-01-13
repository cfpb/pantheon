/* ==========================================================================
   dev-dash

   # UserService service
   # TeamsCtrl controller
   # team directive
   # assetbutton directive
   # userbutton directive
   # userlist directive
   # assetlist directive
   # role directive
   # expandable directive
   # username filter
   # removeUsers filter
   # toArray filter
   # prepUserData filter
   # prepUsersData filter
   # prepTeamData filter
   # Cross Site Request Forgery protection
   # Utility functions
   ========================================================================== */

(function(){

  window.kratosResponse = {
    user: '',
    users: [],
    teams: [],
    // You can use the log when adding/removing things.
    log: []
  };

  angular.module( 'OSWizardApp', [] );

  /* ==========================================================================
     # UserService service
     A single source for getting user data.
     ========================================================================== */

  angular.module('OSWizardApp').factory( 'UserService', function() {
    // The logged in user
    var user = { id: '', name: '', parsedRoles: [], isGHUser: true };
    // All users of dash
    var users = [];
    return {
      user: user,
      users: users,
      // Logged in user functions
      isTeamAdmin: function( permissions ) {
        if ( typeof permissions !== 'undefined' ) {
          return permissions.indexOf( this.user.id ) > -1;
        } else {
          return false;
        }
      },
      // Functions for all users of dash
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
        return this.getByID( id ).data.username;
      },
      // Generic user and users functions
      parseRole: function( role ) {
        return { resource: role.split('|')[0], role: role.split('|')[1] };
      }
    };
  });

  /* ==========================================================================
     # TeamsCtrl controller
     The main controller. All it really does is grabs a JSON file, filters it
     and sets two main properties used throughout the app.
     ========================================================================== */

  angular.module('OSWizardApp').controller( 'TeamsCtrl', function( $scope, $http, $filter, $element, $timeout, UserService ) {
    // Properties
    $scope.loggedIn = true;
    $scope.user = UserService.user;
    $scope.users = UserService.users;
    $scope.teams = [];
    $scope.waiting = false;
    $scope.confirmMessage = {
      show: false
    };
    $scope.requestURL = '/kratos/orgs/devdesign/teams/';
    // Watchers
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
      $scope.initDataDependantProps();
      return true;
    };
    $scope.initDataDependantProps = function() {
      // Set some properties once we have all the data we need
      $scope.canAdd = getObj( $scope.user, [ 'perms', 'team', 'add' ] );
      $scope.canRemove = getObj( $scope.user, [ 'perms', 'team', 'remove' ] );
      $scope.editable = $scope.canAdd && $scope.canRemove;
    };
    $scope.testStatus = function( status ) {
      if ( status === 401 ) {
        $scope.loggedIn = false;
      } else {
        $scope.loggedIn = true;
      }
    };
    $scope.add = function( name ) {
      $scope.waiting = true;
      $.ajax({
        type: 'PUT',
        url: $scope.requestURL + name,
        contentType: 'application/json'
      })
      .done(function( msg ) {
        window.kratosResponse.log.push({ done: angular.fromJson(msg) });
        $scope.$apply(function () {
          $element.find('#add-team .slats-type_input').val('');
          $scope.teams.push( $filter('prepTeamData')( [msg] )[0] );
          $scope.waiting = false;
          $scope.confirmMessage.show = true;
          $scope.confirmMessage.message = 'Added';
          $scope.confirmMessage.teamName = msg.name;
          $scope.confirmMessage.supplement = 'You will find it in the "Other teams" section.';
          $timeout( function() {
            $scope.confirmMessage.show = false;
          }, 4000);
        });
      })
      .error(function( msg ) {
        window.kratosResponse.log.push({ error: angular.fromJson(msg) });
        $scope.$apply(function () {
          $scope.waiting = false;
          $scope.confirmMessage.show = true;
          $scope.confirmMessage.message = 'There was a problem adding';
          $scope.confirmMessage.teamName = msg.name;
          $timeout( function() {
            $scope.confirmMessage.show = false;
          }, 4000);
        });
      });
    };
    $scope.remove = function( teamToRemove ) {
      var assetObj, index;
      angular.forEach( $scope.assets, function( asset ) {
        if ( asset.name === teamToRemove.name || asset.new === teamToRemove.name ) {
          assetObj = asset;
        }
      });
      index = $scope.assets.indexOf( assetObj );
      $.ajax({
        type: 'DELETE',
        url: $scope.requestURL + assetObj.id
      })
      .done(function( msg ) {
        window.kratosResponse.log.push({ done: angular.fromJson(msg) });
        $scope.$apply(function () {
          $scope.assets.splice( index, 1 );
          $scope.updateAssets();
        });
      })
      .error(function( msg ) {
        window.kratosResponse.log.push({ error: angular.fromJson(msg) });
      });
    };
    // Data
    $http.get('/kratos/user/')
      .success( function( response, status, headers, config ) {
        var preppedResponse = $filter('prepUserData')( response );
        angular.copy( preppedResponse, UserService.user );
        window.kratosResponse.user = UserService.user;
      })
      .error( function( response, status ) {
        $scope.testStatus( status );
      });
    $http.get('/kratos/users/')
      .success( function( response, status, headers, config ) {
        var preppedResponse = $filter('prepUsersData')( response );
        angular.copy( preppedResponse, UserService.users );
        window.kratosResponse.users = UserService.users;
      })
      .error( function( response, status ) {
        $scope.testStatus( status );
      });
    $http.get('/kratos/orgs/devdesign/teams/')
      .success( function( response, status, headers, config ) {
        var preppedResponse = $filter('prepTeamData')( response );
        $scope.teams = preppedResponse;
        window.kratosResponse.teams = preppedResponse;
      })
      .error( function( response, status ) {
        $scope.testStatus( status );
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
      templateUrl: '/static/templates/team.html',
      link: function( scope, element, attrs ) {
        // Events
        scope.$on( 'userlistUpdated', function( event, data ) {
          scope.$broadcast( data.role.toLowerCase() + 'UserlistUpdated', data.users );
        });
        scope.$on( 'assetlistUpdated', function( event, data ) {
          scope.$broadcast( data.type.toLowerCase() + 'AssetlistUpdated', data.assets );
        });
      }
    };
  });

  /* ==========================================================================
     # assetbutton directive
     Creates a button to toggle a list of assets on and off.

     team-model: A reference to a team model.

     Example:
        <assetbutton team-model="team"></assetbutton>
     ========================================================================== */

  angular.module('OSWizardApp').directive( 'assetbutton', function() {
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
      templateUrl: '/static/templates/assetbutton.html',
      link: function( scope, element, attrs ) {
        // Properties
        scope.heading = attrs.heading;
        scope.assets = getObj( scope.teamModel.rsrcs, [ 'gh', 'assets' ] );
        if ( typeof scope.assets === 'undefined' ) {
          scope.total = 0;
        } else {
          scope.total = scope.assets.length;
        }
        // Events
        element.on( 'click', function() {
          if ( scope.show ) {
            element.parents('.expandable')[0].expand();
          } else {
            element.parents('.expandable')[0].collapse();
          }
        });
        scope.$on( scope.heading.toLowerCase() + 'AssetlistUpdated', function( event, data ) {
          scope.total = data.length;
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

     TODO: Merge with assetbutton since they do almost the exact same thing.
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
        scope.users = getObj( scope.teamModel.roles, [ scope.role.toLowerCase(), 'members' ] );
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
        scope.$on( scope.role.toLowerCase() + 'UserlistUpdated', function( event, data ) {
          scope.total = data.length;
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
        scope.listFilter = '';
        scope.role = attrs.role;
        scope.canAdd = getObj( scope.teamModel.roles, [ scope.role.toLowerCase(), 'perms', 'add' ] );
        scope.canRemove = getObj( scope.teamModel.roles, [ scope.role.toLowerCase(), 'perms', 'remove' ] );
        scope.editable = scope.canAdd && scope.canRemove;
        scope.userIDs = getObj( scope.teamModel.roles, [ scope.role.toLowerCase(), 'members' ] );
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
          angular.forEach( scope.allUsers, function( user ) {
            user.showConfirmRemove = false;
          });
          if ( typeof scope.users === 'undefined' ) {
            scope.total = 0;
          } else {
            scope.total = scope.users.length;
          }
          // Emit an event that the userlist has been updated. Send the role along with the list of users so
          // that we can match up which userbutton button to update.
          scope.$emit( 'userlistUpdated', { role: scope.role, users: scope.users } );
        };
        scope.inUserList = function( user ) {
          return scope.users.indexOf( user ) > -1;
        };
        scope.confirmRemove = function( user ) {
          user.showConfirmRemove = true;
        };
        scope.abortRemove = function( user ) {
          user.showConfirmRemove = false;
        };
        scope.add = function( user ) {
          $.ajax({
            type: 'PUT',
            url: scope.requestURL + user.name
          })
          .done(function( msg ) {
            window.kratosResponse.log.push({ done: angular.fromJson(msg) });
            scope.$apply(function () {
              scope.users.push( user );
              scope.updateUsers();
            });
          })
          .error(function( msg ) {
            window.kratosResponse.log.push({ error: angular.fromJson(msg) });
          });
        };
        scope.remove = function( user ) {
          $.ajax({
            type: 'DELETE',
            url: scope.requestURL + user.name
          })
          .done(function( msg ) {
            window.kratosResponse.log.push({ done: angular.fromJson(msg) });
            scope.$apply(function () {
              var index = scope.users.indexOf( user );
              scope.users.splice( index, 1 );
              scope.updateUsers();
            });
          })
          .error(function( msg ) {
            window.kratosResponse.log.push({ error: angular.fromJson(msg) });
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

     heading: The heading to show above the list of assets, should be unique.

     Example:
        <div assetlist assets="[{name: 'Assets 1'}, {name: 'Assets 2'}]"
             heading="My assets">
        </div>
     ========================================================================== */

  angular.module('OSWizardApp').directive( 'assetlist', function( $filter, $timeout, UserService ) {
    return {
      restrict: 'A',
      scope: {
        teamModel: '=',
        heading: '='
      },
      templateUrl: '/static/templates/assetlist.html',
      link: function( scope, element, attrs ) {
        // Properties
        scope.canAdd = getObj( scope.teamModel.rsrcs, [ 'gh', 'perms', 'add' ] );
        scope.canRemove = getObj( scope.teamModel.rsrcs, [ 'gh', 'perms', 'remove' ] );
        scope.editable = scope.canAdd && scope.canRemove;
        scope.heading = attrs.heading;
        scope.assets = [];
        scope.assets = getObj( scope.teamModel.rsrcs, [ 'gh', 'assets' ] );
        angular.forEach( scope.assets, function( asset ) {
          if ( asset.new ) {
            asset.name = asset.new;
          }
        });
        scope.assets = $filter( 'orderBy' )( scope.assets, 'name' );
        scope.total = getObj( scope, [ 'assets', 'length' ] ) || 0;
        scope.waiting = false;
        scope.confirmMessage = {
          show: false
        };
        scope.requestURL = '/kratos/orgs/devdesign/teams/' + scope.teamModel.name +
                           '/resources/' + 'gh' + '/';
        scope.updateAssets = function() {
          scope.total = getObj( scope, [ 'assets', 'length' ] ) || 0;
          angular.forEach( scope.assets, function( asset ) {
            asset.showConfirmRemove = false;
          });
          // Emit an event that the assetlist has been updated.
          scope.$emit( 'assetlistUpdated', { type: scope.heading, assets: scope.assets } );
        };
        scope.confirmRemove = function( asset ) {
          asset.showConfirmRemove = true;
        };
        scope.abortRemove = function( asset ) {
          asset.showConfirmRemove = false;
        };
        scope.add = function( name ) {
          var data = { new: name };
          scope.waiting = true;
          $.ajax({
            type: 'POST',
            url: scope.requestURL,
            data: JSON.stringify( data ),
            contentType: 'application/json'
          })
          .done(function( msg ) {
            window.kratosResponse.log.push({ done: angular.fromJson(msg) });
            scope.$apply(function () {
              data.name = data.new;
              scope.assets.unshift( data );
              scope.updateAssets();
              element.find('.slats-type_input').val('');
              scope.waiting = false;
              scope.confirmMessage.show = true;
              scope.confirmMessage.message = 'Added';
              scope.confirmMessage.assetName = data.name;
              $timeout( function() {
                scope.confirmMessage.show = false;
              }, 4000);
            });
          })
          .error(function( msg ) {
            window.kratosResponse.log.push({ error: angular.fromJson(msg) });
            scope.$apply(function () {
              scope.waiting = false;
              scope.confirmMessage.show = true;
              scope.confirmMessage.message = 'There was a problem adding';
              scope.confirmMessage.assetName = data.name;
              $timeout( function() {
                scope.confirmMessage.show = false;
              }, 4000);
            });
          });
        };
        scope.remove = function( assetToRemove ) {
          var assetObj, index;
          angular.forEach( scope.assets, function( asset ) {
            if ( asset.name === assetToRemove.name || asset.new === assetToRemove.name ) {
              assetObj = asset;
            }
          });
          index = scope.assets.indexOf( assetObj );
          $.ajax({
            type: 'DELETE',
            url: scope.requestURL + assetObj.id
          })
          .done(function( msg ) {
            window.kratosResponse.log.push({ done: angular.fromJson(msg) });
            scope.$apply(function () {
              scope.assets.splice( index, 1 );
              scope.updateAssets();
            });
          })
          .error(function( msg ) {
            window.kratosResponse.log.push({ error: angular.fromJson(msg) });
          });
        };
        scope.updateAssets();
      }
    };
  });

  /* ==========================================================================
     # role directive
     Creates a label identifying the current users permission for a given team.

     team-model: A reference to a team model.

     Example:
        <role teamModel="team"></role>

     TODO: Rename this to "teamrole".
     ========================================================================== */

  angular.module('OSWizardApp').directive( 'role', function( $filter, UserService ) {
    return {
      restrict: 'E',
      scope: {
        teamModel: '=',
        username: '='
      },
      templateUrl: '/static/templates/role.html',
      link: function( scope, element, attrs ) {
        // Properties
        scope.roles = [];
        angular.forEach( scope.teamModel.roles, function( role, key ) {
          var members = getObj( role, [ 'members' ] ) || [];
          if ( members.indexOf( UserService.user.id ) > -1 ) {
            scope.roles.push( key );
          }
        });
        scope.roles = $filter('orderBy')( scope.roles );
        element.addClass('corner-badge corner-badge__user');
        element.append( '<span class="corner-badge_label">' + scope.roles.join(', ') + '</span>' );
        // Color this green if the role contains 'admin'.
        if ( scope.roles.indexOf( 'admin' ) !== -1 ) {
          element.addClass('corner-badge__bg-green');
        }
        // Hide this if the role is empty.
        if ( scope.roles.length === 0 ) {
          element.addClass('corner-badge__hide');
        }
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
          var members = getObj( role, [ 'members' ] ) || [];
          if ( members.indexOf( UserService.user.id ) > -1 ) {
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
     # prepUserData filter
     Tweak some properties to the user data before using it.
     ========================================================================== */
  angular.module('OSWizardApp').filter( 'prepUserData', function( UserService ) {
    return function( user ) {
      var output = { id: user.name, name: user.data.username, parsedRoles: [], isGHUser: true, perms: {} };
      var isGHUser = false;
      angular.forEach( user.roles, function( role ) {
        output.parsedRoles.push( UserService.parseRole( role ) );
      });
      angular.forEach( output.roles, function( role ) {
        if ( role.resource === 'gh' ) {
          isGHUser = true;
        }
      });
      output.isGHUser = isGHUser;
      output.perms = user.perms;
      return output;
    };
  });

  /* ==========================================================================
     # prepUsersData filter
     Tweak some properties to the users data before using it.
     ========================================================================== */
  angular.module('OSWizardApp').filter( 'prepUsersData', function( UserService ) {
    return function( users ) {
      var output = [];
      angular.forEach( users, function( user ) {
        user.parsedRoles = [];
        angular.forEach( user.roles, function( role ) {
          user.parsedRoles.push( UserService.parseRole( role ) );
        });
        output.push( user );
      });
      return output;
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

  /* ==========================================================================
     # Utility functions
     ========================================================================== */
  var getObj = function(obj, path) {
      var key = path.shift();
      obj = obj[key];
      if (!obj) { return obj; }
      if (path.length) {
          return getObj(obj, path);
      } else {
          return obj;
      }
  };

})();
