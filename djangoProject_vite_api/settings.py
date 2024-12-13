"""
Django settings for djangoProject_vite_api project.

Generated by 'django-admin startproject' using Django 5.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-z67#b2q3=agr@)&7pynf=%03wa2xvz39m^w1sez@up(=uy2z1h'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']
# CORS_ORIGIN_ALLOW_ALL = True  # 允許攜帶憑證 (Cookie)
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'djangorestframework-simplejwt'
    'rest_framework',
    'corsheaders',
    'schedule_courses.apps.ScheduleCoursesConfig'  # ?
]

# MIDDLEWARE = [
#     'django.middleware.csrf.CsrfViewMiddleware',
#     'corsheaders.middleware.CorsMiddleware',
#     'django.middleware.security.SecurityMiddleware',
#     'django.contrib.sessions.middleware.SessionMiddleware',
#     'django.middleware.common.CommonMiddleware',
#     'django.contrib.auth.middleware.AuthenticationMiddleware',
#     'django.contrib.messages.middleware.MessageMiddleware',
#     'django.middleware.clickjacking.XFrameOptionsMiddleware',
#     # 'corsheaders.middleware.CorsMiddleware',
# # ]
# MIDDLEWARE = [
#     'corsheaders.middleware.CorsMiddleware',  # 必須在最前面或至少在 CommonMiddleware 前
#     'django.middleware.common.CommonMiddleware',
#     'django.middleware.csrf.CsrfViewMiddleware',
#     'django.middleware.security.SecurityMiddleware',
#     'django.contrib.sessions.middleware.SessionMiddleware',
#     'django.contrib.auth.middleware.AuthenticationMiddleware',
#     'django.contrib.messages.middleware.MessageMiddleware',
#     'django.middleware.clickjacking.XFrameOptionsMiddleware',
# ]
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # CORS必須在前
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware', # SessionMiddleware必須在CsrfViewMiddleware前
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware', # CsrfViewMiddleware必須在 SessionMiddleware 之後
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'djangoProject_vite_api.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'schedule_courses', 'templates']
        ,
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

WSGI_APPLICATION = 'djangoProject_vite_api.wsgi.application'


AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]
AUTH_USER_MODEL = 'schedule_courses.CustomUser'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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

# CORS_ORIGIN_WHITELIST = [
#     'http://127.0.0.1:5173',  # React 的開發域名
#     'http://127.0.0.1:5173',
# ]
CSRF_TRUSTED_ORIGINS = [
    'http://localhost:5173',  # 確保與前端完全一致
    'http://127.0.0.1:5173',  # 如果使用 127.0.0.1
]

CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',
    'http://127.0.0.1:5173',
]

CORS_ALLOW_CREDENTIALS = True  # 確保允許攜帶 Cookie
CSRF_COOKIE_SECURE = False  # 禁用 HTTPS 限制
CSRF_COOKIE_SAMESITE = 'Lax'#'Lax'  # 或 'None'（允许跨站点请求携带 Cookie）

SESSION_COOKIE_SECURE = False  # 如果你使用了 Django Session，也需要关闭 HTTPS 限制
# CSRF_COOKIE_SAMESITE = 'None'
# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/
BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



# 找回密碼有限

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # 或您使用的郵件服務提供者
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'lai27418@gmail.com'  # 替換為您的郵件地址
EMAIL_HOST_PASSWORD = 'dhaadbezmiyalbu'  # 替換為您的郵件密碼
# DEFAULT_FROM_EMAIL = 'Your Project <your_email@example.com>'