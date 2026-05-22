from pathlib import Path
import os
import dj_database_url

# ====================== BASE DIR ======================
BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env ONCE (IMPORTANT)


# ====================== SECRET KEY ======================
SECRET_KEY = os.getenv("SECRET_KEY")
import os

SECRET_KEY = os.environ.get("SECRET_KEY")

if not SECRET_KEY:
    raise Exception("SECRET_KEY is missing")
# ====================== DEBUG ======================
DEBUG = os.getenv("DEBUG", "True") == "True"

ALLOWED_HOSTS = ['*']

CSRF_TRUSTED_ORIGINS = [
    'https://jamb-cbt-005e.onrender.com',
    'http://jamb-cbt-005e.onrender.com',
    'http://127.0.0.1',
    'http://localhost',
]

# ====================== DATABASE ======================
if os.environ.get('DATABASE_URL'):
    DATABASES = {
        'default': dj_database_url.config(
            default=os.environ.get('DATABASE_URL')
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# ====================== SECURITY ======================
CSRF_COOKIE_SAMESITE = None
SESSION_COOKIE_SAMESITE = None
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False

# ====================== INSTALLED APPS ======================
INSTALLED_APPS = [
    "jazzmin",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'exams.apps.ExamsConfig',
]

# ====================== MIDDLEWARE ======================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',

    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',

    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'jamb_cbt.urls'

WSGI_APPLICATION = 'jamb_cbt.wsgi.application'

# ====================== TEMPLATES ======================
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

# ====================== AUTH ======================
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/login/'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ====================== LANGUAGE ======================
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ====================== STATIC FILES ======================
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ====================== EMAIL (BREVO FIXED) ======================
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

EMAIL_HOST = "smtp-relay.brevo.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True

EMAIL_HOST_USER = os.getenv("BREVO_EMAIL")
EMAIL_HOST_PASSWORD = os.getenv("BREVO_SMTP_KEY")

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# ====================== PAYSTACK ======================
PAYSTACK_SECRET_KEY = os.getenv("PAYSTACK_SECRET_KEY")
PAYSTACK_PUBLIC_KEY = os.getenv("PAYSTACK_PUBLIC_KEY")

# ====================== JAZZMIN ======================
JAZZMIN_SETTINGS = {
    "site_title": "JAMB CBT Admin",
    "site_header": "JAMB CBT Dashboard",
    "site_brand": "CBT System",
    "welcome_sign": "Welcome to CBT Admin",
    "topmenu_links": [{"name": "Home", "url": "admin:index"}],
    "icons": {
        "auth.User": "fas fa-user",
        "exams.Profile": "fas fa-id-card",
        "exams.Subject": "fas fa-book",
        "exams.Question": "fas fa-question",
    },
    "show_sidebar": True,
    "navigation_expanded": True,
}

# ====================== AUTH BACKENDS ======================
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'