import os


class Config:
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CSRF_ENABLED = True
    SECRET_KEY = 'I-hope-you-can-guess'

    MAIL_SERVER= 'smtp.qq.com'
    MAIL_PORT= 587
    MAIL_USE_TLS = True
    MAIL_USERNAME= '管理员邮箱'
    MAIL_PASSWORD= '邮箱密码'
    FLASKY_MAIL_SUBJECT_PREFIX = '[作业通知]'
    FLASKY_MAIL_SENDER= '作业通知助手<管理员邮箱>'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = ''
    MY_FORM_POST_URL = ''


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root@localhost/homework?charset=utf8'
    MY_FORM_POST_URL = ''


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = ''
    MY_FORM_POST_URL = ''


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
