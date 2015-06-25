"""
Django settings for devdash project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

from django.core.exceptions import ImproperlyConfigured
try:
    import settings_secret as _secret_settings
except:
    _secret_settings = None


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


def get_secret(secret, default=None):
    """
    return the secret setting stored on the local machine,
    outside of version control. Currently, this is done in
    a file called ./devdash/settings_secret.py.
    However, we can convert to env variables at any time.

    will return default if doesn't exist in secret_settings
    and default provided. if no default, will raise error.
    """
    try:
        return getattr(_secret_settings, secret)
    except:
        if default is not None:
            return default
        else:
            msg = "secret, {}, not set".format(secret)
            raise ImproperlyConfigured(msg)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_secret('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

AUTH_USER_MODEL = 'core.User'

LOGIN_REDIRECT_URL = '/'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'core.backends.GitHubEnterprise',
    'core.backends.GitHub',

)

SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'social.pipeline.user.get_username',
    'github.pipeline.enterprise_details',
    'osw.pipeline.join_org',
    'osw.pipeline.enable_2fa',
    'osw.pipeline.github_details',
    'social.pipeline.user.create_user',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
    'social.pipeline.user.user_details',
    # # We are not currently using any of the dash functionality, so we don't want to spend time syncing
    # 'core.pipeline.sync',
    'kratos.pipeline.register_kratos',
)

SOCIAL_AUTH_GITHUB_ENTERPRISE_KEY = get_secret('SOCIAL_AUTH_GITHUB_ENTERPRISE_KEY')
SOCIAL_AUTH_GITHUB_ENTERPRISE_SECRET = get_secret('SOCIAL_AUTH_GITHUB_ENTERPRISE_SECRET')
SOCIAL_AUTH_GITHUB_ENTERPRISE_SCOPE = ['user', 'admin:repo_hook', 'admin:org', 'write:public_key']
SOCIAL_AUTH_GITHUB_ENTERPRISE_HOST = get_secret('SOCIAL_AUTH_GITHUB_ENTERPRISE_HOST')
SOCIAL_AUTH_GITHUB_ENTERPRISE_USER_FIELDS = ('first_name', 'last_name', 'username', 'email', 'contractor',)
SOCIAL_AUTH_GITHUB_KEY = get_secret('SOCIAL_AUTH_GITHUB_KEY')
SOCIAL_AUTH_GITHUB_SECRET = get_secret('SOCIAL_AUTH_GITHUB_SECRET')
SOCIAL_AUTH_GITHUB_SCOPE = ['user', 'write:org', 'write:public_key']

# ids of all orgs belonging to the entity
GH_ORG_IDS = get_secret('GH_ORG_IDS', (1071563,))

# Team to invite users to when joining the org (must invite to a team, not to an org)
GH_WELCOME_TEAM = get_secret('GH_WELCOME_TEAM')

# READ ONLY CREDENTIALS
GH_ADMIN_CREDENTIALS = get_secret('GH_ADMIN_CREDENTIALS') # A requests.auth.HTTPBasicAuth object

# READ ONLY CREDENTIALS
GHE_ADMIN_CREDENTIALS = get_secret('GHE_ADMIN_CREDENTIALS') # A requests.auth.HTTPBasicAuth object

KRATOS_ADMIN_PWD = get_secret('KRATOS_ADMIN_PWD')
KRATOS_ENFORCE_GH_ORGS = GH_ORG_IDS
KRATOS_ENFORCE_GHE = True

# Application definition

INSTALLED_APPS = (
    'tiles',
    'core',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social.apps.django_app.default',
    'github',
    'kratos',
    'osw',
    'jenkins',
)

HOME_TILES = ('github.ghe_repos', 'github.gh_repos',)
SYNC = ('github',)


GH_TILES = ('osw.join_org',)
GHE_TILES = tuple()
GH_REPO_ACTIONS = tuple()
GHE_REPO_ACTIONS = ('osw.openSource', 'jenkins.createJob')

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'core.express_auth.SetExpressAuthentication',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'devdash.urls'

WSGI_APPLICATION = 'devdash.wsgi.application'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'frontend', 'dest', 'static'),
)

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATA_DIR = get_secret('DATA_DIR', BASE_DIR)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(DATA_DIR, 'db.sqlite3'),
    }
}
KRATOS_URL = 'http://localhost/kratos'

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
