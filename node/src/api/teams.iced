couch_utils = require('../couch_utils')
request = require('request')
uuid = require('node-uuid')

teams = {}

teams.update_team = (req, resp) ->
  
teams.get_team = (req, resp) ->
  org = 'org_' + req.params.org_id
  team = 'team_' + req.params.team_id
  couch_utils.nano_admin.use(org).get(team).pipe(resp)

teams.get_teams = (req, resp) ->
  org = 'org_' + req.params.org_id
  couch_utils.nano_admin.use(org).viewWithList('base', 'by_type', 'get_docs', {include_docs: true}).pipe(resp)

teams.add_remove_member_asset = (action_type) ->
  (req, resp) ->
    org = 'org_' + req.params.org_id
    team = 'team_' + req.params.team_id

    db = req.couch.use(org)
    action = {
      action: action_type
      key: req.params.key
      value: req.params.value
      uuid: uuid.v4()
    }
    db.atomic('base', 'do_action', team, action).pipe(resp)

teams.add_asset = (req, resp) ->
  new_val = req.body.new
  if not new_val
    return resp.status(400).end(JSON.stringify({'status': 'error', 'msg': 'new value must be present'}))
  req.params.value = {id: uuid.v4(), 'new': new_val}
  console.log(req.body, req.params.value)
  return teams.add_remove_member_asset('a+')(req, resp)

module.exports = teams
