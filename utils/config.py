import os


class Config(object):
    # Global instance
    _instance = None

    def __init__(self):
        self._token = os.environ.get('TOKEN', None)
        Config._instance = self

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = Config()
        return cls._instance

    @property
    def url(self):
        return "https://api.telegram.org/bot" + self._token + "/"
