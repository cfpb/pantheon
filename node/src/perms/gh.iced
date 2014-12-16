gh = (perms) ->
  is_gh_team_admin = (user, team) ->
    return perms._has_resource_role(user, 'gh', 'user') and
           perms._is_team_admin(user, team)

  perms.gh =
    add_team_asset: (user, team) ->
      return perms.kratos._is_kratos_admin(user) or 
                   is_gh_team_admin(user, team)

    remove_team_asset: (user, team) ->
      return perms.kratos._is_kratos_admin(user) or 
                   is_gh_team_admin(user, team)

    _is_gh_team_admin: is_gh_team_admin

if window?
  gh(window.kratos.perms)
else if exports?
  module.exports = gh
