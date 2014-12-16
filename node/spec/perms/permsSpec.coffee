perms = require('../../lib/perms/perms')

describe 'perms._has_resource_role', () ->
  it 'returns true if the user has the role for the resource', ->
    actual = perms._has_resource_role({roles: ['gh|user', 'kratos|admin']}, 'kratos', 'admin')
    expect(actual).toBe(true)

  it 'returns false if the user does not have the role for the resource', ->
    actual = perms._has_resource_role({roles: ['gh|user']}, 'kratos', 'admin')
    expect(actual).toBe(false)

describe 'perms._is_resource_admin', () ->
  it 'returns true if the user has is an admin for the resource', ->
    actual = perms._is_resource_admin({roles: ['gh|user', 'kratos|admin']}, 'kratos')
    expect(actual).toBe(true)

  it 'returns false if the user is not an admin for the resource', ->
    actual = perms._is_resource_admin({roles: ['gh|user']}, 'kratos')
    expect(actual).toBe(false)

describe 'perms._has_team_role', () ->
  it 'returns true if the user has the role for the team', ->
    actual = perms._has_team_role({name: 'etkdg394hpmujn', roles: []}, {roles: {admin: ['etkdg394hpmujn']}}, 'admin')
    expect(actual).toBe(true)

  it 'returns false if the user does not have the role for the team', ->
    actual = perms._has_team_role({name: 'etkdg394hpmujn', roles: []}, {roles: {admin: []}}, 'admin')
    expect(actual).toBe(false)

describe 'perms._is_team_admin', () ->
  it 'returns true if the user has the role for the team', ->
    actual = perms._is_team_admin({name: 'etkdg394hpmujn', roles: []}, {roles: {admin: ['etkdg394hpmujn']}})
    expect(actual).toBe(true)

  it 'returns false if the user does not have the role for the team', ->
    actual = perms._is_team_admin({name: 'etkdg394hpmujn', roles: []}, {roles: {admin: []}})
    expect(actual).toBe(false)
