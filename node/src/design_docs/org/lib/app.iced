_ = require('lib/underscore')
h = require('lib/helpers')
validation = require('lib/validation')

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
  get_teams: (header, req) ->
    out = []
    while(row = getRow())
      doc = row.doc
      continue if not validation.is_team(doc)
      team = h.add_team_perms(doc, req.userCtx)
      out.push(team)
    return JSON.stringify(out)

exports.shows =
  get_team: (doc, req) ->
    team = h.add_team_perms(doc, req.userCtx)
    return {body: JSON.stringify(team), "headers" : {"Content-Type" : "application/json"}}

exports.validate_doc_update = (newDoc, oldDoc, userCtx, secObj) ->
  validation.validate_doc_update(newDoc, oldDoc, userCtx, secObj)

exports.updates =
  do_action: (team, req) ->
    if not team
      return [null, '{"status": "error", "msg": "team not found"}']
    body = JSON.parse(req.body)
    value = body.value
    action = body.action
    key = body.key
    if action == 'u+'
      container = h.mk_objs(team.roles, [key], [])
      if value in container
        return [null, JSON.stringify(team)]
      else
        container.push(value)

    else if action == 'u-'
      container = h.mk_objs(team.roles, [key], [])
      if value not in container
        return [null, JSON.stringify(team)]
      else
        i = container.indexOf(value)
        container.splice(i, 1)

    else if action == 'a+'
      container = h.mk_objs(team.rsrcs, [key, 'assets'], [])
      item = _.find(container, (item) -> (item.id and (item.id==value.id or String(item.id)==value.id)) or (item.new and item.new==value.new))
      if item
        return [null, JSON.stringify(team)]
      else
        container.push(value)

    else if action == 'a-'
      container = h.mk_objs(team.rsrcs, [key, 'assets'], [])
      item = _.find(container, (item) -> item.id==value or String(item.id)==value)
      if not item
        return [null, JSON.stringify(team)]
      else
        i = container.indexOf(item)
        container.splice(i, 1)

    else
      return [null, '{"status": "error", "msg": "invalid action"}']
    team.audit.push({
      u: req.userCtx.name,
      dt: +new Date(),
      a: action,
      k: key,
      v: value,
      id: body.uuid,
    })
    return [team, JSON.stringify(team)]

exports.rewrites = [
    {
      from: "/teams",
      to: "/_list/get_teams/by_type",
      method: 'GET',
      query: {include_docs: 'true'},
    },
    {
      from: "/teams/:team_id",
      to: "/_show/get_team/:team_id",
      query: {},
    }
]
