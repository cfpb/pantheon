teams = require('./api/teams')
users = require('./api/users')

module.exports = (app) ->
    app.get('/kratos/org/:org_id/teams/', teams.get_teams)
    app.get('/kratos/org/:org_id/teams/:team_id', teams.get_team)
    app.put('/kratos/org/:org_id/teams/:team_id', teams.update_team)

    app.get('/kratos/users', users.get_users)

    # add user to team - no body
    app.put('/kratos/org/:org_id/teams/:team_id/roles/:key/:value/', teams.add_remove_member_asset('u+'))
    # remove user from team - no body
    app.delete('/kratos/org/:org_id/teams/:team_id/roles/:key/:value/', teams.add_remove_member_asset('u-'))
    # add asset to team - content_type=application/json; {new: <string>}
    app.post('/kratos/org/:org_id/teams/:team_id/resources/:key/', teams.add_asset)
    # remove asset from team - no body
    app.delete('/kratos/org/:org_id/teams/:team_id/resources/:key/:value/', teams.add_remove_member_asset('a-'))
