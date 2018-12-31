from config import Config


class DevConfig(Config):
    HOST = 'localhost'
    PORT = 5000
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:wasitacatisaw?@localhost:3306/meant"
    SQLALCHEMY_ECHO = True

    RUN_SETTING = dict(Config.RUN_SETTING, **{
        'host': HOST,
        'port': PORT,
        'debug': DEBUG
    })

    Config.SWAGGER['host'] = '{}:{}'.format(Config.REPRESENTATIVE_HOST or HOST, PORT)
