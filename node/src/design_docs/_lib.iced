module.exports = 
  get_team_data: (_id) ->
    id_parts = _id.split('_')
    if id_parts[0] != 't'
      return null
    name = id_parts.pop()
    typ = id_parts.pop()
    team = id_parts.slice(1)
    return {team: team.join('_'), typ: typ, name: name}
