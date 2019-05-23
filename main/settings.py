"""
Django settings for main project.

Generated by 'django-admin startproject' using Django 2.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os, multiprocessing

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 自动配置环境变量
try:
    with open(os.path.join(BASE_DIR, '.env')) as f:
        data = f.read().split('\n')
    for line in data:
        i, j = line.split('=')
        os.environ[i.strip()] = j.strip()
except:
    pass

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = 'DEBUG' in os.environ

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'usr_sys',
    'match_sys',
    'ajax_sys',
    'external',
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

ROOT_URLCONF = 'main.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'libraries': {
                'tag_loader': 'external.tag_loader',
                'main_filters': 'main.filters',
            }
        },
    },
]

WSGI_APPLICATION = 'main.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

if os.sys.platform == 'win32':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
else:
    # 替换数据库后端
    import pymysql
    pymysql.install_as_MySQLdb()

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'arena',
            'USER': os.environ['MYSQL_USER'],
            'PASSWORD': os.environ['MYSQL_PASSWD'],
            'HOST': os.environ['MYSQL_HOST'],
            'PORT': os.environ['MYSQL_PORT'],
        }
    }

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME':
        'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/assets/'
STATIC_ROOT = os.path.join(BASE_DIR, 'assets')
if os.sys.platform == 'win32':
    STATICFILES_DIRS = [os.path.join(BASE_DIR, 'assets')]
    del STATIC_ROOT

MEDIA_URL = '/_STORAGE/'
MEDIA_ROOT = os.path.join(BASE_DIR, '_STORAGE')

# 合法字符集合
RAND_CHARPOOL = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789_'  # 用于生成随机字符串
USERNAME_CHARPOOL = set(RAND_CHARPOOL)  # 用于匹配用户名

# 邮件bot系统
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.pku.edu.cn'
EMAIL_PORT = 25
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')

# 验证邮件配置参数
EMAIL_VALID_RESEND_MINUTES = 5  # 每{}分钟可重发一次验证邮件
EMAIL_VALID_LAST_DAYS = 5  # 每封验证邮件内链接有效期为{}天

# 动态文件目录
CODE_DIR = os.path.join(MEDIA_ROOT, 'code')  # 比赛记录存储目录
PAIRMATCH_DIR = os.path.join(MEDIA_ROOT, 'pairmatch')  # 比赛记录存储目录

MAX_CODE_PER_GAME = 5  # 单用户单游戏最多保存代码数

### 比赛系统参数
AI_TYPES = {  # AI比赛类型
    0: '黑白棋',
    1: '漂移乒乓',
    2: '纸带圈地',
    3: '星际吞噬',
}
MATCH_TYPES = {  # 生成比赛类型
    4: '交替先后手',
    3: '随机先后手',
    0: '我方先手',
    1: '对方先手',
    2: '双方对半先手',
    # 4:'Override',
}
MATCH_CODE_LENGTH = 10  # 比赛记录文件随机编码长度
MATCH_POOL_SIZE = multiprocessing.cpu_count()  # 最大同时启动比赛数
PAIRMATCH_STATUS = {  # 比赛状态码
    0: '未启动',
    1: '执行中',
    2: '已完成',
    3: '已中止',
}
DEFAULT_MAX_RUNNING_SEC = 2  # 获取计时函数缺省时每局最大运行{}秒

# 天梯匹配参数
SCORE_FACTOR_PAIRMATCH = 16  # 天梯积分变化参数
SCORE_FACTOR_NORANK = 0.05  # 自由对战模式天梯分变动参数
SCORE_NORM = 3000  # 归中分
SCORE_NORM_FACTOR = 0.001  # 归中系数
RANKING_RANDOM_RANGE = 10  # 随机前X个得分相近的代码参与匹配

# 比赛监控进程设置
MONITOR_CYCLE = 0.5  # 每隔（秒）监测一次比赛进程状态
MONITOR_SOCKET_PORT = 37037
MONITOR_DB_PATH = os.path.join(MEDIA_ROOT, 'matches.db')  # 比赛进程数据库路径
MONITOR_DB_VERSION = 'AA'  # 用于修改数据库结构时删库重建
MONITOR_DB_TABLES = [  # 建库使用的语句
    """CREATE TABLE "data_queue" ( `type` INTEGER, `code1` INTEGER, `code2` INTEGER, `match` TEXT, `param` TEXT DEFAULT '{}', `ranked` BOOLEAN DEFAULT false )""",
    """CREATE TABLE "running" ( `match` TEXT )""",
    'CREATE TABLE "%s" ( `n` INTEGER )' % MONITOR_DB_VERSION  # 版本标识
]

# 显示参数
TABLE_ICON_SIZE = 24  # 显示在表格内的用户头像大小
MAX_LADDER_USER = 10  # 天梯显示最大用户数
RECENT_MATCH_SHOWN = 100  # 最大显示历史比赛数
