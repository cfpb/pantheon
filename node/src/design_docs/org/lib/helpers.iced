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
