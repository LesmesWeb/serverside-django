"""
Django settings for serverside project.

Generated by 'django-admin startproject' using Django 2.2.10.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'k6@el62+#j-w8579u-bapoxqqj^6(=&@ppp5lg2lcnfb@3)3i4'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

#Habilita el uso de las cookies para los mensajes flotantes con SweetAlert
#https://docs.djangoproject.com/en/2.2/ref/settings/#std:setting-MESSAGE_STORAGE
MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage' #almacenar mensajes temporales.


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    #Permite analizar el rendimiento de las consultas SQL 
   	'debug_toolbar', 
    #permite modificar campos de formulario en plantillas como son class, type etc
    'widget_tweaks',

    #Libreria de conexiòn inicio de sesión
	'allauth',
	'allauth.account',
	'allauth.socialaccount',
	'allauth.socialaccount.providers.google',
	'django.contrib.sites',

    #Apps
	'apps.proyecto',
	'apps.stakeholders',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #django_toolbar
	'debug_toolbar.middleware.DebugToolbarMiddleware',
]

#IPs validas para django_toolbar
INTERNAL_IPS = [
	# ...
	'127.0.0.1',
    'localhost',
	# ...
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

"""
#Conexión con Postgresql

import config.db as db
DATABASES = db.SQLITE


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'es-co'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

#directorio de donde van a estar alojados los archivos estaticos y donde buscarlos
STATICFILES_DIRS = [
	os.path.join(BASE_DIR, "static"),
]

#Configuraciòn Google Sesion
AUTHENTICATION_BACKENDS = (
	"django.contrib.auth.backends.ModelBackend",
	"allauth.account.auth_backends.AuthenticationBackend",
)

#Diccionario que contiene configuraciones específicas del proveedor de oauth.

SOCIALACCOUNT_PROVIDERS = {
     "google": {
        # Credenciales del app creada en https://console.developers.google.com/?hl=ES&pli=1    
        "APP": {
            'client_id': '', #quitadas
            'secret': '',    #quitadas
            "key": ""
        },
        # These are provider-specific settings that can only be
        # listed here:
        "SCOPE": [
            "profile",
            "email",
        ],
        "AUTH_PARAMS": {
            "access_type": "online",
        },
        "verified_email": "true",
    }
}

# Variables que habilitan la autenticación en el oauth de google

SITE_ID = 1
LOGIN_REDIRECT_URL = 'home' #'proyecto:lista_proyectos' 
LOGOUT_REDIRECT_URL = 'login'
ACCOUNT_AUTHENTICATION_METHOD = "email" # Defaults to username_email
ACCOUNT_USERNAME_REQUIRED = False       # Defaults to True
ACCOUNT_EMAIL_REQUIRED = True           # Defaults to False
SOCIALACCOUNT_QUERY_EMAIL = ACCOUNT_EMAIL_REQUIRED
SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_EMAIL_REQUIRED = False
SOCIALACCOUNT_ADAPTER = 'config.adapter.MySocialAccountAdapter'
VERIFIED_EMAIL = True
#ACCOUNT_EMAIL_VERIFICATION = 'mandatory' #Verificacion por email obligatoria
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 5 #Evita el spam y bloquea al superar el numero de intentos asignados

"""
Para el reestaablecimiento de contraseñas son necesarias las
siguientes variables que habilitan elk envio de correos pos SMTP,
el correo asignado debe tener habilitado la opción de aplicaciones poco seguras:
https://www.google.com/settings/security/lesssecureapps
"""

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587 #TLS usa el valor 587 pero si usa SSL tendrá que ser 465
EMAIL_HOST_USER = ''     #quitada
EMAIL_HOST_PASSWORD = '' #quitada

#https://www.codegrepper.com/code-examples/whatever/django+messages+alert+
#https://www.codegrepper.com/code-examples/whatever/message+tags+in+django
from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.ERROR: 'warning',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning'
}