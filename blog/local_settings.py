# local settings:

DEBUG = True
ALLOWED_HOSTS = ['*']
# ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'BlogDB',
        'HOST': 'blogdb.catsifludzz0.us-east-1.rds.amazonaws.com',
        'PORT': '3306',
        'USER': 'DjangoSQLUser',
        'PASSWORD': 'Djang017Passw',
    }
}

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'


# HTTPS SETTINGS
SECURE_PROXY_SSL_HEADER = None
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
