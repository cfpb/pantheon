(perms) ->
  perms.kratos =
    add_team: (user) ->
      return user.resrcs.kratos?.roles?.admin or false
    remove_team: (user) ->
      return user.resrcs.kratos?.roles?.admin or false
    # add_team_member: (user, team) ->
    #   user_id = user.name
    #   return team.roles.admin?
