import os

from clojos_common.util import env

class Env(env.Env):

    @staticmethod
    def log_level():
        return int(os.environ.get('LOGGING_LEVEL', default=3))
