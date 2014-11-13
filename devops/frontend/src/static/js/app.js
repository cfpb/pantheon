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

    // Functions
    $scope.toggleUserType = function( anything ) {
      console.log('toggle', anything);
      // var key = '';
      // switch ( type ) {
      //   case 'admin': key = 'showAdmins';  break;
      //   case 'read':  key = 'showReaders'; break;
      //   case 'write': key = 'showWriters'; break;
      //   default:      key = 'showReaders';
      // }
      // group[ key ] = !group[ key ];
    };

  });

  angular.module('OSWizardApp').directive( 'users', function() {
    return {
      restrict: 'E',
      template: '{{ group }}',
      scope: {
        group: '=',
        toggle: '&'
      },
      /*jshint multistr: true */
      template: '\
        <ul class="group-content_list">\
            <li>\
                <button class="btn btn__link">\
                    {{ role }} ({{ total }})\
                </button>\
            </li>\
            <li ng-show="group.showAdmins"\
                ng-repeat="user in users"\
                class="group-content_list-item">\
                {{ user.name }}\
            </li>\
        </ul>',
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
        element.find('.btn').on( 'click', function() {
          scope.toggle( scope.group, scope.role );
        });
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

