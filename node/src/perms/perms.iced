perms = {}
perms._has_resource_role = (user, resource, role) ->
  return (resource + '|' + role) in user.roles
perms._has_team_role = (user, team, role) ->
  user_id = user.name
  return user_id in (team.roles[role] or [])
perms._is_resource_admin = (user, resource) ->
  return perms._has_resource_role(user, resource, 'admin')
perms._is_team_admin = (user, team) ->
  return perms._has_team_role(user, team, 'admin')

perms.roles = 
  team: [
    'admin',
    'member',
  ],
  resource: {
    kratos: ['admin'],
    gh: ['user'],
  }
if window?
  window.kratos = {perms: perms}
else if exports?
  require('./kratos')(perms)
  require('./gh')(perms)
  module.exports = perms
