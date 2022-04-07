class Config:
    """Flask Config"""
    SECRET_KEY = 'secretkey'
    SESSION_COOKIE_NAME = 'project'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:password@localhost/project?charset=utf8'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SWAGGER_UI_DOC_EXPANSION = 'list'
    
    
class DevelopmentConfig(Config):
    """Flask Config for Dev"""
    DEBUG = True
    SEND_FILE_MAX_AGE_DEFAULT = None
    # TODO: Front 호출 시 처리
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    """Flask Config for Prod"""
    pass