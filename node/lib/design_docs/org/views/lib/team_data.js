exports.parse = function(_id) {
  var id_parts, name, team, typ;
  id_parts = _id.split('_');
  if (id_parts[0] !== 't') {
    return null;
  }
  name = id_parts.pop();
  typ = id_parts.pop();
  team = id_parts.slice(1);
  return {
    team: team.join('_'),
    typ: typ,
    name: name
  };
};