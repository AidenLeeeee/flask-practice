import os

BASE_PATH = os.path.dirname(os.path.abspath(__file__))

class Config:
    """Flask Config"""
    SECRET_KEY = 'secretkey'
    SESSION_COOKIE_NAME = 'project'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:password@localhost/project?charset=utf8'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SWAGGER_UI_DOC_EXPANSION = 'list'
    USER_STATIC_BASE_DIR = 'user_images'
    
    
class DevelopmentConfig(Config):
    """Flask Config for Dev"""
    DEBUG = True
    SEND_FILE_MAX_AGE_DEFAULT = None
    # TODO: Front 호출 시 처리
    WTF_CSRF_ENABLED = False


class TestingConfig(DevelopmentConfig):
    __test__ = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(BASE_PATH, "sqlite_test.db")}'
    
    
class ProductionConfig(Config):
    """Flask Config for Prod"""
    pass