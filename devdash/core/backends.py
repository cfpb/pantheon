from social.backends.github import GithubOAuth2
from django.conf import settings

class GitHub(GithubOAuth2):
    EXTRA_DATA = [
            ('id', 'id'),
            ('expires', 'expires'),
            ('username', 'username'),
        ]
    def get_user_details(self, response):
        out = super(GitHub, self).get_user_details(response)
        out['gh_id'] = response.get('id')
        return out


class GitHubEnterprise(GithubOAuth2):
    name = 'github-enterprise'
    AUTHORIZATION_URL = settings.SOCIAL_AUTH_GITHUB_ENTERPRISE_HOST + '/login/oauth/authorize'
    ACCESS_TOKEN_URL = settings.SOCIAL_AUTH_GITHUB_ENTERPRISE_HOST + '/login/oauth/access_token'
    EXTRA_DATA = [
            ('id', 'id'),
            ('expires', 'expires'),
            ('username', 'username'),
        ]

    def _user_data(self, access_token, path=None):
        url = self.setting('HOST') + '/api/v3/user{0}'.format(path or '')
        return self.get_json(url, params={'access_token': access_token})

    def get_user_details(self, response):
        out = super(GitHubEnterprise, self).get_user_details(response)
        out['location'] = response.get('location')
        out['ghe_id'] = response.get('id')
        return out
