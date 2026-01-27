"""
Django settings for VisorCamaras_JCD project.

CONFIGURACIÓN SEGURA: Lee las credenciales del archivo .env
"""

from pathlib import Path
import os
from dotenv import load_dotenv  # <--- IMPORTANTE: Carga el archivo .env

# 1. Cargar las variables del archivo .env
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# ==============================================================================
#  SEGURIDAD (Leída desde .env)
# ==============================================================================

# Lee la clave del .env. Si falla, usa una insegura (solo para que no crashee en local)
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'django-insecure-clave-fallback-error')

# Lee si es modo Debug (True/False)
DEBUG = os.getenv('DEBUG') == 'True'

# Lee quién puede entrar
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '*').split(',')

# ==============================================================================
#  APLICACIONES INSTALADAS
# ==============================================================================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # APLICACION
    'monitor',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'VisorCamaras_JCD.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'], # Mantenemos carpeta templates
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

WSGI_APPLICATION = 'VisorCamaras_JCD.wsgi.application'


# ==============================================================================
#  BASE DE DATOS (Conectada al .env)
# ==============================================================================

DATABASES = {
    'default': {
        'ENGINE': 'mssql',
        # Lee del .env (ej: JCDecaux_Visor)
        'NAME': os.getenv('DB_NAME', 'JCDecaux_Visor'),
        # Lee del .env (ej: (localdb)\MSSQLLocalDB)
        'HOST': os.getenv('DB_SERVER', r'(localdb)\MSSQLLocalDB'),
        'PORT': '',
        'OPTIONS': {
            'driver': 'ODBC Driver 17 for SQL Server',
            'extra_params': 'Trusted_Connection=yes',
        },
    }
}


# ==============================================================================
#  VALIDACIÓN DE CONTRASEÑAS
# ==============================================================================

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


# ==============================================================================
#  IDIOMA Y ZONA HORARIA
# ==============================================================================

LANGUAGE_CODE = 'es-es'  # Puesto en español

TIME_ZONE = 'Europe/Madrid' # Hora de España

USE_I18N = True

USE_TZ = True


# ==============================================================================
#  ARCHIVOS ESTÁTICOS
# ==============================================================================

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'