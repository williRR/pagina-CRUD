class DevelopmentConfig():
    DEBUG = True
    
    
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
config ={
    'development': DevelopmentConfig
}