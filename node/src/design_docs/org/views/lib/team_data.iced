exports.parse = (_id) ->
  id_parts = _id.split('_')
  typ = id_parts[0]
  team = id_parts.slice(1)

  if (typ == 'team')
    return {team: team.join('_'), typ: typ}
  else if (['role', 'rsrc'].indexOf(typ) == -1)
    return null
  else
    name = team[0]
    team = team.slice(1)
    return {
      team: team.join('_'),
      typ: typ,
      name: name,
    }
