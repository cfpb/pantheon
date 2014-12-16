// Generated by IcedCoffeeScript 1.8.0-c
(function() {
  var kratos;

  kratos = function(perms) {
    var is_kratos_admin;
    is_kratos_admin = function(user) {
      return perms._is_resource_admin(user, 'kratos');
    };
    return perms.kratos = {
      add_team: function(user) {
        return is_kratos_admin(user);
      },
      remove_team: function(user) {
        return is_kratos_admin(user);
      },
      add_team_member: function(user, team, role) {
        if (role === 'admin' || role === 'deploy') {
          return is_kratos_admin(user);
        } else {
          return is_kratos_admin(user) || perms._is_team_admin(user, team);
        }
      },
      remove_team_member: function(user, team, role) {
        if (role === 'admin' || role === 'deploy') {
          return is_kratos_admin(user);
        } else {
          return is_kratos_admin(user) || perms._is_team_admin(user, team);
        }
      },
      _is_kratos_admin: is_kratos_admin
    };
  };

  if (typeof window !== "undefined" && window !== null) {
    kratos(window.kratos.perms);
  } else if (typeof exports !== "undefined" && exports !== null) {
    module.exports = kratos;
  }

}).call(this);
