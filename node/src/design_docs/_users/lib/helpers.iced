h = {}
h.sanitize_user = (user) ->
  delete user.password_scheme
  delete user.iterations
  delete user.derived_key
  delete user.salt
  return user

module.exports = h
