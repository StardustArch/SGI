"""
settings.py — SGI Internato IICB

Alterações desta versão:
  - LOCAL_MODE: variável de ambiente para alternar entre LAN e produção
  - FRONTEND_URL: centralizado para o password reset
  - REST_FRAMEWORK: paginação padrão global definida
  - TIME_ZONE: corrigido para Africa/Maputo
  - SMS: configuração AfricasTalking (variáveis de ambiente)
  - SECRET_KEY: movida para variável de ambiente (não committar em produção)
"""

import os
from pathlib import Path
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------------
# MODO DE OPERAÇÃO
# LOCAL_MODE=True → sistema corre em LAN sem internet
#   - Email vai para consola (sem envio real)
#   - SMS desactivado (log apenas)
#   - SQLite em vez de MySQL
# LOCAL_MODE=False → produção (Render/VPS)
# ---------------------------------------------------------------------------
LOCAL_MODE = os.environ.get('LOCAL_MODE', 'True') == 'True'

# ---------------------------------------------------------------------------
# SEGURANÇA
# Em produção: export SECRET_KEY="chave-longa-aleatoria"
# Nunca commitar a chave real no git.
# ---------------------------------------------------------------------------
SECRET_KEY = os.environ.get(
    'SECRET_KEY',
    'django-insecure-8fqblpcxe6pn^*72tl(r=l48l#oq)s%6vlk14ap9=(6l=4*4a3'
)

DEBUG = os.environ.get('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'backend',
    'sgi-n29z.onrender.com',
    # Para instalação LAN: adicionar o IP local do servidor
    # Ex: '192.168.1.100'
]

CSRF_TRUSTED_ORIGINS = [
    'https://sgi-n29z.onrender.com',
    'https://sgixp.vercel.app',
    'http://localhost:3000',
]

# ---------------------------------------------------------------------------
# APPS
# ---------------------------------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core.apps.CoreConfig',
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'django_filters',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'sgi_api.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'sgi_api.wsgi.application'

# ---------------------------------------------------------------------------
# BASE DE DADOS
# LOCAL_MODE → SQLite (sem instalação extra, funciona offline)
# Produção  → MySQL (robusto para múltiplos utilizadores em rede)
# ---------------------------------------------------------------------------
if LOCAL_MODE:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.environ.get('DB_NAME', 'sgi_db'),
            'USER': os.environ.get('DB_USER', 'sgi_user'),
            'PASSWORD': os.environ.get('DB_PASSWORD', ''),
            'HOST': os.environ.get('DB_HOST', 'localhost'),
            'PORT': os.environ.get('DB_PORT', '3306'),
        }
    }

# ---------------------------------------------------------------------------
# AUTENTICAÇÃO
# ---------------------------------------------------------------------------
AUTH_USER_MODEL = 'core.Utilizador'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ---------------------------------------------------------------------------
# INTERNACIONALIZAÇÃO
# FIX: TIME_ZONE corrigido para Moçambique (UTC+2)
# ---------------------------------------------------------------------------
LANGUAGE_CODE = 'pt-mz'
TIME_ZONE = 'Africa/Maputo'
USE_I18N = True
USE_TZ = True

# ---------------------------------------------------------------------------
# FICHEIROS ESTÁTICOS E MEDIA
# ---------------------------------------------------------------------------
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ---------------------------------------------------------------------------
# DJANGO REST FRAMEWORK
# Paginação global definida — elimina inconsistência entre views
# ---------------------------------------------------------------------------
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    # FIX: paginação padrão global — todas as ListAPIViews herdam isto
    # Views que precisam de comportamento diferente podem sobrepor pagination_class
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
}

# ---------------------------------------------------------------------------
# JWT
# ---------------------------------------------------------------------------
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),   # Aumentado de 15 → 30 para melhor UX em LAN
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
}

# ---------------------------------------------------------------------------
# EMAIL
# LOCAL_MODE → consola (sem servidor de email necessário)
# Produção  → configurar SMTP real (ex: Gmail, Mailgun, etc.)
# ---------------------------------------------------------------------------
if LOCAL_MODE:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
    EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
    EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')

DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'admin@sgi-iicb.com')

# ---------------------------------------------------------------------------
# SMS via AfricasTalking (presença confirmada em Moçambique)
# Para activar:
#   1. pip install africastalking
#   2. Criar conta em africastalking.com
#   3. Definir variáveis de ambiente:
#      export AT_USERNAME="seu_username"
#      export AT_API_KEY="sua_api_key"
# Em LOCAL_MODE as variáveis ficam vazias e o SMS vai para o log.
# ---------------------------------------------------------------------------
AT_USERNAME = os.environ.get('AT_USERNAME', '')
AT_API_KEY = os.environ.get('AT_API_KEY', '')

# ---------------------------------------------------------------------------
# URL DO FRONTEND (para links de password reset)
# ---------------------------------------------------------------------------
FRONTEND_URL = os.environ.get('FRONTEND_URL', 'http://localhost:3000')

# ---------------------------------------------------------------------------
# CORS
# ---------------------------------------------------------------------------
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://frontend:3000",
    "https://sgixp.vercel.app",
]

# Para instalação LAN: adicionar o IP do servidor frontend
# CORS_ALLOWED_ORIGINS += ["http://192.168.1.100:3000"]
AUTHENTICATION_BACKENDS = [
    'core.backends.IdentificadorBackend',
    'django.contrib.auth.backends.ModelBackend',  # fallback
]
# ---------------------------------------------------------------------------
# LOGGING
# Regista warnings e erros de notificações sem crashar o sistema
# ---------------------------------------------------------------------------
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[{levelname}] {asctime} {module}: {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'core': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}