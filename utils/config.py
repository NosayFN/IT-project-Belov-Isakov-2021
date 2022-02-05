import os


class Config(object):
    # Global instance
    _instance = None
    _database_url = None
    DEBUG = True
    CSRF_ENABLED = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = None

    def __init__(self):
        self._token = os.environ.get('TOKEN', None)
        self.SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', None)
        Config._instance = self

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = Config()
        return cls._instance

    @property
    def url(self):
        return "https://api.telegram.org/bot" + self._token + "/"
