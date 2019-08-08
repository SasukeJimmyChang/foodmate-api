from datetime import timedelta

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_EXPIRATION_DELTA = timedelta(seconds=99999)
    JWT_AUTH_URL_RULE = "/v1/login"

class TestingConfig(Config):
    JWT_AUTH_HEADER_PREFIX = 'FLASK'
    SECRET_KEY = "yourkey"
    SQLALCHEMY_DATABASE_URI = "sqlite///:memory:"

class DevelopmentConfig(Config):
    JWT_AUTH_HEADER_PREFIX = 'FLASK'
    SECRET_KEY = "yourkey"
    SQLALCHEMY_DATABASE_URI = "YourMysqlUrl"

class ProductionConfig(Config):
    pass

app_config = {
    "testing" : TestingConfig,
    "development" : DevelopmentConfig,
    "production" : ProductionConfig
}
