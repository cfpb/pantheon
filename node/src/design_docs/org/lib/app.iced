exports.views =
  by_type:
    map: (doc) ->
      team_data = require('views/lib/team_data').parse(doc._id)
      if (!team_data)
        return
      return emit([team_data.team, team_data.typ, team_data.name], 1)

exports.lists =
  teams: (head, req) ->
    data = {}
    while (row = getRow())
      doc = row.doc
      team_data = require('views/lib/team_data').parse(doc._id)
      if (!team_data)
        continue
      if (!data[team_data.team])
        data[team_data.team] = {
          roles: {},
          rsrcs: {},
        }
      if (team_data.typ == 'team')
        doc.roles = data[team_data.team].roles
        doc.rsrcs = data[team_data.team].rsrcs
        data[team_data.team] = doc
      else
        delete doc.audit
        delete doc.enforce
        data[team_data.team][team_data.typ + 's'][team_data.name] = doc
    out = []
    for k, v of data
      out.push(v)
    return JSON.stringify(out)
  team: (head, req) ->
    return ''

exports.rewrites = [
  {
    from: "/teams",
    to: "/_list/teams/by_type",
    method: 'GET',
    query: {include_docs: 'true'},
  },
]