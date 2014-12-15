exports.views =
  by_type:
    map: (doc) ->
      team_data = require('views/lib/team_data').parse(doc._id)
      if (!team_data)
        return
      return emit([team_data.team, team_data.typ, team_data.name], 1)

exports.lists =
  get_docs: (header, req) ->
    out = []
    while(row = getRow())
      out.push(row.doc)
    return JSON.stringify(out)

exports.updates = 
  do_action: (team, req) ->
    _ = require('underscore')
    if not team
      return [null, '{"status": "error", "msg": "team not found"}']
    body = JSON.parse(req.body)
    action = body.action
    key = body.key
    value = body.value
    if action not in ['u+', 'u-', 'a+', 'a-']
      return [null, '{"status": "error", "msg": "invalid action"}']

    if action[0] == 'u'
      if not team.roles[key]
        team.roles[key] = []
      container = team.roles[key]
      item = value
    else
      if not team.rsrcs[key]
        team.rsrcs[key] = {}
      if not team.rsrcs[key].assets
        team.rsrcs[key].assets = []
      container = team.rsrcs[key].assets
      item = _.find(container, (item) -> item.id==value or String(item.id)==value)
    if action[1] == '+'
      if item in container
        return [null, JSON.stringify(team)]
      else
        container.push(value)
    else
      if item not in container
        return [null, JSON.stringify(team)]
      else
        i = container.indexOf(item)
        container.splice(i, 1)

    team.audit.push({
      u: req.userCtx.name,
      dt: +new Date(),
      a: action,
      k: key,
      v: value,
    })

    return [team, JSON.stringify(team)]

exports.rewrites = [
  # {
  #   from: "/teams",
  #   to: "/_list/teams/by_type",
  #   method: 'GET',
  #   query: {include_docs: 'true'},
  # },
]