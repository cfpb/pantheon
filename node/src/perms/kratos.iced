kratos = (perms) ->
  is_kratos_admin = (user) ->
    return perms._is_resource_admin(user, 'kratos')

  perms.kratos =
    add_team: (user) ->
      return is_kratos_admin(user)

    remove_team: (user) ->
      return is_kratos_admin(user)

    add_team_member: (user, team, role) ->
      if role in ['admin', 'deploy']
        return is_kratos_admin(user)
      else
        return is_kratos_admin(user) or perms._is_team_admin(user, team)

    remove_team_member: (user, team, role) ->
      if role in ['admin', 'deploy']
        return is_kratos_admin(user)
      else
        return is_kratos_admin(user) or perms._is_team_admin(user, team)

    _is_kratos_admin: is_kratos_admin


if window?
  kratos(window.kratos.perms)
else if exports?
  module.exports = kratos
