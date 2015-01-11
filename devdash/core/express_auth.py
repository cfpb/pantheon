import hmac as Hmac
import hashlib
import base64
from django.conf import settings
from django.utils import crypto
from django.core import signing
import json
def get_express_session(req, cookie_name='express_sess'):
    """
    get the Express.js session dict. 

    default session cookie name of express:sess does now work with django.
    """
    key = settings.SECRET_KEY
    cookie_value = req.COOKIES.get(cookie_name)
    cookie_sig = req.COOKIES.get(cookie_name + '.sig')
    if not cookie_value or not cookie_sig:
        return {}

    cookie = cookie_name + '=' + cookie_value
    hmac = Hmac.new(key, cookie, hashlib.sha1)
    digest = signing.b64_encode(hmac.digest())
    valid_sig = crypto.constant_time_compare(digest, cookie_sig)
    if not valid_sig:
        return {}

    try:
        json_data = signing.b64_decode(cookie_value)
        session = json.loads(json_data)
    except:
        return {}
    return session

def set_express_session(resp, session_dict, cookie_name='express_sess'):
    """
    Set express session cookie that express can parse.

    nearly got it. but django adds quotes around the cookie value. will have to fix in express.
    """
    key = settings.SECRET_KEY
    cookie_value = base64.b64encode(unicode(json.dumps(session_dict, separators=(',', ':'))))
    cookie = cookie_name + '=' + cookie_value

    hmac = Hmac.new(key, cookie, hashlib.sha1)
    cookie_sig =  signing.b64_encode(hmac.digest())
    resp.set_cookie(cookie_name, value=cookie_value, max_age=None, expires=None, secure=None, httponly=True)
    resp.set_cookie(cookie_name + '.sig', value=cookie_sig, max_age=None, expires=None, secure=None, httponly=True)



class SetExpressAuthentication(object):
    """
    check to see if the user is logged and has a linked kratos account
    if so, log them into kratos, otherwise ensure the kratos session is
    not logged in.
    """
    def process_response(self, req, resp):
        sess = get_express_session(req)

        if hasattr(req, 'user') and req.user.is_authenticated() and req.user.kratos_id:
            sess['user'] = req.user.kratos_id
        else:
            sess.pop('user', None)
        set_express_session(resp, sess)

        return resp