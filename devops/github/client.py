from universalclient import Client
import rauth
from django.conf import settings
from universalclient import jsonFilter

ghe_client_key = settings.SOCIAL_AUTH_GITHUB_ENTERPRISE_KEY
ghe_client_secret = settings.SOCIAL_AUTH_GITHUB_ENTERPRISE_SECRET
ghe_host = settings.SOCIAL_AUTH_GITHUB_ENTERPRISE_HOST
ghe_admin_auth = settings.GHE_ADMIN_CREDENTIALS

gh_client_key = settings.SOCIAL_AUTH_GITHUB_KEY
gh_client_secret = settings.SOCIAL_AUTH_GITHUB_SECRET
gh_host = 'https://api.github.com'
gh_admin_auth = settings.GH_ADMIN_CREDENTIALS

def GitHubEnterprise(user_model=None, access_token=None):
    """
    return a UniversalClient client for GitHub Enterprise, authenticated with the given access_token.
    If access_token is not passed, will look for the access_token associated with 
    the user_model.
    """
    if not access_token:
        if not user_model.is_authenticated():
            return None
        access_token = user_model.social_auth.get(provider='github-enterprise').tokens
    session = rauth.OAuth2Session(ghe_client_key, ghe_client_secret, access_token)
    return Client(ghe_host + '/api/v3', oauth=session, dataFilter=jsonFilter)

def GitHub(user_model=None, access_token=None):
    """
    return a UniversalClient client for GitHub, authenticated with the given access_token.
    If access_token is not passed, will look for the access_token associated with 
    the user_model.
    """
    if not access_token:
        try:
            access_token = user_model.social_auth.get(provider='github').tokens
        except:
            return None
    session = rauth.OAuth2Session(gh_client_key, gh_client_secret, access_token)
    return Client(gh_host, oauth=session, dataFilter=jsonFilter)

def GitHubEnterpriseAdmin(credentials=None):
    credentials = credentials or ghe_admin_auth
    return Client(ghe_host, auth=credentials, dataFilter=jsonFilter)

def GitHubAdmin(credentials=None):
    credentials = credentials or gh_admin_auth
    return Client(gh_host, auth=credentials, dataFilter=jsonFilter)


def get_org_name(client, org_id):
    """
    given a client for a user that is a member of the org, return the org_name for the given org_id
    """
    orgs = {org['id']: org['login'] for org in client.user.orgs.get().json()}
    return orgs[org_id]

def get_team_id(client, org_id, team_name):
    org_name = get_org_name(client, org_id)
    teams_client = client.orgs._(org_name).teams
    for team_data in iter_get(teams_client):
        if team_data['name'] == team_name:
            return team_data['id']
    return False

def is_org_member(client, username, org_name, public=False):
    """
    client must either be a client for the given username or a client with admin privileges for the org.
    public - whether the user is a public org member
    """
    members = 'public_members' if public else 'members'
    return client.orgs._(org_name)._(members)._(username).get().status_code == 204

def is_team_member(client, username, team_id):
    return client.teams._(str(team_id)).members._(username).get().status_code

def is_2fa_enabled(client, username, org_name):
    no_2fa_members = client.orgs._(org_name).members \
                        .headers(accept='application/vnd.github.the-wasp-preview+json') \
                        .get(params={'filter':'2fa_disabled'}).json()
    no_2fa_usernames = [u['login'] for u in no_2fa_members]
    return username not in no_2fa_usernames


def iter_get(client):
    """
    return an iterator over all results from GETing the client and any subsequent pages.
    """
    items = []
    while items or client:
        if not items:
            resp = client.get()
            items = resp.json()
            next = resp.links.get('next', {}).get('url')
            client = client._path([next]) if next else None
        yield(items.pop(0))
