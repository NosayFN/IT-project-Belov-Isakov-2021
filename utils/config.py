import json


class Config(object):
    # Global instance
    _instance = None

    def __init__(self, **kwargs):
        filename = kwargs.get('file')

        with open(filename) as config_file:
            config = json.loads(config_file.read())
        self._url = config.get('url', None)

        Config._instance = self

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = Config(file='config.json')
        return cls._instance

    @property
    def url(self):
        return self._url
