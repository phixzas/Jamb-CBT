from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-*(*tg&ihe9rb6@#r(n@hxc*b3!5_(!dy0)2$_zo$@xj816_t8h'

DEBUG = True

# ====================== SECURITY SETTINGS ======================

ALLOWED_HOSTS = ['*']

CSRF_TRUSTED_ORIGINS = [
    'http://127.0.0.1',
    'http://localhost',
    'http://192.168.1.104',     # ← Put your current laptop IP here
]

# These are critical for login to work from phone
CSRF_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False

# Optional but helpful
SESSION_COOKIE_DOMAIN = None

# ================= AUTH SETTINGS =================
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/login/'

# ================= APPLICATIONS =================
INSTALLED_APPS = [
    "jazzmin",  # ✅ MUST BE FIRST

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'exams.apps.ExamsConfig',
]

# ================= MIDDLEWARE =================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'jamb_cbt.urls'

# ================= TEMPLATES =================
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

WSGI_APPLICATION = 'jamb_cbt.wsgi.application'

# ================= DATABASE =================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ================= PASSWORD VALIDATION =================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ================= INTERNATIONALIZATION =================
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ================= STATIC =================
STATIC_URL = 'static/'

# ================= EMAIL CONFIG =================
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "phixzas60@gmail.com"
EMAIL_HOST_PASSWORD = "pjbb gfmq jkei uwat"

# ================= PAYSTACK =================
PAYSTACK_SECRET_KEY = "sk_test_86500f868558db97037ae0d4dfaa3036a01dcf71"
PAYSTACK_PUBLIC_KEY = "pk_test_2dd7563c27640843bf759bb0e82497b19ee7e2ed"

# ================= JAZZMIN DESIGN =================
JAZZMIN_SETTINGS = {
    "site_title": "JAMB CBT Admin",
    "site_header": "JAMB CBT Dashboard",
    "site_brand": "CBT System",

    "welcome_sign": "Welcome to CBT Admin",

    "topmenu_links": [
        {"name": "Home", "url": "admin:index"},
    ],

    "icons": {
        "auth.User": "fas fa-user",
        "exams.Profile": "fas fa-id-card",
        "exams.Subject": "fas fa-book",
        "exams.Question": "fas fa-question",
    },

    "show_sidebar": True,
    "navigation_expanded": True,
}
# Allow access from phone
ALLOWED_HOSTS = ['*']

CSRF_TRUSTED_ORIGINS = [
    'http://127.0.0.1',
    'http://localhost',
    'http://192.168.1.104',   # Change this to your actual IP if different
]

SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_SAMESITE = 'Lax'