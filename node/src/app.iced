conf = require('./config')

express = require('express')
bodyParser = require('body-parser')
session = require('cookie-session')
routes = require('./routes')
# cookieParser = require('cookie-parser')
#  , "cookie-parser": "1.3.3"
# serveStatic = require('serve-static')
#  , "serve-static": "1.7.1"



app = express()
app.use(bodyParser.json())
app.use(session(secret: conf.SECRET_KEY))
routes(app)


server = app.listen(5000, () ->
  host = server.address().address
  port = server.address().port
  console.log('app listening at http://%s:%s', host, port)
)
