couch_utils = require('./couch_utils')

module.exports = 
  auth_hack: (req, res, next) ->
    if req.headers.cookie
      req.headers.cookie = req.headers.cookie.replace(/express_sess="(.*?)"/, 'express_sess=$1')
    next()
  couch: (req, res, next) ->
    if req.session.user
      req.couch = couch_utils.nano_user(req.session.user)
    next()