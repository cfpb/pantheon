couch_utils = require('../couch_utils')
request = require('request')

teams = {}

teams.update_team = (req, resp) ->
  
teams.get_team = (req, resp) ->

teams.get_teams = (req, resp, org) ->
  req.session.hello = 'world'
  couch_utils.nano.request({
    db: 'org_devdesign',
    path: '/_design/base/_rewrite/teams'
  }).pipe(resp)

module.exports = teams
