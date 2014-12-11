_ = require('underscore')
config_secret = require('./config_secret')

config = 
  COUCHDB:
    HOST: 'http://localhost'
    PORT: 5984
  SESSION_KEYS: ['notasecret1', 'notasecret2']

_.extend(config, config_secret)

module.exports = config
