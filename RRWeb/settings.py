"""
Django settings for RRWeb project.

Generated by 'django-admin startproject' using Django 2.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '!q$gc_z)%m)rkfo-lxzfqwb1=4#l%@)o4z+e2xrq!dwbj1&&5k'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'rrsite.apps.RRsiteConfig',
    'search.apps.SearchConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
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

ROOT_URLCONF = 'RRWeb.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'RRWeb.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'rrweb_db',
        'USER': 'root',
        'PASSWORD': 'lglmmd',
        'HOST': '58.87.109.246',
        #'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

EMAIL_LOGIN_METHOD = 0
PHONE_LOGIN_METHOD = 1
LOGIN_METHOD = {'no_method': -1, 'email': EMAIL_LOGIN_METHOD, 'phone': PHONE_LOGIN_METHOD}

# 登录账号/密码错误信息
ERROR_LOGIN_MSG = {'msg': 'Email(Phone Number) or Password Incorrect, Please Check Again'}
ERROR_LOGIN_EMAIL_VALIDATION = {'msg': 'Please Check Your Email and Verify the Email Address First'}
# 登录格式错误信息
ERROR_LOGIN_FORMAT = {'msg': 'Email(Phone Number) Format Incorrect, Please Check Again'}
# 注册表单格式错误
ERROR_FORM_FORMAT = {'error_email_msg': 'Form \'s Format is Incorrect'}

ERROR_SEND_EMAIL = {'msg': 'Sending Authentication Email Failed. Please Check Your Email'}
ERROR_EMAIL_FORMAT = {'msg': 'Email \'s Format is Incorrect'}
EMAIL_REGISTER_ALREADY = {'msg': 'You have already register. Please Verify Your Email And Login'}
EMAIL_REGISTER_SUCCESS = {'msg': 'Email Register Success! Please Check Your Email and Activate the Account ASAP!'}

ERROR_PHONE_FORMAT = {'error_phone_msg': 'Form \'s Format is Incorrect'}
ERROR_PHONE_CODE = {'error_phone_msg': 'Your Phone \'s Verification Code is Incorrect'}
PHONE_REGISTER_ALREADY = {'msg': 'You have already register. Please Login'}
PHONE_REGISTER_SUCCESS = {'msg': 'Phone Register Success! You Can Login Now!'}
PHONE_CODE_SEND_FAILED = {'msg': 'Sending Verification Code Failed!'}

# 手机验证码过期时间
PHONE_VERIFY_MINUTES = 10
PHONE_VERIFY_SECONDS = 60 * PHONE_VERIFY_MINUTES

# 邮箱验证SMTP设置
EMAIL_HOST = "smtp.163.com"
EMAIL_PORT = 25
EMAIL_HOST_USER = "RRWeb_Offical@163.com"
EMAIL_HOST_PASSWORD = "mmdlgl233"
EMAIL_USE_TLS = False
EMAIL_FROM = "RRWeb_Offical@163.com"

# 邮箱激活内容
EMAIL_VERIFY_SUCCEED_TITLE = 'Email Activation Succeed!'
EMAIL_VERIFY_SUCCEED_CONTENT = 'The email has been activated.The page will jump to our Main Page in 10 seconds.' \
                           'If the page does not jump you can click the button here to view our main page.'
EMAIL_VERIFY_FAIL_TITLE = 'Email Activation Failed!'
EMAIL_VERIFY_FAIL_CONTENT = 'The email has not been activated. The verification url was wrong!' \
                                  ' The page will jump to our Main Page in 10 seconds.' \
                                  'If the page does not jump you can click the button here to view our main page.'

# 邮箱正则匹配
EMAIL_REGEX = "^[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}$"
# 电话正则匹配
PHONE_REGEX = "1[358][\d]{9}"


# 图片url格式
PHOTO_STATIC_URL_FORMAT = 'http://58.87.109.246/static/photos/{0}.jpg'

# 静态文件路径
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static")
]

# 静态文件收集路径
STATIC_ROOT = '/data/collected_static'