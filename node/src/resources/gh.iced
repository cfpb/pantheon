conf = require('../config')
gh_conf = conf.RESOURCES.GH
request = require('request')
parse_links = require('parse-links')
couch_utils = require('../couch_utils')
_ = require('underscore')
uuid = require('node-uuid')

gha_url = 'https://api.github.com'
gha = request.defaults(
  auth: gh_conf.ADMIN_CREDENTIALS
  json: true
  headers:
    'User-Agent': 'cfpb-kratos'
)

get_all = (client, url, callback) ->
  out = []
  while url
    await client.get(url, defer(err, resp, data))
    return err if err
    out = out.concat(data)
    link_header = resp.headers.link
    links = parse_links(link_header) if link_header?
    url = links?.next or null
  return callback(null, out)

x = {}

x.import_users = (callback) ->
  url = gha_url + '/organizations/' + gh_conf.ORG_ID + '/members'
  await get_all(gha, url, defer(err, members))
  users = []
  await couch_utils.get_uuids(members.length, defer(err, uuids))

  for member, i in members
    users.push({
      _id: "org.couchdb.user:" + uuids[i],
      type: "user",
      name: uuids[i],
      roles: [],
      username: member.login,
      resrcs: {
        gh: {
          roles: {user: false},
          data: {
            login: member.login
            id: member.id
          }
        }
      }
    })
  db = couch_utils.nano.use('_users')
  return db.bulk({docs: users}, callback)

x.import_teams = (db_name, admin_id, callback) ->
  start_time = +new Date()
  url = gha_url + '/organizations/' + gh_conf.ORG_ID + '/teams'
  await get_all(gha, url, defer(err, raw_teams))
  teams = {}
  for raw_team in raw_teams
    if raw_team.id in gh_conf.UNMANAGED_TEAMS
      console.log('skipping', raw_team.id)
      continue
    [name, typ, perm] = raw_team.name.split(' ')
    raw_team.perm = perm
    raw_team.iname = name # internal name
    if typ != 'team'
      continue
    if not teams[name]?
      teams[name] = {}
    teams[name][perm] = raw_team
  team_data = []
  await
    i = 0
    for team_name, team of teams
      import_team(team, admin_id, defer(err, team_data[i]))
      i++
  team_docs = {docs: _.flatten(team_data, true)}
  db = couch_utils.nano.use('org_' + db_name)
  await couch_utils.ensure_db(db, 'bulk', team_docs, defer(err, resp))
  console.log('total time:', +new Date() - start_time)
  return callback()

import_team = (teams, admin_id, callback) ->
  await
    import_repos(teams['admin'], admin_id, defer(err, rsrc_doc))
    i = 0
    import_members(teams, admin_id, defer(err, role_doc))
  return callback(null, [role_doc, rsrc_doc])

import_members = (teams, admin_id, callback) ->
  now = +new Date()
  role_doc = {
    _id: 't_' + teams['admin'].iname + '_role_member',
    members: [],
    audit: [{u: admin_id, dt: now, a: '+', id: uuid.v4()}],
    enforce: [],
    rsrcs_data: {
      gh: _.object(_.map(teams, (item) -> [item.perm, item.id]))
    },
  }

  members = []
  await
    i = 0
    for team_name, team of teams
      url = team.url + '/members'
      get_all(gha, url, defer(err, members[i]))
      i++
  members = _.flatten(members, true)
  members = _.map(members, (item) -> item.id)
  members = _.uniq(members)
  member_gh_ids = _.map(members, (item) -> ['gh', item])
  await couch_utils.nano.use('_users').view('base', 'by_resource_id', {keys: member_gh_ids}, defer(err, user_rows))

  for user in user_rows.rows
    role_doc.members.push(user.value)
    role_doc.audit.push({u: admin_id, dt: now, a: 'c', r: user.value, id: uuid.v4()})
  return callback(null, role_doc)

import_repos = (team, admin_id, callback) ->
  now = +new Date()
  resource_doc = {
    _id: 't_' + team.iname + '_rsrc_gh',
    assets: [],
    audit: [{u: admin_id, dt: now, a: '+', id: uuid.v4()}],
    enforce: [],
  }

  url = team.url + '/repos'
  await get_all(gha, url, defer(err, repos))

  for repo in repos
    repo_record = {id: repo.id, name: repo.name, full_name: repo.full_name}
    resource_doc.assets.push(repo_record)
    resource_doc.audit.push({u: admin_id, dt: now, a: 'c', r: repo_record, id: uuid.v4()})
  return callback(null, resource_doc)
module.exports = x

###
gh = require('./gh')
gh.import_teams('devdesign', 'c0301d9be96094b552835c014f01cf07', function(err, resp) {console.log(err, resp)})
gh.import_all(function(err, resp) {console.log(err, resp)})
###
    # "51": {
    #   "username": "poorgeek",
    #   resrcs: {
    #     'kratos': {"roles": {"admin": true}},
    #     'gh': {"roles": {"user": false}}
    #   }
    # },