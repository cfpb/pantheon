couch_utils = require('./couch_utils')

module.exports = 
  auth_hack: (req, resp, next) ->
    if req.headers.cookie
      req.headers.cookie = req.headers.cookie.replace(/express_sess="(.*?)"/, 'express_sess=$1')
    next()
  couch: (req, resp, next) ->
    if not req.session.user
      return resp.status(401).end(JSON.stringify({error: "unauthorized", msg: "You are not logged in."}))

    req.couch = couch_utils.nano_user(req.session.user)
    next()