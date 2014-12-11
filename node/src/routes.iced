roles = require('./api/roles')
teams = require('./api/teams')

module.exports = (app) ->
    app.get('/kratos/teams/', teams.get_teams)
    app.get('/kratos/teams/:team_id', teams.get_team)
    app.put('/kratos/teams/:team_id', teams.update_team)


    app.put('/kratos/teams/:team_id/roles/:role/:userid/', roles.add_member)
    app.delete('/kratos/teams/:team_name/roles/:role/:userid/', roles.remove_member)
