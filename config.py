import os
basedir = os.path.abspath(os.path.dirname(__file__))

#表单配置
SCRF_ENABLE = True
SECRET_KEY = 'ZZZ'
#数据库配置
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
SQLALCHEMY_TRACK_MODIFICATIONS = False

SQLALCHEMY_DATABASE_URL = os.environ.get('DEV_DATABASE_URL') or 'splite:///' +os.path.join(basedir, 'data-dev.sqlite')
DEBUG = True

CHAPTER_PER_PAGE = 20
