from universalclient import Client
import rauth
from django.conf import settings

ghe_client_key = settings.SOCIAL_AUTH_GITHUB_ENTERPRISE_KEY
ghe_client_secret = settings.SOCIAL_AUTH_GITHUB_ENTERPRISE_SECRET
ghe_host = settings.SOCIAL_AUTH_GITHUB_ENTERPRISE_HOST

gh_client_key = settings.SOCIAL_AUTH_GITHUB_KEY
gh_client_secret = settings.SOCIAL_AUTH_GITHUB_SECRET
gh_host = 'https://api.github.com'

def GitHubEnterprise(user):
    if not user.is_authenticated():
        return None
    access_token = user.social_auth.get(provider='github-enterprise').tokens
    session = rauth.OAuth2Session(ghe_client_key, ghe_client_secret, access_token)
    return Client(ghe_host + '/api/v3', oauth=session)

def GitHub(user):
    try:
        access_token = user.social_auth.get(provider='github').tokens
    except:
        return None
    session = rauth.OAuth2Session(gh_client_key, gh_client_secret, access_token)
    return Client(gh_host, oauth=session)
