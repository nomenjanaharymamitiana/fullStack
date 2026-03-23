import os
import dj_database_url  # N'oublie pas de faire : pip install dj-database-url psycopg2-binary
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-votre-cle-par-defaut')

# Désactiver DEBUG en production (Render mettra DEBUG à False via les variables d'env)
DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'

# Autoriser ton URL Render et localhost
ALLOWED_HOSTS = ['*'] # Tu pourras restreindre à ['votre-app.onrender.com'] plus tard

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'api',
    'rest_framework',
    'corsheaders', # Déjà présent, c'est bien
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware', # DOIT ÊTRE TOUT EN HAUT
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Pour gérer les fichiers statiques sur Render
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'listtodo.urls'

WSGI_APPLICATION = 'listtodo.wsgi.application'

# Configuration de la DATABASE (PostgreSQL sur Render, SQLite en local)
DATABASES = {
    'default': dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600
    )
}

# Configuration CORS
CORS_ALLOW_ALL_ORIGINS = True # Pour le test, on autorise tout

# Fichiers Statiques (Obligatoire pour Render)
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
