perms = require('../../lib/perms/perms')
kratos = perms.kratos

team_admin   = {name: 'etkdg394hpmujn', roles: []}
user         = {name: 'thubsn24joa5gk', roles: []}
kratos_admin = {name: 'nahubk_hpb49km', roles: ['kratos|admin']}
both_admin   = {name: 'ahbksexortixvi', roles: ['kratos|admin']}

team         = {roles: {admin: ['etkdg394hpmujn', 'ahbksexortixvi']}}

describe 'add_team', () ->
  it 'allowed when user is a kratos admin', () ->
    actual = kratos.add_team(kratos_admin)
    expect(actual).toBe(true)
  it 'not allowed when user is not a kratos admin', () ->
    actual = kratos.add_team(user)
    expect(actual).toBe(false)

describe 'remove_team', () ->
  it 'allowed when user is a kratos admin', () ->
    actual = kratos.remove_team(kratos_admin)
    expect(actual).toBe(true)
  it 'not allowed when user is not a kratos admin', () ->
    actual = kratos.remove_team(user)
    expect(actual).toBe(false)

describe 'add_team_member', ->
  it 'allowed when user is a kratos admin', () ->
    actual = kratos.add_team_member(kratos_admin, team)
    expect(actual).toBe(true)

  it 'allowed when user is a team admin', () ->
    actual = kratos.add_team_member(team_admin, team)
    expect(actual).toBe(true)

  it 'not allowed when user is not a kratos admin or a team admin', () ->
    actual = kratos.add_team_member(user, team)
    expect(actual).toBe(false)

describe 'remove_team_member', ->
  it 'allowed when user is a kratos admin', () ->
    actual = kratos.remove_team_member(kratos_admin, team)
    expect(actual).toBe(true)

  it 'allowed when user is a team admin', () ->
    actual = kratos.remove_team_member(team_admin, team)
    expect(actual).toBe(true)

  it 'not allowed when user is not a kratos admin or a team admin', () ->
    actual = kratos.remove_team_member(user, team)
    expect(actual).toBe(false)
