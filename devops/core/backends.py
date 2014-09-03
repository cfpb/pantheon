from social.backends.github import GithubOAuth2
from django.conf import settings

class GitHubEnterprise(GithubOAuth2):
    name = 'github-enterprise'
    AUTHORIZATION_URL = settings.SOCIAL_AUTH_GITHUB_ENTERPRISE_HOST + '/login/oauth/authorize'
    ACCESS_TOKEN_URL = settings.SOCIAL_AUTH_GITHUB_ENTERPRISE_HOST + '/login/oauth/access_token'

    def _user_data(self, access_token, path=None):
        url = self.setting('HOST') + '/api/v3/user{0}'.format(path or '')
        return self.get_json(url, params={'access_token': access_token})
