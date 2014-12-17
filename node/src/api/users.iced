couch_utils = require('../couch_utils')
users = {}
user_db = couch_utils.nano_admin.use('_users')

isInt = (s) ->
  return String(parseInt(s)) == s

users.get_users = (req, resp) ->
  for resource, rsrcs_id of req.query
    break

  if resource
    if isInt(rsrcs_id)
      rsrcs_id = parseInt(rsrcs_id)
    user_db
      .viewWithList('base', 'by_resource_id', 'get_user', 
                    {include_docs: true, key: [resource, rsrcs_id]})
      .pipe(resp)
  else
    couch_utils.rewrite(user_db, 'base', '/users').pipe(resp)



users.remove_member = (req, resp) ->


module.exports = users