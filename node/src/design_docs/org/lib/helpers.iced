auth = require('./auth/auth')

module.exports =
  make_audit_trail: (team, req, key, value) ->
    return {
      u: req.userCtx.name,
      dt: +new Date(),
      a: action,
      k: key,
      v: value,
    }
  mk_objs: (obj, path_array, val={}) ->
    ###
    make a set of nested object.

    mk_objs({'x': 1}, ['a', 'b'], [])
    # returns {'x': 1, 'a': {'b': []}}

    return the val
    ###
    last_key = path_array.pop()
    for key in path_array
      if not obj[key]?
        obj[key] = {}
      obj = obj[key]
    if not obj[last_key]
      obj[last_key] = val
    return obj[last_key]
  add_team_perms: (original_team, user) ->
    team = JSON.parse(JSON.stringify(original_team))
    for rsrc_name, rsrc of team.rsrcs
      rsrc_auth = auth[rsrc_name]
      rsrc.perms = {
        add: rsrc_auth.add_team_asset(user, team)
        remove: rsrc_auth.remove_team_asset(user, team)
      }
    for role_name, role of team.roles
      role.perms = {
        add: auth.kratos.add_team_member(user, team, role_name)
        remove: auth.kratos.remove_team_member(user, team, role_name)
      }
    return team